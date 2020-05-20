#!/usr/bin/env python3

# stdlibs:
from urllib.parse import urlparse
import re
import requests
# external:
from fdroidserver import common, index


def mirrors(fingerprint='43238D512C1E5EB2D6569F4A3AFBF5523418B82E0A3ED1552770ABB9A9C9CCAB'):
    """
    - Extract mirrors from README.md
    - Download index from first mirror and extract potential missing mirrors

    :param fingerprint: used when downloading index from first mirror
    :return: dict of mirror urls where True means that the mirror is included in the index (=official) {url: True/False}
    """

    config = dict()
    config['jarsigner'] = 'jarsigner'
    common.config = config
    index.config = config

    with open('README.md') as fp:
        readme = fp.read()
    teststr = '## Active Mirrors'

    # if the README has a fingerprint, prefer that one
    for line in readme.split('\n'):
        m = re.match(r'^fingerprint.*([0-9A-Fa-f]{64})$', line)
        if m:
            fingerprint = m.group(1)
            break

    main = 1
    mirrors = dict()
    for line in readme[readme.find(teststr) + len(teststr) + 1:].split('\n'):
        if not line:
            continue

        match = re.match('^\\s*\\*\\s*(http.*|rsync.*)', line)
        if not match:
            continue

        url = match.group(1)
        if url not in mirrors:
            # add mirror as unofficial
            mirrors[url] = False

        if len(mirrors) == main:
            print("Extracting official mirrors from repo index of %s/repo/index-v1.jar ..." %
                  url, end=' ', flush=True)
            try:
                data, _ = index.download_repo_index(
                    url + '/repo?fingerprint=' + fingerprint, timeout=60)
            except TimeoutError:
                print("\n%s timed out. Trying different mirror...",
                      url, end=' ', flush=True)
                main += 1

            print("done")

    for mirror in mirrors:
        if mirror + '/repo' in data['repo']['mirrors']:
            # mirror is official
            mirrors[mirror] = True

    return mirrors


def repos():
    """
    Extract repos from izzy, wiki

    :return: array of repo urls
    """
    repos = set()
    izzyurl = 'https://android.izzysoft.de/articles/named/list-of-fdroid-repos'
    repo_pattern = re.compile(b'https://[^<]+/repo')
    r = requests.get(izzyurl, allow_redirects=True)
    if r.status_code == 200:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                for repo in repo_pattern.findall(chunk):
                    repos.add(repo.decode())

    wikiurl = 'https://forum.f-droid.org/t/known-repositories/721.json?print=true'
    r = requests.get(wikiurl, allow_redirects=True)
    data = r.json()

    links = set()
    for link in data['details']['links']:
        links.add(link['url'])
    for link in links:
        print('checking', link)
        url = urlparse(link)
        if url.path.rstrip('/').endswith('/repo'):
            repos.add('https://' + url.hostname + url.path.rstrip('/'))
        else:
            for path in ('/repo', '/fdroid/repo'):
                try:
                    testurl = 'https://' + url.hostname + path
                    r = requests.head(testurl + '/index.jar')
                    if r.status_code == 200:
                        repos.add(testurl)
                        print('adding found repo:', testurl)
                except Exception as e:
                    print(e)
    return sorted(repos)
