import re
from typing import Optional

from sardine.lang.tokenizer.tokens import TOKEN_PATTERNS, COMMENT_TOKEN
from sardine.lang.tokenizer.objects import Token
from sardine.exceptions.lang.tokenizer.unknown_token import UnknownToken


class Tokenizer:

    @classmethod
    def tokenize(cls, code: str):
        code_lines = [line.strip() for line in code.splitlines() if line.strip()]
        tokens = []
        for n_line, line in enumerate(code_lines):
            whole_line = line
            while line:
                detected_token = cls._next_token(line)
                if detected_token is None:
                    raise UnknownToken(whole_line, line, n_line)
                if detected_token.type == COMMENT_TOKEN:
                    break
                line = line[len(detected_token.value):].strip()
                detected_token.value = detected_token.value.replace("'", '')
                tokens.append(detected_token)
        return tokens

    @staticmethod
    def _next_token(line: str) -> Optional[Token]:
        for token_type, regex in TOKEN_PATTERNS:
            match = re.search(r"\A{}".format(regex), line)
            if match:
                value = match.group(0)
                return Token(token_type, value)
