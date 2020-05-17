from pathlib2 import Path

SPLIT_FG_IMPLEMENTED = ['FG_ISA','FG_IRMODE']
COLAPSE_FG_IMPLEMENTED = ['FG_COMPLEX']


SUPPORTED_VERSIONS = ['4.24', '5.0', '5.00 Bruker JCAMP library', '5.00 BRUKER JCAMP library', '5.01']
GRAMMAR = {
        'COMMENT_LINE' : '\$\$[^\n]*\n',
        'PARAMETER': '##',
        'USER_DEFINED' : '\$',
        'TRAILING_EOL' : '\n$',
        'DATA_LABEL' : '\(XY..XY\)',
        'DATA_DELIMETERS':', |\n',
        'SIZE_BRACKET': '^\([^\(\)<>]*\)(?!$)',
        'LIST_DELIMETER': ', ',
        'EQUAL_SIGN': '=',
        'PARALLEL_BRACKET': '\) ',
        'GEO_OBJ': '\(\(\([\s\S]*\)[\s\S]*\)[\s\S]*\)',
        'HEADER':'TITLE|JCAMPDX|JCAMP-DX|DATA TYPE|DATATYPE|ORIGIN|OWNER',
        'VERSION_TITLE':'JCAMPDX|JCAMP-DX'
    }
MAX_LINE_LEN = 78