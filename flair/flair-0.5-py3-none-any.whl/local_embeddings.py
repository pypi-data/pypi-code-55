from abc import abstractmethod
from pathlib import Path
from typing import Union, List

import torch, re
import sentencepiece as sp
from more_itertools import iterate
from transformers import BertModel, BertTokenizer, DistilBertTokenizer, DistilBertModel, AlbertTokenizer, AlbertModel, \
    AutoTokenizer, AutoModel, AutoConfig, XLNetTokenizer, T5Tokenizer, GPT2Tokenizer, OpenAIGPTTokenizer, \
    TransfoXLPreTrainedModel

import flair
from flair.data import DataPair, Sentence, Token
from flair.embeddings import Embeddings, DocumentEmbeddings, TokenEmbeddings, ScalarMix, RoBERTaEmbeddings


class PairEmbeddings(Embeddings):

    def __init__(self, embeddings: DocumentEmbeddings):
        """The constructor takes a list of embeddings to be combined."""
        super().__init__()
        self.embeddings = embeddings

    @property
    def embedding_type(self) -> str:
        return "data-pair-level"

    @property
    def embedding_length(self) -> int:
        return self.embeddings.embedding_length * 2

    def embed(self, pairs: Union[DataPair, List[DataPair]]):

        # if only one sentence is passed, convert to list of sentence
        if type(pairs) is DataPair:
            pairs = [pairs]

        all_first = [pair.first for pair in pairs]
        all_second = [pair.second for pair in pairs]

        self.embeddings.embed(all_first)
        self.embeddings.embed(all_second)


