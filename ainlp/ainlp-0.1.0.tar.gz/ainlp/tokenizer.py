import string


class QATokenizer(object):
    """
    专用于QA问题的Tokenizer
    相对于transformer提供的tokenizer，返回token到text字符索引，以及text字符到token的反向索引，以便于上层应用追踪tokenize后位置
    """
    def __init__(self, tokenizer):
        """
        :param tokenizer: transformer提供的tokenizer实例
        """
        self.tokenizer = tokenizer

    def _get_doc_tokens(self, text):
        """ 将中文文本序列处理成可以被tokenizer独立分割的单元
        类似于transformers提供的BasicTokenizer，但它返回token到character的索引，以及反向索引
        用于中文带英文或数字的情况，比如：
        olay玉兰油618促销，需要切分成['olay', '玉', '兰', '油', '618', '促', '销']
        :param text: character sequence
        :return: tokens, chr_to_tok_index, tok_to_chr_index
        """
        ascii_digits = string.ascii_letters + string.digits
        prev_token = ''
        tokens, chr_to_tok_index = [], []
        for i, c in enumerate(text):
            if c in ascii_digits:
                prev_token += c
                chr_to_tok_index.append(len(tokens))
            else:
                if prev_token:
                    tokens.append(prev_token)
                    prev_token = ''
                chr_to_tok_index.append(len(tokens))
                tokens.append(c)
        if prev_token:
            tokens.append(prev_token)

        tok_to_chr_index = []
        cur_len = 0
        for i, tok in enumerate(tokens):
            tok_to_chr_index.append(cur_len)
            cur_len += len(tok)
        return tokens, chr_to_tok_index, tok_to_chr_index

    def tokenize(self, text, return_index=True, **kwargs):
        """
        :param text: 字符序列
        :param return_index: 是否返回token到字符的索引，以及反向索引
        :param kwargs: 可以传入到tokenizer的其他参数
        :return: tokens, (chr_to_tok_index, tok_to_chr_index)
            tokens: token list
            chr_to_tok_index: optional, a list for character to token index
            tok_to_chr_index: optional, a list for token to character index
        """
        if return_index:
            doc_tokens, chr_to_tok_index, tok_to_chr_index = self._get_doc_tokens(text)
            chr_to_sub_index, sub_to_chr_index = [], []
            all_sub_tokens = []
            for i, tok in enumerate(doc_tokens):
                sub_tokens = self.tokenizer.tokenize(tok, **kwargs)
                chr_len = tok_to_chr_index[i]
                if len(sub_tokens) == 0:  # 已知tok为空格时，sub_tokens为空
                    for j in range(len(tok)):
                        chr_to_sub_index.append(len(all_sub_tokens))
                for sub in sub_tokens:
                    sub_len = len(sub) - 2 if sub.startswith('##') else len(sub)  # WordPiece Tokenizer Prefix
                    for j in range(sub_len):
                        chr_to_sub_index.append(len(all_sub_tokens))
                    sub_to_chr_index.append(chr_len)
                    all_sub_tokens.append(sub)
                    chr_len += sub_len
            return all_sub_tokens, chr_to_sub_index, sub_to_chr_index
        else:
            tokens = self.tokenizer.tokenize(text, **kwargs)
            return tokens

    def __getattr__(self, name):
        return getattr(self.tokenizer, name)
