__version__ = "0.0.1"

import os
import pandas as pd
import numpy as np
from plotnine import ggplot, theme, geom_point, geom_line, labs, element_text, aes

from itertools import islice
from github import Github

def get_stargazers_with_dates(repo):
    if isinstance(repo, str):
        g = Github(os.environ["GITHUB_TOKEN"])
        repo = g.get_repo(repo)

    sg_pages = list(repo.get_stargazers_with_dates())
    
    res = pd.DataFrame([entry.raw_data for entry in sg_pages]) \
        .assign(
            author=lambda d: d.user.map(lambda x: x["login"]),
            ttl = lambda d: np.arange(len(d)),
            starred_at = lambda d: pd.to_datetime(d.starred_at)
        ) \
        .drop(columns = 'user')

    return res

def plot_stargazers(data):
    return ggplot(data, aes("starred_at", "ttl")) \
            + geom_line(aes(group = 1)) \
            + geom_point() \
            + theme(axis_text_x = element_text(angle = 45, hjust = 1)) \
            + labs(title = "stargazers over time")