class TransformerWordEmbeddings_NoBatch(TokenEmbeddings):
    def __init__(
        self,
        model: str = "bert-base-uncased",
        layers: str = "-1,-2,-3,-4",
        pooling_operation: str = "first",
        use_scalar_mix: bool = False,
        fine_tune: bool = False
    ):
        """
        Bidirectional transformer embeddings of words, as proposed in Devlin et al., 2018.
        :param bert_model_or_path: name of BERT model ('') or directory path containing custom model, configuration file
        and vocab file (names of three files should be - config.json, pytorch_model.bin/model.chkpt, vocab.txt)
        :param layers: string indicating which layers to take for embedding
        :param pooling_operation: how to get from token piece embeddings to token embedding. Either pool them and take
        the average ('mean') or use first word piece embedding as token embedding ('first)
        :param document_only: set only document (sentence) emebddings
        """
        super().__init__()

        # load tokenizer and transformer model
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        config = AutoConfig.from_pretrained(model, output_hidden_states=True)
        self.model = AutoModel.from_pretrained(model, config=config)

        # model name
        self.name = str(model)

        # when initializing, embeddings are in eval mode by default
        self.model.eval()
        self.model.to(flair.device)

        # embedding parameters
        self.layer_indexes = [int(x) for x in layers.split(",")]
        self.pooling_operation = pooling_operation
        self.use_scalar_mix = use_scalar_mix
        self.fine_tune = fine_tune
        self.static_embeddings = not self.fine_tune

        self.special_tokens = []
        self.special_tokens.append(self.tokenizer.bos_token)
        self.special_tokens.append(self.tokenizer.cls_token)

        # most models have an intial BOS token, except for XLNet, T5 and GPT2
        self.begin_offset = 1
        if isinstance(self.tokenizer, XLNetTokenizer):
            self.begin_offset = 0
        if isinstance(self.tokenizer, T5Tokenizer):
            self.begin_offset = 0
        if isinstance(self.tokenizer, GPT2Tokenizer):
            self.begin_offset = 0


    def _add_embeddings_internal(self, sentences: List[Sentence]) -> List[Sentence]:
        """Add embeddings to all words in a list of sentences. If embeddings are already added,
        updates only if embeddings are non-static."""

        # gradients are enabled if fine-tuning is enabled
        gradient_context = torch.enable_grad() if (self.fine_tune and self.training) else torch.no_grad()

        with gradient_context:

            # first, subtokenize each sentence and find out into how many subtokens each token was divided
            for sentence in sentences:

                # subtokenize sentence
                subtokenized_sentence = self.tokenizer.encode(sentence.to_tokenized_string(), add_special_tokens=True)

                # push sentence through model
                input_ids = torch.tensor(subtokenized_sentence, dtype=torch.long, device=flair.device).unsqueeze(0)
                hidden_states = self.model(input_ids)[-1]

                word_iterator = iter(sentence)
                token = next(word_iterator)

                token_subtoken_lengths = []
                reconstructed_token = ''
                subtoken_count = 0

                # iterate over subtokens and reconstruct tokens
                subtokens = self.tokenizer.convert_ids_to_tokens(subtokenized_sentence)
                for subtoken_id, subtoken in enumerate(subtokens):

                    subtoken_count += 1

                    # remove special markup
                    subtoken = re.sub('^Ġ', '', subtoken)    # RoBERTa models
                    subtoken = re.sub('^##', '', subtoken)   # BERT models
                    subtoken = re.sub('^▁', '', subtoken)    # XLNet models
                    subtoken = re.sub('</w>$', '', subtoken) # XLM models

                    # append subtoken to reconstruct token
                    reconstructed_token = reconstructed_token + subtoken

                    # check if reconstructed token is special begin token ([CLS] or similar)
                    if reconstructed_token in self.special_tokens and subtoken_id == 0:
                        reconstructed_token = ''
                        subtoken_count = 0

                    # check if reconstructed token is the same as current token
                    if reconstructed_token.lower() == token.text.lower():

                        subtoken_embeddings: List[torch.FloatTensor] = []

                        # get states from all selected layers, aggregate with pooling operation
                        for layer in self.layer_indexes:
                            current_embeddings = hidden_states[layer][0][subtoken_id-subtoken_count+1:subtoken_id+1]

                            if self.pooling_operation == "first":
                                final_embedding: torch.FloatTensor = current_embeddings[0]

                            if self.pooling_operation == "last":
                                final_embedding: torch.FloatTensor = current_embeddings[-1]

                            if self.pooling_operation == "first_last":
                                final_embedding: torch.Tensor = torch.cat([current_embeddings[0], current_embeddings[-1]])

                            if self.pooling_operation == "mean":
                                all_embeddings: List[torch.FloatTensor] = [
                                    embedding.unsqueeze(0) for embedding in current_embeddings
                                ]
                                final_embedding: torch.Tensor = torch.mean(torch.cat(all_embeddings, dim=0), dim=0)

                            subtoken_embeddings.append(final_embedding)

                        # use scalar mix of embeddings if so selected
                        if self.use_scalar_mix:
                            sm = ScalarMix(mixture_size=len(subtoken_embeddings))
                            sm_embeddings = sm(subtoken_embeddings)

                            subtoken_embeddings = [sm_embeddings]

                        # set the extracted embedding for the token
                        token.set_embedding(self.name, torch.cat(subtoken_embeddings))

                        # reset subtoken count and reconstructed token
                        reconstructed_token = ''
                        subtoken_count = 0

                        # break from loop if all tokens are accounted for
                        if token.idx < len(sentence):
                            token = next(word_iterator)
                        else:
                            break

        return sentences

    @property
    @abstractmethod
    def embedding_length(self) -> int:
        """Returns the length of the embedding vector."""
        return (
            len(self.layer_indexes) * self.model.config.hidden_size
            if not self.use_scalar_mix
            else self.model.config.hidden_size
        )


