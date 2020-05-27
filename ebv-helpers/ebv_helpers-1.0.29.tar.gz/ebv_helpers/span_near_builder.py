# coding=utf-8
import re
import logging

BRAND_IDENTIFIER = '_brand_'

LOGGER = logging.getLogger(__name__)


class InvalidPatternError(Exception):
    def __init__(self, msg):
        self.msg = msg


class SpanNearBuilder(object):
    """ https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-span-near-query.html
    Span queries are low-level positional queries which provide
    expert control over the order and proximity of the specified terms.
    """
    ASTERISKS_SEPARATOR_REGEX = r"(?=(\S+)\s\*\s(\S+))\1"
    EXCLUDE_PATTERN_REGEX = r"\s\-(?P<pattern>([^\r\n\t\f\v \-](\s[^\r\n\t\f\v \-])?)+)(?=\s|$)"

    def __init__(self, slop=5, field='body', is_percolator_query=True):
        """
        :param slop:
        :param field:
        """
        self.slop = slop
        self.field = field
        self.is_percolator_query = is_percolator_query
        self.words_in_pattern = {
            'prefix+suffix': [],
            'suffix': [],
            'infix': [],
            'prefix': [],
            'word': []
        }

    def get_prefix(self, word):
        return {
            "field_masking_span": {
                "query": {
                    "span_term": {
                        "{}.prefix".format(self.field): word
                    }
                },
                "field": self.field
            }
        }

    def get_wildcard(self, word):
        return {
            "span_multi": {
                "match": {
                    "wildcard": {
                        self.field: {
                            "value": word
                        }
                    }
                }
            }
        }

    def get_term(self, word):
        return {
            "span_term": {
                self.field: word
            }
        }

    @staticmethod
    def get_cleaned_word(word):
        """
            find the type of word which is used in the ES percolate query.
            Also sanitize the word from the character including asterisk.

            It is important because we use different analyzer types to fetch
            the patterns. Some use asterisk (*) because of the wildcard, some
            use only the word without asterisk (*) because their mapping don't
            require it like the custom analyzer 'wildcard_suffix_search_time',
            'wildcard_prefix' etc...
        :param word:
        :return:
        """
        if re.search(r"\S\*\S", word):
            raise InvalidPatternError("Inappropriate pattern! why asterisk (*) in the middle of the word used! :: %s"
                                      % word)
        elif re.search(r"^\*\S+\*$", word):
            word_type, cleaned_word = 'prefix+suffix', word[1:-1]
        elif re.search(r"^\*\S", word):
            word_type, cleaned_word = 'suffix', word[1:]
        elif re.search(r"\S\*$", word):
            word_type, cleaned_word = 'prefix', word[:-1]
        else:
            word_type, cleaned_word = 'word', word

        return word_type, cleaned_word

    def get_clause(self, cleaned_word, raw_word, word_type):
        if word_type in ['prefix+suffix', 'suffix']:
            clause = self.get_wildcard(raw_word)
        elif word_type in ['prefix']:
            if self.is_percolator_query:
                clause = self.get_prefix(cleaned_word)
            else:
                clause = self.get_wildcard(raw_word)
        elif word_type in ['word']:
            clause = self.get_term(cleaned_word)
        return clause

    def get_span_near(self, words, slop=0, is_set_word_type=True):
        """ span_near wrapper
        :param words:
        :param slop: distance of words
        :param is_set_word_type: update words_in_pattern dict?
        :return:
        """
        clauses = []
        for word in words:
            if not word or word == "*":
                continue

            word_type, cleaned_word = self.get_cleaned_word(word)
            if is_set_word_type:
                if cleaned_word not in self.words_in_pattern[word_type] \
                        and len(cleaned_word) >= 1 and cleaned_word != BRAND_IDENTIFIER:
                    self.words_in_pattern[word_type].append(cleaned_word)

            # word_type, cleaned_word, raw_word = self.find_word_type(word)
            clauses.append(self.get_clause(cleaned_word, word, word_type))
        return {
            "span_near": {
                "in_order": True,
                "clauses": clauses,
                "slop": slop
            }
        }

    def get_left_and_right_asterisk(self, pattern):
        """ Example usage is below
        :param pattern: 'lorem * ipsum dolor * sit amet'
        :return: [
            (lorem, ipsum),
            (dolor, sit)
        ]
        """
        for r in re.finditer(self.ASTERISKS_SEPARATOR_REGEX, pattern, re.MULTILINE):
            yield r.groups()

    def remove_excluded_patterns(self, pattern):
        return " ".join(re.sub(self.EXCLUDE_PATTERN_REGEX, '', pattern).split())

    def get_exclude_patterns(self, pattern):
        excluded_patterns = []
        for r in re.finditer(self.EXCLUDE_PATTERN_REGEX, pattern, re.MULTILINE):
            excluded_patterns.append(r.group('pattern'))  # remove last whitespace char.
        return excluded_patterns

    def build_excluded(self, exclude_patterns):
        should = []
        for pattern in exclude_patterns:
            split_pattern = pattern.split()
            if len(split_pattern) > 1:
                should.append(self.get_span_near(split_pattern, is_set_word_type=False))
            else:
                should.append(self.get_span_near([pattern], is_set_word_type=False))
        return {
            "bool": {
                "should": should
            }
        }

    def build_with_slop(self, word_groups):
        """ Separate words
        :param word_groups:
        :return:
        """
        must = list()
        for left_and_right_group in word_groups:
            must.append(self.get_span_near(left_and_right_group, slop=self.slop))
        return must

    def build_without_slop(self, word_groups):
        """ side by side words
        :param word_groups:
        :return:
        """
        must = list()
        for words in word_groups:
            if len(word_groups) > 1 and len(words) == 1:
                continue
            must.append(self.get_span_near(words, slop=0))
        return must

    def build(self, pattern):
        """ Build span_near query for pattern
        :param pattern:
        :return:
        """
        if not pattern:
            raise InvalidPatternError("Pattern is empty")
        must = list()
        should = list()

        exclude_patterns = self.get_exclude_patterns(pattern)
        pattern = self.remove_excluded_patterns(pattern)
        must.extend(self.build_with_slop(self.get_left_and_right_asterisk(pattern)))
        must.extend(self.build_without_slop([p.split() for p in pattern.split(' * ')]))

        field_type, word = self.find_biggest_word()
        query = {"bool": {}}
        if exclude_patterns:
            must_not_bool = self.build_excluded(exclude_patterns)
            query['bool']['must_not'] = must_not_bool

        if field_type == 'prefix+suffix' and self.is_percolator_query:
            should.extend(self.match(field_type, word))
            query['bool']['should'] = should
        elif self.is_percolator_query:
            must.extend(self.match(field_type, word))

        query['bool']['must'] = must

        return query

    def get_word_by_size(self, word_type):
        length = 0
        word = None
        for ii in self.words_in_pattern[word_type]:
            if word_type == "prefix+suffix":
                word = ii
                break
            if len(ii) > length:
                length = len(ii)
                word = ii
        if not word:
            LOGGER.exception('Inappropriate analysis pattern! %s', self.words_in_pattern[word_type])
        return word

    def find_biggest_word(self):
        """
            to improve the performance of analyzer percolate,
            some pattern have highest priority than some pattern causing the slow query!
            Soo the pattern get slower like hierarchy respectively
            word > prefix > suffix > prefix+suffix
        :return:
        """
        efficiency_order = ["word", "prefix", "suffix", "prefix+suffix"]
        inefficiency_order = list(reversed(efficiency_order))
        word_type = None
        for inefficient_word_type in inefficiency_order:
            find_status = False
            if len(self.words_in_pattern[inefficient_word_type]) > 0:
                for efficient_word_type in efficiency_order:
                    if len(self.words_in_pattern[efficient_word_type]) > 0:
                        word_type = efficient_word_type
                        find_status = True
                        break
            if find_status:
                break

        if not word_type:
            raise InvalidPatternError("words_in_pattern object is empty!")

        filtered_word = self.get_word_by_size(word_type)
        return word_type, filtered_word

    def get_word_types(self):
        word_types = [ii for ii in self.words_in_pattern if len(self.words_in_pattern[ii]) > 0]
        return word_types

    @staticmethod
    def match(field_type, word):
        if field_type in ['suffix', 'prefix']:
            return [
                {
                    "match": {
                        "filter_by_one_word.{}".format(field_type): word
                    }
                }
            ]

        elif field_type == 'prefix+suffix':
            return [
                {
                    "match": {
                        "filter_by_one_word.prefix": word
                    }
                },
                {
                    "match": {
                        "filter_by_one_word.suffix": word
                    }
                }
            ]
        else:
            return [
                {
                    "match": {
                        "filter_by_one_word": word
                    }
                }
            ]


class QueryStringBuilder(object):
    @staticmethod
    def is_equal_parentheses_count(query):
        return query.count("(") == query.count(")")

    @classmethod
    def build(cls, query, analyze_wildcard=True, default_operator="AND", fields=None):
        if not cls.is_equal_parentheses_count(query):
            raise InvalidPatternError("Parentheses count is not equal.")

        if len(query) < 1:
            raise InvalidPatternError("Query must not empty!")

        return {
            "query_string": {
                "analyze_wildcard": analyze_wildcard,
                "default_operator": default_operator,
                "query": query,
                "fields": fields
            }
        }
