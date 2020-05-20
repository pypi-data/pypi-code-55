import re
import emoji
import jieba
import pyrefo
import string


class TextProcessor(object):
    """ 通用文本预处理
    """
    CLAUSE_DELIMITERS = [",", ".", "?", "!", ";", "~", "，", "。", "？", "！", "；", "～", " ", "…"]
    SENTENCE_DELIMITERS = [".", "?", "!", ";", "？", "！", "：", "。", "；"]

    def __init__(self):
        self.clause_regex = re.compile('|'.join(map(re.escape, self.CLAUSE_DELIMITERS)))
        self.html_entities_regex = re.compile(r'&#?[a-z0-9]{2,8};')
        self.link_regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.emoji_regex = re.compile('|'.join(map(re.escape, emoji.unicode_codes.UNICODE_EMOJI)))
        self.special_chr_regex = re.compile('\n|\\\\n')
        self.han_regex = re.compile('[^\u4E00-\u9FD5a-zA-Z0-9+#&\._%\-]+')
        self.sentence_regex = re.compile('|'.join(map(re.escape, self.SENTENCE_DELIMITERS)))

    def split_clauses(self, text):
        clauses = self.clause_regex.split(text)
        # 只保留非空的clause
        clauses = [cl for cl in clauses if cl != '']
        return clauses

    def split_sentences(self, text):
        sentences = self.sentence_regex.split(text)
        # 只保留非空的句子
        sentences = [s for s in sentences if s != '']
        return sentences

    def remove_html_entities(self, text):
        return self.html_entities_regex.sub('', text)

    def remove_emojis(self, text):
        return self.emoji_regex.sub('', text)

    def remove_links(self, text):
        return self.link_regex.sub('', text)

    def remove_special_chrs(self, text):
        return self.special_chr_regex.sub('', text)

    def remove_non_han(self, text):
        return self.han_regex.sub('，', text)

    def process(self, text, methods=['html_entities', 'emojis', 'links', 'special_chrs', 'non_han']):
        for m in methods:
            func = getattr(self, 'remove_' + m)
            text = func(text)
        clauses = self.split_clauses(text)
        return '，'.join(clauses)

    def test_html_entities(self, text):
        match = self.html_entities_regex.search(text)
        if match:
            return True
        return False

    def test_emojis(self, text):
        match = self.emoji_regex.search(text)
        if match:
            return True
        return False

    def test_links(self, text):
        match = self.link_regex.search(text)
        if match:
            return True
        return False

    def test_special_chrs(self, text):
        match = self.special_chr_regex.search(text)
        if match:
            return True
        return False


class Match(object):
    """ 模拟pyrefo.Match接口，可以手动构造Match """

    def __init__(self, state):
        self.state = state

    def span(self, key=None):
        return self[key]

    def start(self, key=None):
        return self[key][0]

    def end(self, key=None):
        return self[key][1]

    def group(self, key=None):
        return self[key]

    def __getitem__(self, key):
        try:
            return self.state[(key, 0)], self.state[(key, 1)]
        except KeyError:
            return KeyError(key)

    def __repr__(self):
        return 'Match(%d, %d)' % (self.start(), self.end())


