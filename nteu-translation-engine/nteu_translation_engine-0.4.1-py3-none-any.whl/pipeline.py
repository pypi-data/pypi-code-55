from pangeamt_nlp.processor.pipeline_decoding import PipelineDecoding
from pangeamt_nlp.truecaser.truecaser import Truecaser
from pangeamt_nlp.bpe.bpe import BPE
from pangeamt_nlp.tokenizer.tokenizer_factory import TokenizerFactory
from pangeamt_nlp.seg import Seg
from typing import Dict
import os


class Pipeline:

    def __init__(self, config: Dict):
        self._config = config
        self._src_lang = config["src_lang"]
        self._tgt_lang = config["tgt_lang"]
        self._processors = self.load_decoding_pipeline()
        self._src_bpe = self.load_bpe()
        self._src_truecaser, self._tgt_truecaser = self.load_truecaser()
        self._src_tokenizer, self._tgt_tokenizer = self.load_tokenizer()

    async def preprocess(self, seg: Seg):
        self._processors.process_src(seg)
        seg.src = self._src_tokenizer.tokenize(seg.src)
        if self._src_truecaser is not None:
            seg.src = self._src_truecaser.truecase(seg.src)
        if self._src_bpe is not None:
            seg.src = self._src_bpe.apply(seg.src)

    async def postprocess(self, seg: Seg):
        seg.tgt = BPE.undo(seg.tgt)
        seg.tgt = self._tgt_tokenizer.detokenize(seg.tgt.split(" "))
        seg.tgt = self._tgt_truecaser.detruecase(seg.tgt)
        self._processors.process_tgt(seg)

    def load_decoding_pipeline(self):
        return PipelineDecoding.create_from_dict(
            self._src_lang, self._tgt_lang, self._config["processors"]
        )

    def load_bpe(self):
        if self._config["bpe"] is not None:
            path = self._config["translation_engine_server"]["bpe"]
            if self._config["bpe"]["joint"]:
                codes = os.path.join(path, "codes32k.txt")
                vocab = os.path.join(path, "src_vocab.txt")
                return BPE(codes, vocab)
            else:
                codes = os.paht.join(path, "src_codes.txt")
                return BPE(codes)
        return None

    def load_truecaser(self):
        if self._config["truecaser"]["src"] == "enabled":
            path = os.path.join(
                self._config["translation_engine_server"]["truecaser"],
                "src_model.txt"
            )
            truecaser = Truecaser(path)
            return truecaser, truecaser
        else:
            return None, Truecaser()

    def load_tokenizer(self):
        src_tok_name = self._config["tokenizer"]["src"]
        tgt_tok_name = self._config["tokenizer"]["tgt"]

        src_tokenizer = TokenizerFactory.new(self._src_lang, src_tok_name)
        tgt_tokenizer = TokenizerFactory.new(self._tgt_lang, tgt_tok_name)

        return (src_tokenizer, tgt_tokenizer)