class TransformerWordEmbeddings_ScalarMix(TokenEmbeddings):
    def __init__(
        self,
        model: str = "bert-base-uncased",
        layers: str = "-1,-2,-3,-4",
        pooling_operation: str = "first",
        use_scalar_mix: bool = True,
        fine_tune: bool = False
    ):
        """
        Bidirectional transformer embeddings of words from various transformer architectures.
        :param model: name of transformer model (see https://huggingface.co/transformers/pretrained_models.html for
        options)
        :param layers: string indicating which layers to take for embedding (-1 is topmost layer)
        :param pooling_operation: how to get from token piece embeddings to token embedding. Either take the first
        subtoken ('first'), the last subtoken ('last'), both first and last ('first_last') or a mean over all ('mean')
        :param batch_size: How many sentence to push through transformer at once. Set to 1 by default since transformer
        models tend to be huge.
        :param use_scalar_mix: If True, uses a scalar mix of layers as embedding
        :param fine_tune: If True, allows transformers to be fine-tuned during training
        """
        super().__init__()

        # load tokenizer and transformer model
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        config = AutoConfig.from_pretrained(model, output_hidden_states=True)
        self.model = AutoModel.from_pretrained(model, config=config)

        # model name
        self.name = 'transformer-word-' + str(model)

        # when initializing, embeddings are in eval mode by default
        self.model.eval()
        self.model.to(flair.device)

        # embedding parameters
        self.layer_indexes = [int(x) for x in layers.split(",")]
        self.mix = ScalarMix(mixture_size=len(self.layer_indexes), trainable=True)
        self.pooling_operation = pooling_operation
        self.use_scalar_mix = use_scalar_mix
        self.fine_tune = fine_tune
        self.static_embeddings = not self.fine_tune
        if self.use_scalar_mix:
            self.static_embeddings = False
        self.batch_size = 1

        self.special_tokens = []
        self.special_tokens.append(self.tokenizer.bos_token)
        self.special_tokens.append(self.tokenizer.cls_token)

        # most models have an intial BOS token, except for XLNet, T5 and GPT2
        self.begin_offset = 1
        if type(self.tokenizer) == XLNetTokenizer:
            self.begin_offset = 0
        if type(self.tokenizer) == T5Tokenizer:
            self.begin_offset = 0
        if type(self.tokenizer) == GPT2Tokenizer:
            self.begin_offset = 0

        # initialize cache if use_cache set
        self.cache = None
        use_cache = True
        if use_cache:
            cache_path = Path(f'{self.name}-tmp-cache.sqllite')
            from sqlitedict import SqliteDict
            self.cache = SqliteDict(str(cache_path), autocommit=True)

    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        state['cache'] = None
        return state

    def _add_embeddings_internal(self, sentences: List[Sentence]) -> List[Sentence]:
        """Add embeddings to all words in a list of sentences."""

        # embed each micro-batch
        for sentence in sentences:
            self._add_embeddings_to_sentence(sentence)

        return sentences

    def _add_embeddings_to_sentence(self, sentence: Sentence):
        """Match subtokenization to Flair tokenization and extract embeddings from transformers for each token."""

        # first, subtokenize each sentence and find out into how many subtokens each token was divided
        tokenized_string = sentence.to_tokenized_string()

        all_token_embeddings = self.cache.get(tokenized_string)

        if not all_token_embeddings:

            # method 2:
            ids = self.tokenizer.encode(tokenized_string, add_special_tokens=False)
            input_ids = torch.tensor(self.tokenizer.build_inputs_with_special_tokens(ids), dtype=torch.long, device=flair.device)
            subtokens = self.tokenizer.convert_ids_to_tokens(input_ids)

            input_ids = input_ids.unsqueeze(0)

            word_iterator = iter(sentence)
            token = next(word_iterator)
            token_text = token.text.lower()

            token_subtoken_lengths = []
            reconstructed_token = ''
            subtoken_count = 0

            # iterate over subtokens and reconstruct tokens
            for subtoken_id, subtoken in enumerate(subtokens):

                subtoken_count += 1

                # remove special markup
                subtoken = re.sub('^Ġ', '', subtoken)    # RoBERTa models
                subtoken = re.sub('^##', '', subtoken)   # BERT models
                subtoken = re.sub('^▁', '', subtoken)    # XLNet models
                subtoken = re.sub('</w>$', '', subtoken) # XLM models

                # append subtoken to reconstruct token
                reconstructed_token = reconstructed_token + subtoken

                # print(reconstructed_token)

                # check if reconstructed token is special begin token ([CLS] or similar)
                if reconstructed_token in self.special_tokens and subtoken_id == 0:
                    reconstructed_token = ''
                    subtoken_count = 0

                # special handling for UNK subtokens
                if self.tokenizer.unk_token and self.tokenizer.unk_token in reconstructed_token:
                    pieces = self.tokenizer.convert_ids_to_tokens(
                        self.tokenizer.encode(token.text, add_special_tokens=False))
                    token_text = ''
                    for piece in pieces:
                        # remove special markup
                        piece = re.sub('^Ġ', '', piece)  # RoBERTa models
                        piece = re.sub('^##', '', piece)  # BERT models
                        piece = re.sub('^▁', '', piece)  # XLNet models
                        piece = re.sub('</w>$', '', piece)  # XLM models
                        token_text += piece
                    token_text = token_text.lower()

                # check if reconstructed token is the same as current token
                if reconstructed_token.lower() == token_text:

                    # if so, add subtoken count
                    token_subtoken_lengths.append(subtoken_count)

                    # reset subtoken count and reconstructed token
                    reconstructed_token = ''
                    subtoken_count = 0

                    # break from loop if all tokens are accounted for
                    if len(token_subtoken_lengths) < len(sentence):
                        token = next(word_iterator)
                        token_text = token.text.lower()
                    else:
                        break

            # put encoded batch through transformer model to get all hidden states of all encoder layers
            hidden_states = self.model(input_ids)[-1]
            hidden_states = [layer.clone().detach().cpu() for layer in hidden_states]

            # gradients are enabled if fine-tuning is enabled
            gradient_context = torch.enable_grad() if (self.fine_tune and self.training) else torch.no_grad()

            if self.use_scalar_mix and self.training:
                gradient_context = torch.enable_grad()

            with gradient_context:

                subword_start_idx = self.begin_offset

                sentence_idx = 0

                all_token_embeddings = []

                # for each token, get embedding
                for token_idx, (token, number_of_subtokens) in enumerate(zip(sentence, token_subtoken_lengths)):

                    subword_end_idx = subword_start_idx + number_of_subtokens

                    subtoken_embeddings: List[torch.FloatTensor] = []

                    # get states from all selected layers, aggregate with pooling operation
                    for layer in self.layer_indexes:
                        current_embeddings = hidden_states[layer][sentence_idx][subword_start_idx:subword_end_idx]

                        if self.pooling_operation == "first":
                            final_embedding: torch.FloatTensor = current_embeddings[0]

                        if self.pooling_operation == "last":
                            final_embedding: torch.FloatTensor = current_embeddings[-1]

                        if self.pooling_operation == "first_last":
                            final_embedding: torch.Tensor = torch.cat([current_embeddings[0], current_embeddings[-1]])

                        if self.pooling_operation == "mean":
                            all_embeddings: List[torch.FloatTensor] = [
                                embedding.unsqueeze(0) for embedding in current_embeddings
                            ]
                            final_embedding: torch.Tensor = torch.mean(torch.cat(all_embeddings, dim=0), dim=0)

                        subtoken_embeddings.append(final_embedding)

                    all_token_embeddings.append(subtoken_embeddings)

                    subword_start_idx += number_of_subtokens

            self.cache[tokenized_string] = all_token_embeddings

        self.mix = self.mix.cpu()
        for token, embeddings in zip(sentence, all_token_embeddings):

            # use scalar mix of embeddings if so selected
            if self.use_scalar_mix:
                # embeddings = [emb.to(flair.device) for emb in embeddings]
                sm_embeddings = self.mix(embeddings)
                #
                embeddings = [sm_embeddings]
                # embeddings = [embeddings[0]]

            # set the extracted embedding for the token
            token.set_embedding(self.name, torch.cat(embeddings))

    def train(self, mode=True):
        if not self.fine_tune:
            pass
        else:
            super().train(mode)

    @property
    @abstractmethod
    def embedding_length(self) -> int:
        """Returns the length of the embedding vector."""

        if not self.use_scalar_mix:
            length = len(self.layer_indexes) * self.model.config.hidden_size
        else:
            length = self.model.config.hidden_size

        if self.pooling_operation == 'first_last': length *= 2

        return length
