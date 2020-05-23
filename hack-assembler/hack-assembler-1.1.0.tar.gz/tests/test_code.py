import re
import assembler.code as code
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
        "obj": re.fullmatch(A_INSTRUCTION, '@next')
    },
    {
        "type": "A_INSTRUCTION",
        "obj": re.fullmatch(A_INSTRUCTION, '@MAIN_LOOP')
    },
    {
        "type": "C_INSTRUCTION",
        "obj": re.fullmatch(C_INSTRUCTION, '0;JMP')
    }
]
HACK_CODE = ['1111110010101000', '0000000000010000', '0000000000000000', '1110101010000111']


def test_code(mocker):
    mocker.patch.object(code, 'write_code')
    code.write_code.return_value = None

    assert code.assemble(PARSED_CODE, None) == HACK_CODE
