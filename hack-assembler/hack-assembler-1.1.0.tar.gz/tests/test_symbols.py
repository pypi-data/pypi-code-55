import re
import assembler.symbols as symbols
from assembler.parser import A_INSTRUCTION, C_INSTRUCTION, L_INSTRUCTION


PARSED_CODE = [
    {
        "type": "L_INSTRUCTION",
        "obj": re.fullmatch(L_INSTRUCTION, '(MAIN_LOOP)')

    },
    {
        "type": "C_INSTRUCTION",
        "obj": re.fullmatch(C_INSTRUCTION, 'AM=M-1')
    },
    {
        "type": "A_INSTRUCTION",
        "obj": re.fullmatch(A_INSTRUCTION, '@var1')
    },
    {
        "type": "A_INSTRUCTION",
        "obj": re.fullmatch(A_INSTRUCTION, '@MAIN_LOOP')
    },
    {
        "type": "C_INSTRUCTION",
        "obj": re.fullmatch(C_INSTRUCTION, '0;JMP')
    },
    {
        "type": "L_INSTRUCTION",
        "obj": re.fullmatch(L_INSTRUCTION, '(NESTED_LOOP)')

    },
    {
        "type": "A_INSTRUCTION",
        "obj": re.fullmatch(A_INSTRUCTION, '@var2')
    },
    {
        "type": "C_INSTRUCTION",
        "obj": re.fullmatch(C_INSTRUCTION, '0;JMP')
    }
]
SYMBOLS = {
    "MAIN_LOOP": 0,
    "NESTED_LOOP": 4,
    "var1": 16,
    "var2": 17
}


def test_symbols(mocker):
    assert symbols.get_symbol_table(PARSED_CODE) == {**symbols.default_symbols_table, **SYMBOLS}