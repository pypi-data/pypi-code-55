from datetime import datetime
from typing import List

from dateutil.relativedelta import relativedelta


GRANULARITY_STEP = {
    "seconds": lambda x: relativedelta(seconds=x),
    "minutes": lambda x: relativedelta(minutes=x),
    "hours": lambda x: relativedelta(hours=x),
    "days": lambda x: relativedelta(days=x),
    "weeks": lambda x: relativedelta(weeks=x),
    "months": lambda x: relativedelta(months=x),
    "years": lambda x: relativedelta(years=x),
}

START_MESSAGE = """
    ------------------------------------
    Runing ddbt iteration {i} / {iter_no}
    ------------------------------------
    Start interval:    {start}
    End interaval:     {end}
    Increment:         {increment}
    Granularity:       {granularity}
    ------------------------------------
    Current timestamp: {start_timestamp}
    Next timestamp:    {next_timestamp}
    ------------------------------------
"""

DDBT_TIME_ARGS = [
    {
        "name_or_flag": ["--start"],
        "default": datetime.now().strftime("%Y-%m-%d"),
        "help": "Start timestamp for looping. Default current date.",
    },
    {
        "name_or_flag": ["--end"],
        "default": datetime.now().strftime("%Y-%m-%d"),
        "help": "End timestamp for looping. Default current date.",
    },
    {
        "name_or_flag": ["--increment"],
        "default": 1,
        "type": int,
        "nargs": "?",
        "help": "Increment of time interval. Default 1.",
    },
    {
        "name_or_flag": ["--granularity"],
        "default": "days",
        "nargs": "?",
        "choices": ["seconds", "minutes", "hours", "days", "weeks", "months", "years"],
        "help": "Granularity of time interval. Default days.",
    },
]

DDBT_MAT_ARGS = [
    {
        "name_or_flag": ["-mat", "--materialization"],
        "nargs": "+",
        "choices": ["table", "view", "incremental"],
        "help": "Filter models by materialization type.",
    }
]

DDBT_GIT_ARGS = [
    {
        "name_or_flag": ["-cc", "--cached-changes"],
        "action": "store_true",
        "help": """
            If set, run only cached(staged) and untracked models/sources.
        """,
    },
    {
        "name_or_flag": ["-lc", "--last-changes"],
        "action": "store_true",
        "help": """
            If set, run models/sources that changed in last commit.
        """,
    },
    {
        "name_or_flag": ["-cd", "--commit-diff"],
        "action": "store_true",
        "help": """
            If set, run all models/sources changed accourding to diff from
            provided commit id to HEAD.
        """,
    },
    {
        "name_or_flag": ["-ci", "--commit-id"],
        "default": "HEAD^",
        "help": "Id of commit to be compared to HEAD. Default HEAD^.",
    },
]

DDBT_EXTRACT_ARGS = [
    {
        "name_or_flag": ["-s", "--sources"],
        "nargs": "+",
        "help": """
            Specify the sources to include. Please use only source name without
            extension.'.
        """,
    },
    {
        "name_or_flag": ["-e", "--embulk-template"],
        "nargs": "?",
        "help": """
            Specify the Jinja template name for Embulk. Please use only template name
            without extensions. It overrides settings in source or schema yml in
            meta section.
        """,
    },
    {
        "name_or_flag": ["--keep-template"],
        "action": "store_true",
        "help": """
            If set, rendered templates are not deleted after Embulk finish.
            Jinja templates will be stored in target-path. Useful for ex-post
            debugging.
        """,
    },
    {
        "name_or_flag": ["--dont-run"],
        "action": "store_true",
        "help": """
            If set, Embulk is not executed, only templates will be rendered.
            Jinja templates will be stored in target-path. Useful for manual
            execution with `embulk run [rendered template]`.
        """,
    },
    {
        "name_or_flag": ["--template-help"],
        "action": "store_true",
        "help": """
            If set, all parameters and functions usable in Jinja template.
            Useful for debugging and template creation.
        """,
    },
]

DDBT_BOOTSTRAP_ARGS = [
    {
        "name_or_flag": ["--missing-only"],
        "action": "store_true",
        "help": """
            If set, only missing sources are processed.
        """,
    },
]

DDBT_BOOTSTRAP_SOURCE_ARGS = [
    {
        "name_or_flag": ["-p", "--source-path"],
        "default": "./models/sources",
        "help": "Location where source files should be stored.",
    },
    {
        "name_or_flag": ["-db", "--raw-database"],
        "default": "prod",
        "help": "Name of the raw database",
    },
]

GIT_CURRENT_CHANGES = ["git", "ls-files", "--exclude-standard", "-ocm"]
GIT_LAST_CHANGES = ["git", "diff", "--name-only", "HEAD", "HEAD~1"]


def get_commit_diff(commit_id: str) -> List[str]:
    return ["git", "diff", "--name-only", "--diff-filter=ACMR", commit_id, "HEAD"]
