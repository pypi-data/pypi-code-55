USE_TOKEN = 'use_token'
REPOSITORY_NAME_TOKEN = 'repository_name_token'
STACK_NAME_TOKEN = 'stack_name_token'
AS_TOKEN = 'as_token'
ALIAS_TOKEN = 'alias_token'
LOAD_TOKEN = 'load_token'
FROM_TOKEN = 'from_token'
COMMENT_TOKEN = 'comment_token'

TOKEN_PATTERNS = [
    (USE_TOKEN, r'[Uu]se'),
    (AS_TOKEN, r'as'),
    (LOAD_TOKEN, r'[Ll]oad'),
    (FROM_TOKEN, r'from'),
    (COMMENT_TOKEN, r'#'),
    (REPOSITORY_NAME_TOKEN, r"'([A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+)'"),
    (STACK_NAME_TOKEN, r"'([A-Za-z0-9_.-]+)'"),
    (ALIAS_TOKEN, r'[A-Za-z0-9_.-]+')
]
