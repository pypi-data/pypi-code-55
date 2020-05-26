import requests, io, gzip, re, json

def get_gzip(url, offset=None, length=None):
    if offset is not None and length is not None:
        res = requests.get(url, headers = {'Range': f'bytes={offset}-{offset + length - 1}'})
        good_status = 206
    else:
        res = requests.get(url)
        good_status = 200
    if res.status_code == good_status:
        decompressed_file = gzip.GzipFile(fileobj = io.BytesIO(res.content))
        for line in decompressed_file:
            yield line.decode(errors = 'ignore')


class CCParser:

    def __init__(self, version='CC-MAIN-2020-16'):
        self.DATA_URL = f'https://commoncrawl.s3.amazonaws.com/crawl-data/{version}/warc.paths.gz'
        self.INDEX_URL = f'https://index.commoncrawl.org/{version}-index'


    def get_warcs(self):
        return [WARCData(x.strip()) for x in get_gzip(self.DATA_URL)]
 
    def url_search(self, url):
        res = requests.get(self.INDEX_URL, params={'url': url, 'output': 'json'})
        if res.status_code == 200:
            objs = [json.loads(line) for line in res.content.splitlines()]
            return [
                WARCData(obj['filename'], offset=int(obj['offset']), length=int(obj['length']))
                for obj in objs
            ]
        return []


class WARCData:
    
    def __init__(self, filename, offset=None, length=None):
       self.url = f'https://commoncrawl.s3.amazonaws.com/{filename}'
       self.offset = offset
       self.length = length

    def _file_generator(self):
        data = get_gzip(self.url, offset=self.offset, length=self.length)
        text = ''
        for line in data:
            if line.startswith('WARC/'):
                if text != '':
                    yield text.strip()
                text = line
            else:
                text += line
        yield text.strip()
     
    def data(self):
        gen = self._file_generator()
        if self.offset is None:
            next(gen) # skip warcinfo
        while True:
            try:
                if self.offset is None:
                    request, response, metadata = next(gen), next(gen), next(gen)
                else:
                    request = metadata = None
                    response = next(gen)
                x = response.split('\r\n\r\n', 2)
                if len(x) != 3:
                    # malformed entry?
                    continue
                response_warc, header, content = x
                url_match = re.search('WARC-Target-URI: (.*)', response_warc)
                lang_match = None if metadata is None else re.search('languages-cld2: (.*)', metadata)
                content_type_match = re.search('Content-Type: (.*)', header)
                out = {
                    'url': url_match.group(1).strip() if url_match else '',
                    'http_response': header.splitlines()[0].strip(),
                    'content-type': content_type_match.group(1).strip() if content_type_match else '',
                    'html': content.strip(),
                }
                if lang_match is not None:
                    out['languages'] = json.loads(lang_match.group(1)).get('languages', []) if lang_match else []
                yield out
            except StopIteration:
                break
