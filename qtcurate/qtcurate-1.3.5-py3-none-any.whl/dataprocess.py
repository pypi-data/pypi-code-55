from qtcurate.config import BASE_URL
import requests
import re
import json
from enum import Enum
from typing import Dict, List
import os.path
from qtcurate.exceptions import QtFileTypeError, QtArgumentError, QtConnectionError, QtRestApiError, QtDataProcessError


tag_files = "files"
tag_urls = "urls"
tag_title = "title"
tag_stitle = "stitle"
tag_index = "index"
tag_autotag = "get_phrases"
tag_max_token = "maxTokenPerUtt"
tag_min_token = "minTokenPerUtt"
tag_exclude_utt = "exclude_utt_without_entities"
tag_search_dict = "searchDictionaries"
tag_cmd = "cmd"
tag_sort_by_position = "sortByPosition"
phrase_matching_pattern = "phraseMatchingPattern"
phrase_matching_groups = "phraseMatchingGroups"
between_key_and_value = "skipPatternBetweenKeyAndValue"
between_values = "skipPatternBetweenValues"
search_mod = "searchMode"
analyze_mod = "analyzeMode"
stop_word_list = "stopwordList"
synonym_l = "synonymList"
tag_query = "query"
tag_sources = "sources"


class DictionaryType(Enum):
    NUMBER = "DOUBLE"
    STRING = "STRING"
    DATETIME = "DATETIME"
    NONE = "NONE"
    REGEX = "KEYWORD"


class ChunkMode(Enum):
    NONE = "NONE"
    SENTENCE = "SENTENCE"
    PARAGRAPH = "PARAGRAPH"
    PAGE = "PAGE"


class SearhMode(Enum):
    ORDERED_SPAN = "ORDERED_SPAN"
    FUZZY_ORDERED_SPAN = "FUZZY_ORDERED_SPAN"
    SPAN = "SPAN"
    FUZZY_SPAN = "FUZZY_SPAN"
    PARTIAL_SPAN = "PARTIAL_SPAN"
    PARTIAL_FUZZY_SPAN = "PARTIAL_FUZZY_SPAN"


class AnalyzeMode(Enum):
    EXACT = "EXACT"
    EXACT_CI = "EXACT_CI"
    WHITESPACE = "WHITESPACE"
    SIMPLE = "SIMPLE"
    STANDARD = "STANDARD"
    STEM = "STEM"