class TokenMatcher(object):
    """ 在本的分词结果中搜索keyword，要求keyword完整匹配分词边界 """
    def __init__(self, text, clause_delimiter=None, sentence_delimiter=None):
        self.text = text
        self.clause_delimiter = clause_delimiter or TextProcessor.CLAUSE_DELIMITERS
        self.sentence_delimiter = sentence_delimiter or TextProcessor.SENTENCE_DELIMITERS
        self.tokens = jieba.lcut(text)
        # clause_index: token idx to clause idx map
        # sentence_index: token idx to sentence idx map
        # pos_index: token idx to character idx map
        self.clause_index, self.sentence_index, self.pos_index = self._build_index()

    def _build_index(self):
        clause_index, sentence_index, pos_index = [], [], []
        cur_cl_idx, cur_sent_idx, cur_len = 0, 0, 0
        for i, tok in enumerate(self.tokens):
            clause_index.append(cur_cl_idx)
            sentence_index.append(cur_sent_idx)
            pos_index.append(cur_len)
            cur_len += len(tok)
            if tok in self.clause_delimiter:
                cur_cl_idx += 1
            if tok in self.sentence_delimiter:
                cur_sent_idx += 1
        pos_index.append(cur_len)
        return clause_index, sentence_index, pos_index

    def _get_clause_start_idx(self, clause_idx):
        """ 返回第clause_idx分句起始token索引位置 """
        return self.clause_index.index(clause_idx)

    def _get_clause_end_idx(self, clause_idx):
        """ 返回第clause_idx分句下一个token索引位置 """
        try:
            return self.clause_index.index(clause_idx + 1)
        except ValueError:
            return len(self.tokens)

    def get_clause_range(self, start_tok_idx, end_tok_idx):
        """ 返回包含[start_tok_idx, end_tok_idx)区间内token序列的分句范围 """
        start_clause_idx = self.clause_index[start_tok_idx]
        clause_start_idx = self._get_clause_start_idx(start_clause_idx)
        end_clause_idx = self.clause_index[end_tok_idx - 1]
        clause_end_idx = self._get_clause_end_idx(end_clause_idx)
        return clause_start_idx, clause_end_idx

    def find_all(self, keyword):
        """
        查找keyword出现的所有最佳位置。在匹配时，需要考虑2点：
        1. “效果 更好”匹配“保湿效果还可以，配合金盏花爽肤水，效果会更好”时，选择到最佳匹配“效果会更好”
        2. 按分词匹配。“效果好”可以匹配到分词序列“效果 好”

        搜索算法：
        L(k)(i)：表示第k个part匹配到的第i个match
        k：表示搜索到到第k个part与第k+1个part最佳匹配
        i: 表示在第k个part搜索位置
        j: 表示在第k+1个part搜索位置
        先查找L(k)与L(k+1)最佳匹配对，再查找L(k+1)与L(k+2)最佳匹配对
        算法复杂度为O(k*N)
        """
        parts = keyword.split(' ')
        if len(parts) == 0:
            return []
        L = [pyrefo.findall(pyrefo.Phrase(p), self.tokens) for p in parts]
        if len(L) == 1:
            return L[0]
        for k in range(len(parts) - 1):
            m = 0  # 记录L(k)的起始位置
            best_matches = []  # 记录最佳匹配位置
            for j in range(len(L[k + 1])):
                best_i = None  # 记录L(k+1)(j)匹配到第k个part的最佳位置
                for i in range(m, len(L[k])):
                    if L[k][i].end() <= L[k + 1][j].start():  # L(k)(i)位置在L(k+1)(j)前面
                        best_i = i
                    else:
                        m = i  # 下次从这个位置开始搜索
                        break
                if best_i is not None:  # 找到一个最佳匹配
                    best_matches.append((best_i, j))
            # L(0)到L(k)只保留最佳匹配到的i位置元素
            for n in range(k + 1):
                L[n] = [L[n][p[0]] for p in best_matches]
            # L(k+1)只保留最佳匹配到的j位置元素
            L[k + 1] = [L[k + 1][p[1]] for p in best_matches]

        if len(L[0]) == 0:
            return []
        # 合并parts匹配的结果
        match = []
        for i in range(len(L[0])):
            match.append(Match({(None, 0): L[0][i].start(), (None, 1): L[-1][i].end()}))
        return match

    def search(self, keyword):
        """
        查找keyword出现的最佳位置。
        """
        m = self.find_all(keyword)
        d = [(p.end() - p.start()) for p in m]
        if len(m) > 0:
            index = min(range(len(d)), key=d.__getitem__)
            return m[index]
        return None

    def search_co_occurance(self, kw1, kw2):
        """ 查找共现词出现的最佳位置，即2个词相距最近 """
        kw1_match = self.find_all(kw1)
        kw2_match = self.find_all(kw2)
        if len(kw1_match) == 0 or len(kw2_match) == 0:
            return None
        kw1_pos = [m.start() for m in kw1_match]
        kw2_pos = [m.start() for m in kw2_match]
        pos_diff = [abs(kw1_pos[i] - kw2_pos[j]) for i in range(len(kw1_pos)) for j in range(len(kw2_pos))]
        index = min(range(len(pos_diff)), key=pos_diff.__getitem__)
        kw1_index, kw2_index = index // len(kw2_pos), index % len(kw2_pos)
        kw1_m, kw2_m = kw1_match[kw1_index], kw2_match[kw2_index]
        start = min(kw1_m.start(), kw2_m.start())
        end = max(kw1_m.end(), kw2_m.end())
        return Match({(None, 0): start, (None, 1): end,
                      ('kw1', 0): kw1_m.start(), ('kw1', 1): kw1_m.end(),
                      ('kw2', 0): kw2_m.start(), ('kw2', 1): kw2_m.end()})