class DataProcess:

    def __init__(self, api_key: str, environment: str = ""):
        self.session = requests.Session()
        self.headers = {"X-API-Key": api_key}
        self.temp_dict = dict()
        self.temp_dict[tag_files] = []
        self.temp_dict[tag_urls] = []
        self.temp_dict[tag_title] = None
        self.temp_dict[tag_index] = None
        self.temp_dict[tag_autotag] = None
        self.temp_dict[tag_max_token] = None
        self.temp_dict[tag_min_token] = None
        self.temp_dict[tag_exclude_utt] = None
        self.temp_dict[tag_cmd] = None
        self.temp_dict[tag_search_dict] = []
        self.temp_dict[tag_query] = None
        self.temp_dict[tag_sources] = []
        if environment != "":
            environment = environment + "."
        self.url = 'http://' + environment + BASE_URL

    def title(self, value: str) -> None:
        """Create title for mining data"""

        if isinstance(value, str):
            self.temp_dict[tag_title] = value
        else:
            raise QtArgumentError("Argument type error: String is expected as title")

    def cmd(self, value: str) -> None:
        """Create cmd for mining data"""

        if isinstance(value, str):
            self.temp_dict[tag_cmd] = value
        else:
            raise QtArgumentError("Argument type error: String is expected as cmd")

    def query(self, value: str) -> None:
        """Create cmd for mining data"""

        if isinstance(value, str):
            self.temp_dict[tag_query] = value
        else:
            raise QtArgumentError("Argument type error: String is expected as cmd")

    def stitle(self, value: str) -> None:
        """Create title for mining data"""

        if isinstance(value, str):
            self.temp_dict[tag_stitle] = value
        else:
            raise QtArgumentError("Argument type error: String is expected as title")

    def index(self, value: str) -> None:
        """Create index for mining data, this is optional parameter"""

        if isinstance(value, (str, int)):
            self.temp_dict[tag_index] = value
        else:
            raise QtArgumentError("Argument type error: String is expected as index")

    def autotag(self, value: bool) -> None:
        """Set autotag for mining data, this is optional parameter"""

        if isinstance(value, bool):
            self.temp_dict[tag_autotag] = value
        else:
            raise QtArgumentError("Argument type error: Boolean is expected as autotag")

    def sort_by_position(self, value: bool) -> None:
        """Set sortByPosition for mining data, this is optional parameter"""

        if isinstance(value, bool):
            self.temp_dict[tag_sort_by_position] = value
        else:
            raise QtArgumentError("Argument type error: Boolean is expected as sortByPosition")

    def max_token_per_utt(self, value: int) -> None:
        """Create  max token per utt for mining data, this is optional parameter"""

        if isinstance(value, int):
            self.temp_dict[tag_max_token] = value
        else:
            raise QtArgumentError("Argument type error: Integer is expected as max token per utt")

    def min_token_per_utt(self, value: int) -> None:
        """Create min token per utt for mining data, this is optional parameter"""

        if isinstance(value, int):
            self.temp_dict[tag_min_token] = value
        else:
            raise QtArgumentError("Argument type error: Integer is expected as min token per utt")

    def exclude_utt_without_entities(self, value: bool) -> None:
        """Set exclude utt for mining data, this is optional parameter"""

        if isinstance(value, bool):
            self.temp_dict[tag_exclude_utt] = value
        else:
            raise QtArgumentError("Argument type error: Boolean is expected as exclude utt without entities")

    def files(self, list_of_files: list) -> None:
        """Create a list of existing files"""

        if isinstance(list_of_files, list):
            self.temp_dict[tag_files] = list_of_files
        else:
            raise QtArgumentError("Argument type error: Expected list of file indexes")

    def sources(self, list_of_files: list) -> None:
        """Create a list of existing files"""

        if isinstance(list_of_files, list):
            self.temp_dict[tag_sources] = list_of_files
        else:
            raise QtArgumentError("Argument type error: Expected list of file indexes")

    def urls(self, list_of_urls: list) -> None:
        """Create a list of existing files"""

        if isinstance(list_of_urls, list):
            self.temp_dict[tag_urls] = list_of_urls
        else:
            raise QtArgumentError("Argument type error: Expected list of urls")

    def search_rule(self, dictionary_path: str, vocab_value_type: DictionaryType = None, regex_phrase: str = None, regex_group: List = None,
                    skip_pattern_between_key_and_value: str = None, skip_pattern_between_values: str = None, stopword_list: str = None,
                    synonim_list: str = None, search_mode: SearhMode = None, analyze_mode: AnalyzeMode = None) -> None:
        """Prepare dictionary for searching"""

        vocab_dict = dict()
        if isinstance(dictionary_path, str):
            vocab_dict["vocabPath"] = dictionary_path
        else:
            raise QtArgumentError("Argument type error: String is expected as dictionary_path index")

        if vocab_value_type is not None:
            if isinstance(vocab_value_type, DictionaryType):
                vocab_dict["vocabValueType"] = vocab_value_type.value
            else:
                raise QtArgumentError("Argument type error: DictionaryType object is expected as vocab_value_type")

        if vocab_value_type.value == "REGEX":
            if regex_phrase is not None or regex_group is not None:
                vocab_dict[phrase_matching_pattern] = regex_phrase
                vocab_dict[phrase_matching_groups] = regex_group
            else:
                raise QtArgumentError("Argument type error: If use regex you have to add regex_phrase and regex_group")

        if regex_phrase is not None:
            if isinstance(regex_phrase, str):
                try:
                    re.compile(regex_phrase)
                    valid = True
                except re.error:
                    valid = False
                if valid is False:
                    raise QtArgumentError("Argument type error: Please write valid regular expression.")
            else:
                raise QtArgumentError("Argument type error: Please write valid regular expression.")

        if regex_group is not None:
            if not isinstance(regex_group, List):
                raise QtArgumentError("Argument type error: List is expected as regex group")

        if skip_pattern_between_key_and_value is not None:
            if isinstance(skip_pattern_between_key_and_value, str):
                vocab_dict[between_key_and_value] = skip_pattern_between_key_and_value
            else:
                raise QtArgumentError("Argument type error: String is expected as skip_pattern_between_key_and_value")

        if skip_pattern_between_values is not None:
            if isinstance(skip_pattern_between_values, str):
                vocab_dict[between_values] = skip_pattern_between_values
            else:
                raise QtArgumentError("Argument type error: String is expected as skip_pattern_between_values")

        if stopword_list is not None:
            if isinstance(stopword_list, str):
                vocab_dict[stop_word_list] = stopword_list
            else:
                raise QtArgumentError("Argument type error: String is expected as stopword_list")

        if synonim_list is not None:
            if isinstance(synonim_list, str):
                vocab_dict[synonym_l] = synonim_list
            else:
                raise QtArgumentError("Argument type error: String is expected as synonim_list")

        if search_mode is not None:
            if isinstance(search_mode, SearhMode):
                vocab_dict[search_mod] = search_mode.value
            else:
                raise QtArgumentError("Argument type error: SearchMode object is expected as search_mode")

        if analyze_mode is not None:
            if isinstance(analyze_mode, AnalyzeMode):
                vocab_dict[analyze_mod] = analyze_mode.value
            else:
                raise QtArgumentError("Argument type error: AnalyzeMode object is expected as analyze_mode")

        self.temp_dict[tag_search_dict].append(vocab_dict)

    def clear(self) -> None:
        """Remove all temporary data"""

        self.temp_dict[tag_files] = []
        self.temp_dict[tag_urls] = []
        self.temp_dict[tag_title] = None
        self.temp_dict[tag_index] = None
        self.temp_dict[tag_autotag] = None
        self.temp_dict[tag_max_token] = None
        self.temp_dict[tag_min_token] = None
        self.temp_dict[tag_exclude_utt] = None
        self.temp_dict[tag_search_dict] = []

    def upload(self, file: str) -> Dict:
        """Upload files for data mining"""

        if not isinstance(file, str):
            raise QtArgumentError("Argument type error: String is expected as file path")

        extension = os.path.splitext(file)[1].lower()
        if extension not in [".pdf", ".txt", ".html"]:
            raise QtArgumentError("Argument type error: PDF, TXT or HTML file expected")
        if not os.path.exists(file):
            raise QtArgumentError(f"Argument error: File {file} does not exist")
        files = {'file': open(file, 'rb')}
        try:
            res = self.session.post(self.url + "search/" + "file", headers=self.headers, files=files)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        
        return res.json()

    def create(self) -> Dict:
        """Mine data via dictionaries"""

        self.headers["Content-Type"] = "application/json"
        correct = 0
        if len(self.temp_dict[tag_search_dict]) == 0:
            raise QtDataProcessError("DataProcess error: Please add parameters using search_rule function")
        if len(self.temp_dict[tag_files]) > 0:
            data = {'files': self.temp_dict[tag_files], 'searchDictionaries': self.temp_dict[tag_search_dict]}
            correct += 1
        elif len(self.temp_dict[tag_urls]) > 0:
            data = {'urls': self.temp_dict[tag_urls], 'searchDictionaries': self.temp_dict[tag_search_dict]}
            correct += 1
        elif len(self.temp_dict[tag_sources]) > 0:
            data = {'urls': self.temp_dict[tag_sources], 'searchDictionaries': self.temp_dict[tag_search_dict]}
            correct += 1
        if correct != 1:
            raise QtDataProcessError("DataProcess error: You must choose one kind of data: files, URLs or source")
        if len(self.temp_dict[tag_search_dict]) != 0:
            data['searchDictionaries'] = self.temp_dict[tag_search_dict]
        if self.temp_dict[tag_title] is not None:
            data['title'] = self.temp_dict[tag_title]
        if self.temp_dict[tag_index] is not None:
            data['index'] = self.temp_dict[tag_index]
        if self.temp_dict[tag_autotag] is not None:
            data['autotag'] = self.temp_dict[tag_autotag]
        if self.temp_dict[tag_max_token] is not None:
            data['maxTokenPerUtt'] = self.temp_dict[tag_max_token]
        if self.temp_dict[tag_min_token] is not None:
            data['minTokenPerUtt'] = self.temp_dict[tag_min_token]
        if self.temp_dict[tag_exclude_utt] is not None:
            data['exclude_utt_without_entities'] = self.temp_dict[tag_exclude_utt]
        try:
            res = self.session.post(self.url + "search/" + "new", headers=self.headers, data=json.dumps(data))
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        return res.json()

    def delete(self, index: str) -> bool:
        """Delete data container"""

        if not isinstance(index, str):
            raise QtArgumentError("Argument type error: String is expected as index")
        try:
            res = self.session.delete(self.url + "search/" + index, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202, 204]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        return res.ok

    def progress(self, index: str = None) -> Dict:
        """Show progress for submitted data mining job"""

        url_path = "progress"
        if index is not None:
            if isinstance(index, str):
                url_path = url_path + "/" + index
            else:
                raise QtArgumentError("Expected string")
        try:
            res = self.session.get(self.url + "search/" + url_path, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        return res.json()

    def search(self, index: str, param_from: int = 0, size: int = None, f1: int = None, f2: int = None) -> Dict:
        """Search full-text and faceted search"""

        if not isinstance(index, str):
            raise QtArgumentError("Argument type error: String is expected as index")
        if isinstance(param_from, int):
            parameters = [('from', param_from)]
        else:
            raise QtArgumentError("Argument type error: Integer is expected as parameter")
        if size is not None:
            if isinstance(size, int) and 0 < size <= 200:
                parameters.append(('size', size))
            else:
                raise QtArgumentError("Argument type error: Integer between 0 and 200 is expected as parameter")
        if f1 is not None and f2 is not None:
            parameters.append(('f', f1))
            parameters.append(('f', f2))
        elif f1 is None and f2 is None:
            pass
        else:
            raise QtArgumentError("Argument error: Query filters must be used in pairs")
        try:
            res = self.session.get(self.url + "search/" + index, headers=self.headers, params=parameters)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        return res.json()

    def report_to_xlsx(self, index: str, path: str) -> bool:
        """Exporting in Excel format"""

        if not isinstance(index, str):
            raise QtArgumentError("Argument type error: String is expected as index")
        if not isinstance(path, str):
            raise QtArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QtArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".xlsx":
            raise QtFileTypeError("File type error: Please use xlsx extension saving file")
        try:
            res = self.session.get(self.url + "reports/" + index + "/xlsx", headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        with open(path, 'wb') as excel_file:
            excel_file.write(res.content)
        return res.ok

    def report_to_json(self, index: str, path: str) -> bool:
        """Exporting in Excel format"""

        if not isinstance(index, str):
            raise QtArgumentError("Argument type error: String is expected as index")
        if not isinstance(path, str):
            raise QtArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QtArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".json":
            raise QtFileTypeError("File type error: Please use json extension saving file")
        try:
            res = self.session.get(self.url + "reports/" + index + "/json", headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        with open(path, "w") as json_file:
            json.dump(res.json(), json_file)
        return res.ok
