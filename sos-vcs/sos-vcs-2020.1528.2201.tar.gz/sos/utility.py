#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xa1cac224

# Compiled with Coconut version 1.4.3-post_dev25 [Ernest Scribbler]

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_cached_module = _coconut_sys.modules.get("__coconut__")
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules["__coconut__"]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import *
from __coconut__ import _coconut, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_forward_dubstar_compose, _coconut_back_dubstar_compose, _coconut_pipe, _coconut_back_pipe, _coconut_star_pipe, _coconut_back_star_pipe, _coconut_dubstar_pipe, _coconut_back_dubstar_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_base_pattern_func, _coconut_addpattern, _coconut_sentinel, _coconut_assert, _coconut_mark_as_match
_coconut_sys.path.pop(0)

# Compiled Coconut: -----------------------------------------------------------

# Copyright (c) 2017-2020  Arne Bachmann
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import hashlib  # early time tracking  # line 4
import itertools  # early time tracking  # line 4
import logging  # early time tracking  # line 4
import os  # early time tracking  # line 4
import shutil  # early time tracking  # line 4
sys = _coconut_sys  # early time tracking  # line 4
import time  # early time tracking  # line 4
START_TIME = time.time()  # early time tracking  # line 4

if TYPE_CHECKING:  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Any  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import AnyStr  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Dict  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import FrozenSet  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Generic  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import IO  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Iterable  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Iterator  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import NoReturn  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import List  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Optional  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Sequence  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Set  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Tuple  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Type  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import TypeVar  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6
    from typing import Union  # we cannot delay this import, since we need to type-check the Coconut version-detection, which again is required to know if we actually can type-check...  # line 6

from sos import pure  # line 8
from sos.values import *  # line 9
from sos import usage  # line 10


# Lazy imports for quicker initialization TODO make mypy accept this
bz2 = None  # type: Any  # line 14
codecs = None  # type: Any  # line 14
difflib = None  # type: Any  # line 14
class bz2:  # line 15
    @_coconut_tco  # line 15
    def __getattribute__(_, key):  # line 15
        global bz2  # line 16
        import bz2  # line 16
        return _coconut_tail_call(bz2.__getattribute__, key)  # line 16
bz2 = bz2()  # type: object  # line 17

class codecs:  # line 19
    @_coconut_tco  # line 19
    def __getattribute__(_, key):  # line 19
        global codecs  # line 20
        import codecs  # line 20
        return _coconut_tail_call(codecs.__getattribute__, key)  # line 20
codecs = codecs()  # type: object  # line 21

class difflib:  # line 23
    @_coconut_tco  # line 23
    def __getattribute__(_, key):  # line 23
        global difflib  # line 24
        import difflib  # line 24
        return _coconut_tail_call(difflib.__getattribute__, key)  # line 24
difflib = difflib()  # type: object  # line 25


verbose = [None] if '--verbose' in sys.argv or '-v' in sys.argv else []  # type: List[None]  # line 28
debug_ = [None] if os.environ.get("DEBUG", "False").lower() == "true" or '--debug' in sys.argv else []  # type: List[None]  # line 29


# Classes
class Accessor(dict):  # line 33
    ''' Dictionary with attribute access. '''  # line 34
    def __init__(_, mapping: 'Dict[str, Any]'={}) -> 'None':  # line 35
        dict.__init__(_, mapping)  # line 35
    def __getattr__(_, k):  # from https://github.com/feluxe/sty/issues/17  # line 36
        try:  # was: dict.__getitem__  # line 37
            return _[k]  # was: dict.__getitem__  # line 37
        except KeyError:  # line 38
            raise AttributeError(k)  # line 38
    def __setattr__(_, k: 'str', v: 'Any') -> 'None':  # was: _[name] = value  # line 39
        try:  # line 40
            object.__getattribute__(_, k)  # line 40
        except AttributeError:  # line 41
            _[k] = v  # line 41
        else:  # line 42
            object.__setattr__(_, k, v)  # line 42
    @_coconut_tco  # line 43
    def __bool__(_) -> 'bool':  # line 43
        return _coconut_tail_call(bool, int(_[None]))  # line 43
    @_coconut_tco  # line 44
    def __str__(_) -> 'str':  # line 44
        return _coconut_tail_call(str, _[None])  # line 44
    def __add__(_, b: 'Any') -> 'str':  # line 45
        return _.value + b  # line 45

useColor = [None]  # type: List[_coconut.typing.Optional[bool]]  # line 47
def enableColor(enable: 'bool'=True, force: 'bool'=False):  # line 48
    ''' This piece of code only became necessary to enable enabling/disabling of the colored terminal output after initialization.
      enable: target state
      force: for testing only
  '''  # line 52
    if not force and (useColor[0] if enable else not useColor[0]):  # nothing to do since already set  # line 53
        return  # nothing to do since already set  # line 53
    MARKER.value = MARKER_COLOR if enable and sys.platform != "win32" else usage.MARKER_TEXT  # HINT because it doesn't work with the loggers yet  # line 54
    try:  # line 55
        if useColor[0] is None:  # very initial, do some monkey-patching  # line 56
            colorama.init(wrap=False)  # line 57
            sys.stdout = colorama.AnsiToWin32(sys.stdout).stream  # TODO replace by "better-exceptions" code  # line 58
            sys.stderr = colorama.AnsiToWin32(sys.stderr).stream  # line 59
    except:  # line 60
        pass  # line 60
    useColor[0] = enable  # line 61

# fallbacks in case there is no colorama library present
Fore = Accessor({k: "" for k in ["RESET", "BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "YELLOW", "WHITE"]})  # type: Dict[str, str]  # line 64
Style = Accessor({k: "" for k in ["NORMAL", "BRIGHT", "RESET_ALL"]})  # type: Dict[str, str]  # line 65
Back = Fore  # type: Dict[str, str]  # line 66
MARKER = Accessor({"value": usage.MARKER_TEXT})  # type: str  # assume default text-only  # line 67
try:  # line 68
    import colorama  # line 69
    import colorama.ansitowin32  # line 69
    if sys.stderr.isatty:  # list of ansi codes: http://bluesock.org/~willkg/dev/ansi.html  # line 70
        from colorama import Back  # line 71
        from colorama import Fore  # line 71
        from colorama import Style  # line 71
        MARKER_COLOR = Fore.WHITE + usage.MARKER_TEXT + Fore.RESET  # type: str  # line 72
        if sys.platform == "win32":  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 73
            Style.BRIGHT = ""  # sadly this would modify background color as well in the Windows console to make it appear brighter  # line 73
        enableColor()  # line 74
except:  # if library not installed, use fallback even for colored texts  # line 75
    MARKER_COLOR = usage.MARKER_TEXT  # if library not installed, use fallback even for colored texts  # line 75

if TYPE_CHECKING:  # available since coconut 1.3.1.21 (?)  # line 77
    Number = TypeVar("Number", int, float)  # line 78
    class Counter(Generic[Number]):  # line 79
        ''' A simple counter. Can be augmented to return the last value instead. '''  # line 80
        def __init__(_, initial: 'Number'=0) -> 'None':  # line 81
            _.value = initial  # type: Number  # line 81
        def inc(_, by: 'Number'=1) -> 'Number':  # line 82
            _.value += by  # line 82
            return _.value  # line 82
else:  # line 83
    class Counter:  # line 84
        def __init__(_, initial=0) -> 'None':  # line 85
            _.value = initial  # line 85
        def inc(_, by=1):  # line 86
            _.value += by  # line 86
            return _.value  # line 86

class ProgressIndicator(Counter):  # line 88
    ''' Manages a rotating progress indicator. '''  # line 89
    def __init__(_, symbols: 'str', callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None) -> 'None':  # line 90
        super(ProgressIndicator, _).__init__(-1)  # line 90
        _.symbols = symbols  # line 90
        _.timer = time.time()  # type: float  # line 90
        _.callback = callback  # type: Optional[_coconut.typing.Callable[[str], None]]  # line 90
    def getIndicator(_) -> '_coconut.typing.Optional[str]':  # line 91
        ''' Returns a value only if a certain time has passed. '''  # line 92
        newtime = time.time()  # type: float  # line 93
        if newtime - _.timer < .1:  # line 94
            return None  # line 94
        _.timer = newtime  # line 95
        sign = _.symbols[int(_.inc() % len(_.symbols))]  # type: str  # line 96
        if _.callback:  # line 97
            _.callback(sign)  # line 97
        return sign  # line 98

class Logger:  # line 100
    ''' Logger that supports joining many items. '''  # line 101
    def __init__(_, log) -> 'None':  # line 102
        _._log = log  # line 102
    def debug(_, *s):  # line 103
        _._log.debug(pure.sjoin(*s))  # line 103
    def info(_, *s):  # line 104
        _._log.info(pure.sjoin(*s))  # line 104
    def warn(_, *s):  # line 105
        _._log.warning(pure.sjoin(*s))  # line 105
    def error(_, *s):  # line 106
        _._log.error(pure.sjoin(*s))  # line 106


# Constants
_log = Logger(logging.getLogger(__name__))  # line 110
debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # line 110
ONLY_GLOBAL_FLAGS = ["strict", "track", "picky", "compress"]  # type: List[str]  # line 111
CONFIGURABLE_FLAGS = ["useChangesCommand", "useUnicodeFont", "useColorOutput"]  # type: List[str]  # line 112
CONFIGURABLE_LISTS = ["texttype", "bintype", "ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # line 113
CONFIGURABLE_INTS = ["logLines", "diffLines"]  # type: List[str]  # line 114
GLOBAL_LISTS = ["ignores", "ignoreDirs", "ignoresWhitelist", "ignoreDirsWhitelist"]  # type: List[str]  # lists that don't allow folders with their file patterns  # line 115
TRUTH_VALUES = ["true", "yes", "on", "1", "enable", "enabled"]  # type: List[str]  # all lower-case normalized  # line 116
FALSE_VALUES = ["false", "no", "off", "0", "disable", "disabled"]  # type: List[str]  # line 117
PROGRESS_MARKER = ["|/-\\", "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588\u2587\u2586\u2585\u2584\u2583\u2582", "\U0001f55b\U0001f550\U0001f551\U0001f552\U0001f553\U0001f554\U0001f555\U0001f556\U0001f557\U0001f558\U0001f559\U0001f55a\U0001f559\U0001f558\U0001f557\U0001f556\U0001f555\U0001f554\U0001f553\U0001f552\U0001f551\U0001f550"]  # type: List[str]  # line 118
BACKUP_SUFFIX = "_last"  # type: str  # line 119
metaFolder = ".sos"  # type: str  # line 120
DUMP_FILE = metaFolder + ".zip"  # type: str  # line 121
metaFile = ".meta"  # type: str  # line 122
metaBack = metaFile + BACKUP_SUFFIX  # type: str  # line 123
bufSize = pure.MEBI  # type: int  # line 124
UTF8 = "utf-8"  # type: str  # early used constant, not defined in standard library  # line 125
SVN = "svn"  # type: str  # line 126
SLASH = "/"  # type: str  # line 127
PARENT = ".."  # type: str  # line 128
DOT_SYMBOL = "\u00b7"  # type: str  # line 129
MULT_SYMBOL = "\u00d7"  # type: str  # line 130
CROSS_SYMBOL = "\u2716"  # type: str  # line 131
CHECKMARK_SYMBOL = "\u2714"  # type: str  # line 132
CHANGED_SYMBOL = "\u00b1"  # type: str  # alternative for "~"  # line 133
MOVED_SYMBOL = "\u21cc"  # type: str  # alternative for "#". or use \U0001F5C0", which is very unlikely to be in any console font  # line 134
ARROW_SYMBOL = "\u2799"  # type: str  # alternative for "*" in pointing to "this revision"  # line 135
METADATA_FORMAT = 2  # type: int  # counter for (partially incompatible) consecutive formats (was undefined, "1" is the first numbered format version after that)  # line 136
vcsFolders = {".svn": SVN, ".git": "git", ".bzr": "bzr", ".hg": "hg", ".fslckout": "fossil", "_FOSSIL_": "fossil", ".CVS": "cvs", "_darcs": "darcs", "_MTN": "monotone", ".git/GL_COMMIT_EDIT_MSG": "gl"}  # type: Dict[str, str]  # line 137
vcsBranches = {SVN: "trunk", "git": "master", "bzr": "trunk", "hg": "default", "fossil": None, "cvs": None, "darcs": None, "monotone": None}  # type: Dict[str, _coconut.typing.Optional[str]]  # line 138
vcsCommits = {SVN: (True, None), "git": (False, None), "bzr": (True, None), "hg": (True, None), "fossil": (True, "--no-warnings"), "cvs": (True, None), "darcs": (False, "--all"), "monotone": (False, None)}  # type: Dict[str, Tuple[bool, _coconut.typing.Optional[str]]]  # 2-tuple(is_tracked? (otherwise picky), str-arguments to "commit") TODO CVS, RCS have probably different per-file operation  # line 139
vcsNames = {SVN: "Subversion", "git": "Git", "bzr": "Bazaar", "hg": "Mercurial", "fossil": "Fossil", "cvs": "CVS", "darcs": "darcs", "monotone": "monotone"}  # type: Dict[str, str]  #  from cmd to long name  # line 140
NL_NAMES = {None: "<No newline>", b"\r\n": "<CR+LF>", b"\n\r": "<LF+CR>", b"\n": "<LF>", b"\r": "<CR>"}  # type: Dict[_coconut.typing.Optional[bytes], str]  # line 141
MAX_COMMAND_LINE = {"win32": 8191, "linux2": 4096, None: 1023}  # type: Dict[_coconut.typing.Optional[str], int]  # may be much longer on posix. https://stackoverflow.com/questions/3205027/maximum-length-of-command-line-string  # line 142
defaults = Accessor({"strict": False, "track": False, "picky": False, "compress": False, "useChangesCommand": False, "useUnicodeFont": sys.platform != "win32", "useColorOutput": True, "diffLines": 2, "logLines": 20, "texttype": ["*.md", "*.coco", "*.py", "*.pyi", "*.pth", "*.ps1", "*.bat"], "bintype": [], "ignoreDirs": [".*", "__pycache__", ".mypy_cache"], "ignoreDirsWhitelist": [], "ignores": ["__coconut__.py", "*.bak", "*.py[cdo]", "*.class", ".fslckout", "_FOSSIL_", "*%s" % DUMP_FILE] + ["~*"] if sys.platform == "win32" else [], "ignoresWhitelist": []})  # type: Accessor  # line 143
RETRY_NUM = 3  # type: int  # line 157
RETRY_WAIT = 1.5  # type: int  # line 158
CODEC_FUNCTIONS = ['utf_32_be', 'utf_32_le', 'utf_32', 'utf_16_be', 'utf_16_le', 'utf_16', 'utf_7', 'utf_8_sig', 'utf_8']  # type: List[str]  # line 159


# Functions
def printo(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 163
    color = useColor[0] and color or ""  # line 164
    reset = Fore.RESET if useColor[0] and color else ""  # line 165
    tryOrIgnore(lambda: sys.stdout.write(color + s + reset + nl) and False, lambda E: sys.stdout.buffer.write((s + nl).encode(sys.stdout.encoding, 'backslashreplace')) and False)  # PEP528 compatibility  # line 166
    sys.stdout.flush()  # PEP528 compatibility  # line 166

def printe(s: 'str'="", nl: 'str'="\n", color: '_coconut.typing.Optional[str]'=None):  # line 169
    color = useColor[0] and color or ""  # line 170
    reset = Fore.RESET if useColor[0] and color else ""  # line 171
    tryOrIgnore(lambda: sys.stderr.write(color + s + reset + nl) and False, lambda E: sys.stderr.buffer.write((s + nl).encode(sys.stderr.encoding, 'backslashreplace')) and False)  # line 172
    sys.stderr.flush()  # line 172

@_coconut_tco  # for py->os access of writing filenames  # PEP 529 compatibility  # line 175
def encode(s: 'str') -> 'bytes':  # for py->os access of writing filenames  # PEP 529 compatibility  # line 175
    return _coconut_tail_call(os.fsencode, s)  # for py->os access of writing filenames  # PEP 529 compatibility  # line 175

@_coconut_tco  # for os->py access of reading filenames  # line 177
def decode(b: 'bytes') -> 'str':  # for os->py access of reading filenames  # line 177
    return _coconut_tail_call(os.fsdecode, b)  # for os->py access of reading filenames  # line 177

def guessEncoding(binary: 'bytes') -> 'List[str]':  # line 179
    ''' If encoding cannot be determined automatically, attempt a guess. Usually it's not unambiguous, though.
  >>> print(guessEncoding(b"abcd0234"))
  ['ascii']
  >>> print(guessEncoding(bytes([0b00100100, 0b11000010, 0b10100010, 0b11100010, 0b10000010, 0b10101100, 0b11110000, 0b10011010, 0b10110011, 0b10011001])))  # utf_8  1:$ 2:cent 3:€, 4:? -> gives 5 options, but it's UTF-8
  ['utf_16_be', 'utf_16_le', 'utf_8']
  >>> print(guessEncoding(bytes([0b00000000, 0b00100100, 0b11011000, 0b01010010, 0b11011111, 0b01100010])))  # utf_16 $ ? -> gives 3 options, on is correct
  ['utf_16_be', 'utf_16_le']
  >>> print(guessEncoding(bytes([0b00100100, 0b11000010, 0b10100010])))  # utf_8  1:$ 2:cent 3:€, 4:? -> gives 2 UTF-8 options
  ['utf_8']
  '''  # line 189
    if all((bite < 128 for bite in binary)):  # TODO move as first detection step  # line 190
        return ["ascii"]  # TODO move as first detection step  # line 190
    decoded = list(filter(lambda _=None: tryOrDefault(lambda: codecs.encode(codecs.decode(binary, _), _) == binary, None), CODEC_FUNCTIONS))  # type: List[str]  # line 191
    if (len(binary) >> 1) << 1 != len(binary):  # only utf-8 variants possible here  # line 192
        decoded[:] = list(filter(lambda _=None: "8" in _, decoded))  # only utf-8 variants possible here  # line 192
    return decoded  # line 193

# Optional dependency: https://github.com/chardet/chardet
try:  # line 196
    import chardet  # line 197
    def detectEncoding(binary: 'bytes') -> '_coconut.typing.Optional[str]':  # returns None if nothing useful detected  # line 198
        return chardet.detect(binary)["encoding"]  # returns None if nothing useful detected  # line 198
except:  # line 199
    def detectEncoding(binary: 'bytes') -> '_coconut.typing.Optional[str]':  # line 200
        ''' Fallback function definition if no chardet library installed. '''  # line 201
        encodings = guessEncoding(binary)  # type: List[str]  # line 202
        if len(encodings) == 1:  # line 203
            return encodings[0]  # line 203
        if len(encodings) == 0:  # or cp1252 or cp850  # line 204
            return None  # or cp1252 or cp850  # line 204
        return encodings[-1]  # line 205

def tryOrDefault(func: 'Callable[[], Any]', default: 'Any') -> 'Any':  # line 207
    try:  # line 208
        return func()  # line 208
    except:  # line 209
        return default  # line 209

def tryOrIgnore(func: 'Callable[[], Any]', onError: 'Callable[[Exception], None]'=lambda e: None) -> 'Any':  # line 211
    try:  # line 212
        return func()  # line 212
    except Exception as E:  # line 213
        onError(E)  # line 213

def removePath(key: 'str', value: 'str') -> 'str':  # line 215
    ''' Cleanup of user-specified *global* file patterns, used in config. '''  # line 216
    return value if value in GLOBAL_LISTS or SLASH not in value else value[value.rindex(SLASH) + 1:]  # line 217

def dictUpdate(dikt: 'Dict[Any, Any]', by: 'Dict[Any, Any]') -> 'Dict[Any, Any]':  # line 219
    ''' Updates a dictionary by another one, returning a new copy without touching any of the passed dictionaries. '''  # line 220
    d = dict(dikt)  # type: Dict[Any, Any]  # line 221
    d.update(by)  # line 221
    return d  # line 221

def openIt(file: 'str', mode: 'str', compress: 'bool'=False) -> 'IO[bytes]':  # line 223
    ''' Abstraction for opening both compressed and plain files. '''  # line 224
    return bz2.BZ2File(encode(file), mode) if compress else open(encode(file), mode + "b")  # line 225

def eoldet(file: 'bytes') -> '_coconut.typing.Optional[bytes]':  # line 227
    ''' Determine EOL style from a binary string. '''  # line 228
    lf = file.count(b"\n")  # type: int  # line 229
    cr = file.count(b"\r")  # type: int  # line 230
    crlf = file.count(b"\r\n")  # type: int  # line 231
    if crlf > 0:  # DOS/Windows/Symbian etc.  # line 232
        if lf != crlf or cr != crlf:  # line 233
            warn("Inconsistent CR/NL count with CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 233
        return b"\r\n"  # line 234
    if lf != 0 and cr != 0:  # line 235
        warn("Inconsistent CR/NL count without CR+NL. Mixed EOL style detected, may cause problems during merge")  # line 235
    if lf > cr:  # Linux/Unix  # line 236
        return b"\n"  # Linux/Unix  # line 236
    if cr > lf:  # older 8-bit machines  # line 237
        return b"\r"  # older 8-bit machines  # line 237
    return None  # no new line contained, cannot determine  # line 238

if TYPE_CHECKING:  # line 240
    def safeSplit(s: 'AnyStr', d: '_coconut.typing.Optional[AnyStr]'=None) -> 'List[AnyStr]':  # line 241
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 241
else:  # line 242
    def safeSplit(s, d=None):  # line 243
        return s.split((("\n" if isinstance(s, str) else b"\n") if d is None else d)) if len(s) > 0 else []  # line 243

@_coconut_tco  # line 245
def hashStr(datas: 'str') -> 'str':  # line 245
    return _coconut_tail_call(hashlib.sha256(datas.encode(UTF8)).hexdigest)  # line 245

def modified(changes: 'ChangeSet', onlyBinary: 'bool'=False) -> 'bool':  # line 247
    return len(changes.additions) > 0 or len(changes.deletions) > 0 or len(changes.modifications) > 0 or len(changes.moves) > 0  # line 247

def listindex(lizt: 'Sequence[Any]', what: 'Any', index: 'int'=0) -> 'int':  # line 249
    return lizt[index:].index(what) + index  # line 249

def branchFolder(branch: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 251
    return os.path.join((os.getcwd() if base is None else base), metaFolder, "b%d" % branch) + ((os.sep + file) if file else "")  # line 251

def revisionFolder(branch: 'int', revision: 'int', base: '_coconut.typing.Optional[str]'=None, file: '_coconut.typing.Optional[str]'=None) -> 'str':  # line 253
    return os.path.join(branchFolder(branch, base), "r%d" % revision) + ((os.sep + file) if file else "")  # line 253

def Exit(message: 'str'="", code: 'int'=1, excp: 'Any'=None):  # line 255
    if not '--quiet' in sys.argv:  # line 256
        lines = (message + ("" if excp is None else ("\n" + exception(excp)))).replace("\r", "\n").split("\n")  # type: List[str]  # line 257
        printe("[", nl="")  # line 258
        printe("EXIT", color=Fore.YELLOW if code else Fore.GREEN, nl="")  # line 259
        printe("%s%s]" % (" %.1fs" % (time.time() - START_TIME) if verbose else "", (" " + lines[0] + ".") if lines[0] != "" else ""))  # line 260
        if len(lines) > 1:  # line 261
            printe("\n".join(lines[1:]))  # line 264
    if '--wait' in sys.argv:  # line 265
        input("Hit Enter to finish." if not '--quiet' in sys.argv else "")  # line 265
    sys.exit(code)  # line 266

def fitStrings(strings: '_coconut.typing.Sequence[str]', prefix: 'str', length: 'int'=MAX_COMMAND_LINE.get(sys.platform, MAX_COMMAND_LINE[None]), separator: 'str'=" ", process: '_coconut.typing.Callable[..., str]'=lambda _=None: '"%s"' % _) -> 'str':  # line 268
    ''' Returns a packed string, destructively consuming entries from the provided list. Does similar as xargs. getconf ARG_MAX or xargs --show-limits. '''  # line 269
    if len(prefix + separator + ((process)(strings[0]))) > length:  # line 270
        raise Exception("Cannot possibly strings pack into specified length")  # line 270
    while len(strings) > 0 and len(prefix + separator + ((process)(strings[0]))) <= length:  # line 271
        prefix += separator + ((process)(strings.pop(0)))  # line 271
    return prefix  # line 272

def exception(E) -> 'str':  # line 274
    ''' Report an exception to the user to allow useful bug reporting. '''  # line 275
    import traceback  # line 276
    return str(E) + "\n" + traceback.format_exc() + "\n" + "".join(traceback.format_list(traceback.extract_stack()))  # line 277

def hashFile(path: 'str', compress: 'bool', saveTo: 'List[str]'=[], callback: 'Optional[_coconut.typing.Callable[[str], None]]'=None, symbols: 'str'=PROGRESS_MARKER[0]) -> 'Tuple[str, int]':  # line 279
    ''' Calculate and return (hash of file contents, compressed sized (if writing) else 0). '''  # line 280
    indicator = ProgressIndicator(symbols, callback) if callback else None  # type: _coconut.typing.Optional[ProgressIndicator]  # line 281
    _hash = hashlib.sha256()  # line 282
    wsize = 0  # type: int  # line 283
    if saveTo and os.path.exists(encode(saveTo[0])):  # line 284
        Exit("Hash collision detected. Leaving repository in inconsistent state", 1)  # HINT this exits immediately  # line 285
    to = openIt(saveTo[0], "w", compress) if saveTo else None  # line 286
    retry = RETRY_NUM  # type: int  # line 287
    while True:  # line 288
        try:  # line 289
            with open(encode(path), "rb") as fd:  # line 290
                while True:  # line 291
                    buffer = fd.read(bufSize)  # type: bytes  # line 292
                    _hash.update(buffer)  # line 293
                    if to:  # line 294
                        to.write(buffer)  # line 294
                    if len(buffer) < bufSize:  # line 295
                        break  # line 295
                    if indicator:  # line 296
                        indicator.getIndicator()  # line 296
                if to:  # line 297
                    to.close()  # line 298
                    wsize = os.stat(encode(saveTo[0])).st_size  # line 299
                    for remote in saveTo[1:]:  # line 300
                        tryOrDefault(lambda: shutil.copy2(encode(saveTo[0]), encode(remote)), lambda e: error("Error creating remote copy %r" % remote))  # line 300
            break  # line 301
        except Exception as E:  # (IsADirectoryError, PermissionError)  # line 302
            retry -= 1  # line 303
            if retry == 0:  # line 304
                raise E  # line 304
            error("Cannot open %r - retrying %d more times in %.1d seconds" % (path, retry, RETRY_WAIT))  # line 305
            time.sleep(RETRY_WAIT)  # line 306
    return (_hash.hexdigest(), wsize)  # line 307

def getAnyOfMap(map: 'Dict[str, Any]', params: '_coconut.typing.Sequence[str]', default: 'Any'=None) -> 'Any':  # line 309
    ''' Utility to find any entries of a dictionary in a list to return the dictionaries value. '''  # line 310
    for k, v in map.items():  # line 311
        if k in params:  # line 311
            return v  # line 311
    return default  # line 312

@_coconut_tco  # line 314
def strftime(timestamp: '_coconut.typing.Optional[int]'=None) -> 'str':  # line 314
    return _coconut_tail_call(time.strftime, "%Y-%m-%d %H:%M:%S", time.localtime(timestamp / 1000. if timestamp is not None else None))  # line 314

def detectAndLoad(filename: '_coconut.typing.Optional[str]'=None, content: '_coconut.typing.Optional[bytes]'=None, ignoreWhitespace: 'bool'=False) -> 'Tuple[str, _coconut.typing.Optional[bytes], _coconut.typing.Sequence[str]]':  # line 316
    ''' Detects a (text) file's encoding, detects the end of line markers, loads the file and splits it into lines.
      returns: 3-tuple (encoding-string, end-of-line bytes, [lines])
  '''  # line 319
    lines = []  # type: List[str]  # line 320
    if filename is not None:  # line 321
        with open(encode(filename), "rb") as fd:  # line 321
            content = fd.read()  # line 321
    encoding = (lambda _coconut_none_coalesce_item: sys.getdefaultencoding() if _coconut_none_coalesce_item is None else _coconut_none_coalesce_item)(detectEncoding(content))  # type: str  # line 322
    eol = eoldet(content)  # type: _coconut.typing.Optional[bytes]  # line 323
    if filename is not None:  # line 324
        with codecs.open(encode(filename), encoding=encoding) as fd2:  # line 324
            lines = safeSplit(fd2.read(), ((b"\n" if eol is None else eol)).decode(encoding))  # line 324
    elif content is not None:  # line 325
        lines = safeSplit(content.decode(encoding), ((b"\n" if eol is None else eol)).decode(encoding))  # line 325
    else:  # line 326
        return (sys.getdefaultencoding(), b"\n", [])  # line 326
    if ignoreWhitespace:  # line 327
        lines[:] = [line.replace("\t", "  ").strip() for line in lines]  # line 327
    return (encoding, eol, lines)  # line 328

if TYPE_CHECKING:  # line 330
    DataType = TypeVar("DataType", BranchInfo, ChangeSet, MergeBlock, PathInfo)  # line 331
    @_coconut_tco  # line 332
    def dataCopy(_tipe: 'Type[DataType]', _old: 'DataType', *_args, byValue: 'bool'=False, **_kwargs) -> 'DataType':  # line 332
        ''' A better makedata() version. '''  # line 333
        r = _old._asdict()  # type: Dict[str, Any]  # line 334
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 335
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 336
else:  # line 337
    @_coconut_tco  # line 338
    def dataCopy(_tipe, _old, *_args, byValue=False, **_kwargs) -> 'DataType':  # line 338
        ''' A better makedata() version. '''  # line 339
        r = _old._asdict()  # line 340
        r.update({k: ([e for e in v] if byValue and isinstance(v, (list, tuple, set)) else v) for k, v in _kwargs.items()})  # copy by value if required  # line 341
        return _coconut_tail_call(makedata, _tipe, *(list(_args) + [r[field] for field in _old._fields]))  # TODO also offer copy-by-value here  # line 342

def detectMoves(changes: 'ChangeSet', strict: 'bool') -> 'Dict[str, Tuple[str, PathInfo]]':  # line 344
    ''' Compute renames/removes for a changeset, returning new targetpath -> (old source path, new info). '''  # line 345
    moves = {}  # type: Dict[str, Tuple[str, PathInfo]]  # line 346
    for path, info in changes.additions.items():  # line 347
        for dpath, dinfo in changes.deletions.items():  # line 347
            if info.size == dinfo.size and ((info.hash == dinfo.hash) if strict else (info.mtime == dinfo.mtime)):  # was moved  # line 348
                if dpath not in moves or path.split(SLASH)[-1] == dpath.split(SLASH)[-1]:  # only override previously stored arbitrary move, when name match perfectly this time TODO compare even more parent folders when matching  # line 349
                    moves[dpath] = (path, info)  # store new data and original name, but don't remove add/del  # line 350
                break  # deletions loop, continue with next addition  # line 351
    return {path: (dpath, info) for dpath, (path, info) in moves.items()}  # sort by target (by moved-to)  # line 352

def user_input(text: 'str', choices: 'Iterable[str]', default: 'str'=None, selection: 'str'="") -> 'str':  # line 354
    ''' Default can be a selection from choice and allows empty input. '''  # line 355
    while True:  # line 356
        selection = input(text).strip().lower()  # line 357
        if selection != "" and selection in choices:  # line 358
            break  # line 358
        if selection == "" and default is not None:  # line 359
            selection = default  # line 359
            break  # line 359
    return selection  # line 360

def user_block_input(output: 'List[str]'):  # line 362
    ''' Side-effect appending to input list. '''  # line 363
    sep = input("Enter end-of-text marker (default: <empty line>: ")  # type: str  # line 364
    line = sep  # type: str  # line 364
    while True:  # line 365
        line = input("> ")  # line 366
        if line == sep:  # line 367
            break  # line 367
        output.append(line)  # writes to caller-provided list reference  # line 368

def mergeClassic(file: 'bytes', intofile: 'str', fromname: 'str', intoname: 'str', totimestamp: 'int', context: 'int', ignoreWhitespace: 'bool'=False):  # line 370
    encoding = None  # type: str  # typing  # line 371
    othreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 371
    othr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 371
    curreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 371
    curr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 371
    try:  # line 372
        encoding, othreol, othr = detectAndLoad(content=file, ignoreWhitespace=ignoreWhitespace)  # line 373
        encoding, curreol, curr = detectAndLoad(filename=intofile, ignoreWhitespace=ignoreWhitespace)  # line 374
    except Exception as E:  # in case of binary files  # line 375
        Exit("Cannot diff '%s' vs '%s': %r" % (("<bytes>" if fromname is None else fromname), ("<bytes>" if intoname is None else intoname)), excp=E)  # in case of binary files  # line 375
    for line in difflib.context_diff(othr, curr, fromname, intoname, time.ctime(int(totimestamp / 1000))):  # from generator expression  # line 376
        printo(line)  # from generator expression  # line 376

def merge(file: '_coconut.typing.Optional[bytes]'=None, into: '_coconut.typing.Optional[bytes]'=None, filename: '_coconut.typing.Optional[str]'=None, intoname: '_coconut.typing.Optional[str]'=None, mergeOperation: 'MergeOperation'=MergeOperation.BOTH, charMergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False, eol: 'bool'=False, ignoreWhitespace: 'bool'=False) -> 'Tuple[Union[bytes, List[MergeBlock]], _coconut.typing.Optional[bytes]]':  # line 378
    ''' Merges other binary text contents in 'file' (or reads from file 'filename') into current text contents 'into' (or reads from file 'intoname'), returning merged result.
      For 'sos update', the other version is assumed to be the "new/added" one, while for diff, the 'file' with changes is the one shown as "added".
      However, change direction markers are insert ("+") for elements only in into, and remove ("-") for elements only in other file (just like the diff marks +/-)
      diffOnly: if True, return detected change blocks only, don't perform the actual text merging
      eol: if True, will use the other file's EOL marks instead of current file's
      in case of a replace block and INSERT strategy, the change will be added **behind** the original. HINT this could be made configurable
  '''  # line 393
    encoding = None  # type: str  # typing  # line 394
    othreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 394
    othr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 394
    curreol = None  # type: _coconut.typing.Optional[bytes]  # typing  # line 394
    curr = None  # type: _coconut.typing.Sequence[str]  # typing  # line 394
    try:  # load files line-wise and normalize line endings (keep the one of the current file) TODO document  # line 395
        encoding, othreol, othr = detectAndLoad(filename=filename, content=file, ignoreWhitespace=ignoreWhitespace)  # line 396
        encoding, curreol, curr = detectAndLoad(filename=intoname, content=into, ignoreWhitespace=ignoreWhitespace)  # line 397
    except Exception as E:  # line 398
        Exit("Cannot merge '%s' into '%s': %r" % (("<bytes>" if filename is None else filename), ("<bytes>" if intoname is None else intoname)), excp=E)  # line 398
    if None not in (othreol, curreol) and othreol != curreol:  # line 399
        warn("Differing EOL-styles detected during merge. Using current file's style for merged output")  # line 399
    output = difflib.Differ().compare(othr, curr)  # type: Union[Iterable[str], List[str]]  # line 400
    blocks = []  # type: List[MergeBlock]  # merged result in blocks  # line 401
    tmp = []  # type: List[str]  # block of consecutive lines  # line 402
    last = " "  # type: str  # "into"-file offset for remark lines  # line 403
    no = None  # type: int  # "into"-file offset for remark lines  # line 403
    line = None  # type: str  # "into"-file offset for remark lines  # line 403
    offset = 0  # type: int  # "into"-file offset for remark lines  # line 403

    for no, line in pure.appendEndmarkerIterator(enumerate(output), endValue="X"):  # EOF marker (difflib's output will never be "X" alone)  # line 405
        if line[0] == last:  # continue filling current block, no matter what type of block it is  # line 406
            tmp.append(line[2:])  # continue filling current block, no matter what type of block it is  # line 406
            continue  # continue filling current block, no matter what type of block it is  # line 406
        if line == "X" and len(tmp) == 0:  # break if nothing left to do, otherwise perform operation for stored block  # line 407
            break  # break if nothing left to do, otherwise perform operation for stored block  # line 407
        if last == " " and len(tmp) > 0:  # same in both files. avoid adding empty keep block  # line 408
            blocks.append(MergeBlock(MergeBlockType.KEEP, [line for line in tmp], line=no - offset - len(tmp)))  # same in both files. avoid adding empty keep block  # line 408
        elif last == "-":  # may be a pure deletion or part of a replacement (with previous or next block being "+")  # line 409
            blocks.append(MergeBlock(MergeBlockType.REMOVE, [line for line in tmp], line=no - offset - len(tmp)))  # line 410
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.INSERT:  # is a +/- replacement  # line 411
                offset += len(blocks[-2].lines)  # line 412
                blocks[-2] = dataCopy(MergeBlock, blocks[-1], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-2], line=blocks[-1].line))  # remember replaced stuff with reference to insert merge block TODO why -1 necessary?  # line 413
                blocks.pop()  # line 414
        elif last == "+":  # may be a pure insertion or part of a replacement (with previous or next block being "-")  # line 415
            blocks.append(MergeBlock(MergeBlockType.INSERT, [line for line in tmp], line=no - offset - len(tmp)))  # line 416
            if len(blocks) >= 2 and blocks[-2].tipe == MergeBlockType.REMOVE:  #  and len(blocks[-1].lines) == len(blocks[-2].lines):  # requires previous block and same number of lines TODO allow multiple intra-line merge for same-length blocks  # line 417
                offset += len(blocks[-1].lines)  # line 418
                blocks[-2] = dataCopy(MergeBlock, blocks[-2], tipe=MergeBlockType.REPLACE, replaces=dataCopy(MergeBlock, blocks[-1], line=blocks[-2].line))  # remember replaced stuff with reference to other merge block TODO why -1 necessary?  # line 419
                blocks.pop()  # remove TOS due to merging two blocks into replace or modify  # line 420
        elif last == "?":  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 421
            offset += 1  # marker for intra-line change comment HINT was earlier part of the MergeBlock  # line 421
        last = line[0]  # remember for comparison once next block comes around  # line 422
        tmp[:] = [line[2:]]  # only remember current line as fresh next block  # line 423
# TODO add code to detect and mark moved blocks here
    nl = othreol if eol else ((othreol if curreol is None else curreol))  # type: bytes  # no default newline, to mark "no newline"  # line 425
    debug("Diff blocks: " + repr(blocks))  # line 426
    if diffOnly:  # line 427
        return (blocks, nl)  # line 427

# now perform merge operations depending on detected blocks and selected merge options
    output = []  # clean list of strings  # line 430
    add_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 430
    del_all = None  # type: _coconut.typing.Optional[str]  # clean list of strings  # line 430
    selection = ""  # type: str  # clean list of strings  # line 430
    for block in blocks:  # line 431
        if block.tipe == MergeBlockType.KEEP:  # line 432
            output.extend(block.lines)  # line 432
        elif (block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value)) or (block.tipe == MergeBlockType.REMOVE and (mergeOperation.value & MergeOperation.INSERT.value)):  # will add line despite remove if --add-line was selected  # line 433
            output.extend(block.lines)  # line 435
        elif block.tipe == MergeBlockType.REPLACE:  # complete block replacement  # line 436
            if len(block.lines) == len(block.replaces.lines) == 1:  # both sides are one-liners: apply next sub-level merge  # line 437
                output.append(lineMerge(block.lines[0], block.replaces.lines[0], mergeOperation=charMergeOperation))  # line 438
            elif mergeOperation == MergeOperation.ASK:  # more than one line: needs user input  # line 439
#      if mergeOperation == MergeOperation.ASK:  # more than one line: needs user input
                printo(pure.ajoin("- ", block.lines, nl="\n"))  # TODO check +/- in update mode, could be swapped  # line 441
                printo(pure.ajoin("+ ", block.replaces.lines, nl="\n"))  # line 442
                while True:  # line 443
                    op = input(" Line replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ").strip().lower()[:1]  # type: str  # line 444
                    if op in "tb":  # order for both determined here - TODO make configurable  # line 445
                        output.extend(block.lines)  # order for both determined here - TODO make configurable  # line 445
                    if op in "ib":  # line 446
                        output.extend(block.replaces.lines)  # line 446
                    if op == "u":  # line 447
                        user_block_input(output)  # line 447
                    if op in "tbiu":  # was valid user input  # line 448
                        break  # was valid user input  # line 448
            else:  # more than one line and not ask  # line 449
                if mergeOperation == MergeOperation.REMOVE:  # line 450
                    pass  # line 450
                elif mergeOperation == MergeOperation.BOTH:  # line 451
                    output.extend(block.lines)  # line 451
                elif mergeOperation == MergeOperation.INSERT:  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 452
                    output.extend(list(block.replaces.lines) + list(block.lines))  # TODO optionally allow insertion BEFORE or AFTER original (order of these both lines)  # line 452
        elif block.tipe in (MergeBlockType.INSERT, MergeBlockType.REMOVE) and mergeOperation == MergeOperation.ASK:  # user - interactive insert/remove section  # line 453
            if (block.tipe == MergeBlockType.INSERT and add_all is None) or (block.tipe == MergeOperation.REMOVE and del_all is None):  # condition for asking  # line 454
                selection = user_input(pure.ajoin("+ " if block.tipe == MergeBlockType.INSERT else "- ", block.lines) + "\n  Accept? *[Y]es, [N]o, yes to [A]ll %s, n[O] to all: " % "insertions" if block.tipe == MergeBlockType.INSERT else "deletions", "ynao", "y")  # line 456
                if selection in "ao":  # line 457
                    if block.tipe == MergeBlockType.INSERT:  # line 458
                        add_all = "y" if selection == "a" else "n"  # line 458
                        selection = add_all  # line 458
                    else:  # REMOVE case  # line 459
                        del_all = "y" if selection == "a" else "n"  # REMOVE case  # line 459
                        selection = del_all  # REMOVE case  # line 459
            if (block.tipe == MergeBlockType.INSERT and "y" in (add_all, selection)) or ("n" in (del_all, selection)):  # REMOVE case  # line 460
                output.extend(block.lines)  # line 462
    debug("Merge output: " + "\n".join(output))  # line 463
    return (((b"\n" if nl is None else nl)).join([line.encode(encoding) for line in output]), nl)  # returning bytes  # line 464
# TODO handle check for more/less lines in found -/+ blocks to find common section and splitting prefix/suffix out

@_coconut_tco  # line 467
def lineMerge(othr: 'str', into: 'str', mergeOperation: 'MergeOperation'=MergeOperation.BOTH, diffOnly: 'bool'=False) -> 'Union[str, List[MergeBlock]]':  # line 467
    ''' Merges string 'othr' into current string 'into'.
      change direction mark is insert for elements only in into, and remove for elements only in file (according to diff marks +/-)
      returns: merged line
      raises: Exception in case of unparseable marker
  '''  # line 472
    out = list(difflib.Differ().compare(othr, into))  # type: List[str]  # line 473
    blocks = []  # type: List[MergeBlock]  # line 474
    for i, charline in enumerate(out):  # line 475
        if charline[0] == "+":  # line 476
            if i + 1 < len(out) and out[i + 1][0] == "+":  # look-ahead: block will continue  # line 477
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # middle of + block  # line 478
                    blocks[-1].lines.append(charline[2])  # add one more character to the accumulating list  # line 479
                else:  # first + in block  # line 480
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [charline[2]], i))  # line 481
            else:  # last charline of + block  # line 482
                if i > 0 and blocks[-1].tipe == MergeBlockType.INSERT:  # end of a block  # line 483
                    blocks[-1].lines.append(charline[2])  # line 484
                else:  # single charline  # line 485
                    blocks.append(MergeBlock(MergeBlockType.INSERT, [charline[2]], i))  # line 486
                if i >= 1 and blocks[-2].tipe == MergeBlockType.REMOVE:  # previous - and now last in + block creates a replacement block  # line 487
                    blocks[-2] = MergeBlock(MergeBlockType.REPLACE, blocks[-2].lines, i, replaces=blocks[-1])  # line 488
                    blocks.pop()  # line 488
        elif charline[0] == "-":  # line 489
            if i > 0 and blocks[-1].tipe == MergeBlockType.REMOVE:  # part of - block  # line 490
                blocks[-1].lines.append(charline[2])  # line 491
            else:  # first in block  # line 492
                blocks.append(MergeBlock(MergeBlockType.REMOVE, [charline[2]], i))  # line 493
        elif charline[0] == " ":  # keep area  # line 494
            if i > 0 and blocks[-1].tipe == MergeBlockType.KEEP:  # part of block  # line 495
                blocks[-1].lines.append(charline[2])  # line 496
            else:  # first in block  # line 497
                blocks.append(MergeBlock(MergeBlockType.KEEP, [charline[2]], i))  # line 498
        else:  # line 499
            raise Exception("Cannot parse diff charline %r" % charline)  # line 499
    blocks[:] = [dataCopy(MergeBlock, block, lines=["".join(block.lines)], replaces=dataCopy(MergeBlock, block.replaces, lines=["".join(block.replaces.lines)]) if block.replaces else None) for block in blocks]  # update blocks  # line 500
    if diffOnly:  # debug interrupt - only return blocks  # line 501
        return blocks  # debug interrupt - only return blocks  # line 501

    out = []  # line 503
    for i, block in enumerate(blocks):  # line 504
        if block.tipe == MergeBlockType.KEEP:  # line 505
            out.extend(block.lines)  # line 505
        elif block.tipe == MergeBlockType.REPLACE:  # line 506
            if mergeOperation == MergeOperation.ASK:  # TODO add loop here like in merge  # line 507
                printo(pure.ajoin("- ", othr))  # line 508
                printo("- " + (" " * i) + block.replaces.lines[0])  # line 509
                printo("+ " + (" " * i) + block.lines[0])  # line 510
                printo(pure.ajoin("+ ", into))  # line 511
                op = user_input(" Character replacement: *M[I]ne (+), [T]heirs (-), [B]oth, [U]ser input: ", "tbim")  # type: str  # line 512
                if op in "tb":  # line 513
                    out.extend(block.lines)  # line 513
                    break  # line 513
                if op in "ib":  # line 514
                    out.extend(block.replaces.lines)  # line 514
                    break  # line 514
                if op == "m":  # line 515
                    user_block_input(out)  # line 515
                    break  # line 515
            else:  # non-interactive  # line 516
                if mergeOperation == MergeOperation.REMOVE:  # neither keep old nor insert new  # line 517
                    pass  # neither keep old nor insert new  # line 517
                elif mergeOperation == MergeOperation.BOTH:  # remove old and insert new  # line 518
                    out.extend(block.lines)  # remove old and insert new  # line 518
                elif mergeOperation == MergeOperation.INSERT:  # keep old an insert new  # line 519
                    out.extend(block.replaces.lines + block.lines)  # keep old an insert new  # line 519
        elif block.tipe == MergeBlockType.INSERT and not (mergeOperation.value & MergeOperation.REMOVE.value):  # line 520
            out.extend(block.lines)  # line 520
        elif block.tipe == MergeBlockType.REMOVE and mergeOperation.value & MergeOperation.INSERT.value:  # line 521
            out.extend(block.lines)  # line 521
# TODO ask for insert or remove as well
    return _coconut_tail_call("".join, out)  # line 523

def findSosVcsBase() -> 'Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str], _coconut.typing.Optional[str]]':  # line 525
    ''' Attempts to find sos and legacy VCS base folders.
      Returns (SOS-repo root, VCS-repo root, VCS command)
  '''  # line 528
    debug("Detecting root folders...")  # line 529
    path = os.getcwd()  # type: str  # start in current folder, check parent until found or stopped  # line 530
    vcs = (None, None)  # type: Tuple[_coconut.typing.Optional[str], _coconut.typing.Optional[str]]  # line 531
    while not os.path.exists(encode(os.path.join(path, metaFolder))):  # line 532
        contents = set(os.listdir(path))  # type: Set[str]  # line 533
        vcss = [executable for folder, executable in vcsFolders.items() if folder in contents or (SLASH in folder and os.path.exists(os.path.join(os.getcwd(), folder.replace(SLASH, os.sep))))]  # type: _coconut.typing.Sequence[str]  # determine VCS type from existence of dot folder TODO use encode?  # line 534
        choice = None  # type: _coconut.typing.Optional[str]  # line 535
        if len(vcss) > 1:  # line 536
            choice = SVN if SVN in vcss else vcss[0]  # SVN is preferred  # line 537
            warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 538
        elif len(vcss) > 0:  # line 539
            choice = vcss[0]  # line 539
        if not vcs[0] and choice:  # memorize current repo root  # line 540
            vcs = (path, choice)  # memorize current repo root  # line 540
        new = os.path.dirname(path)  # get parent path  # line 541
        if new == path:  # avoid infinite loop  # line 542
            break  # avoid infinite loop  # line 542
        path = new  # line 543
    if os.path.exists(encode(os.path.join(path, metaFolder))):  # found something  # line 544
        if vcs[0]:  # already detected vcs base and command  # line 545
            return (path, vcs[0], vcs[1])  # already detected vcs base and command  # line 545
        sos = path  # line 546
        while True:  # continue search for VCS base  # line 547
            contents = set(os.listdir(path))  # line 548
            vcss = [executable for folder, executable in vcsFolders.items() if folder in contents]  # determine VCS type  # line 549
            choice = None  # line 550
            if len(vcss) > 1:  # line 551
                choice = SVN if SVN in vcss else vcss[0]  # line 552
                warn("Detected more than one parallel VCS checkouts %r. Falling back to '%s'" % (vcss, choice))  # line 553
            elif len(vcss) > 0:  # line 554
                choice = vcss[0]  # line 554
            if choice:  # line 555
                return (sos, path, choice)  # line 555
            new = os.path.dirname(path)  # get parent path  # line 556
            if new == path:  # no VCS folder found  # line 557
                return (sos, None, None)  # no VCS folder found  # line 557
            path = new  # line 558
    return (None, vcs[0], vcs[1])  # line 559

def tokenizeGlobPattern(pattern: 'str') -> 'List[GlobBlock]':  # line 561
    index = 0  # type: int  # line 562
    out = []  # type: List[GlobBlock]  # literal = True, first index  # line 563
    while index < len(pattern):  # line 564
        if pattern[index:index + 3] in ("[?]", "[*]", "[[]", "[]]"):  # line 565
            out.append(GlobBlock(False, pattern[index:index + 3], index))  # line 565
            continue  # line 565
        if pattern[index] in "*?":  # line 566
            count = 1  # type: int  # line 567
            while index + count < len(pattern) and pattern[index] == "?" and pattern[index + count] == "?":  # line 568
                count += 1  # line 568
            out.append(GlobBlock(False, pattern[index:index + count], index))  # line 569
            index += count  # line 569
            continue  # line 569
        if pattern[index:index + 2] == "[!":  # line 570
            out.append(GlobBlock(False, pattern[index:pattern.index("]", index + 2) + 1], index))  # line 570
            index += len(out[-1][1])  # line 570
            continue  # line 570
        count = 1  # line 571
        while index + count < len(pattern) and pattern[index + count] not in "*?[":  # line 572
            count += 1  # line 572
        out.append(GlobBlock(True, pattern[index:index + count], index))  # line 573
        index += count  # line 573
    return out  # line 574

def tokenizeGlobPatterns(oldPattern: 'str', newPattern: 'str') -> 'Tuple[_coconut.typing.Sequence[GlobBlock], _coconut.typing.Sequence[GlobBlock]]':  # line 576
    ot = tokenizeGlobPattern(oldPattern)  # type: List[GlobBlock]  # line 577
    nt = tokenizeGlobPattern(newPattern)  # type: List[GlobBlock]  # line 578
#  if len(ot) != len(nt): Exit("Source and target patterns can't be translated due to differing number of parsed glob markers and literal strings")
    if len([o for o in ot if not o.isLiteral]) < len([n for n in nt if not n.isLiteral]):  # line 580
        Exit("Source and target file patterns contain differing number of glob markers and can't be translated")  # line 580
    if any((O.content != N.content for O, N in zip([o for o in ot if not o.isLiteral], [n for n in nt if not n.isLiteral]))):  # line 581
        Exit("Source and target file patterns differ in semantics")  # line 581
    return (ot, nt)  # line 582

def convertGlobFiles(filenames: '_coconut.typing.Sequence[str]', oldPattern: '_coconut.typing.Sequence[GlobBlock]', newPattern: '_coconut.typing.Sequence[GlobBlock]') -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 584
    ''' Converts given filename according to specified file patterns. No support for adjacent glob markers currently. '''  # line 585
    pairs = []  # type: List[Tuple[str, str]]  # line 586
    for filename in filenames:  # line 587
        literals = [l for l in oldPattern if l.isLiteral]  # type: List[GlobBlock]  # source literals  # line 588
        nextliteral = 0  # type: int  # line 589
        index = 0  # type: int  # line 589
        parsedOld = []  # type: List[GlobBlock2]  # line 590
        for part in oldPattern:  # match everything in the old filename  # line 591
            if part.isLiteral:  # line 592
                parsedOld.append(GlobBlock2(True, part.content, part.content))  # line 592
                index += len(part.content)  # line 592
                nextliteral += 1  # line 592
            elif part.content.startswith("?"):  # line 593
                parsedOld.append(GlobBlock2(False, part.content, filename[index:index + len(part.content)]))  # line 593
                index += len(part.content)  # line 593
            elif part.content.startswith("["):  # line 594
                parsedOld.append(GlobBlock2(False, part.content, filename[index]))  # line 594
                index += 1  # line 594
            elif part.content == "*":  # line 595
                if nextliteral >= len(literals):  # line 596
                    parsedOld.append(GlobBlock2(False, part.content, filename[index:]))  # line 596
                    break  # line 596
                nxt = filename.index(literals[nextliteral].content, index)  # type: int  # also matches empty string  # line 597
                parsedOld.append(GlobBlock2(False, part.content, filename[index:nxt]))  # line 598
                index = nxt  # line 598
            else:  # line 599
                Exit("Invalid file pattern specified for move/rename")  # line 599
        globs = [g for g in parsedOld if not g.isLiteral]  # type: List[GlobBlock2]  # line 600
        literals = [l for l in newPattern if l.isLiteral]  # target literals  # line 601
        nextliteral = 0  # line 602
        nextglob = 0  # type: int  # line 602
        outname = []  # type: List[str]  # line 603
        for part in newPattern:  # generate new filename  # line 604
            if part.isLiteral:  # line 605
                outname.append(literals[nextliteral].content)  # line 605
                nextliteral += 1  # line 605
            else:  # line 606
                outname.append(globs[nextglob].matches)  # line 606
                nextglob += 1  # line 606
        pairs.append((filename, "".join(outname)))  # line 607
    return pairs  # line 608

@_coconut_tco  # line 610
def reorderRenameActions(actions: '_coconut.typing.Sequence[Tuple[str, str]]', exitOnConflict: 'bool'=True) -> '_coconut.typing.Sequence[Tuple[str, str]]':  # line 610
    ''' Attempt to put all rename actions into an order that avoids target == source names.
      Note, that it's currently not really possible to specify patterns that make this work (swapping "*" elements with a reference).
      An alternative would be to always have one (or all) files renamed to a temporary name before renaming to target filename.
  '''  # line 614
    if not actions:  # line 615
        return []  # line 615
    sources = None  # type: List[str]  # line 616
    targets = None  # type: List[str]  # line 616
    sources, targets = [list(l) for l in zip(*actions)]  # line 617
    last = len(actions)  # type: int  # line 618
    while last > 1:  # line 619
        clean = True  # type: bool  # line 620
        for i in range(1, last):  # line 621
            try:  # line 622
                index = targets[:i].index(sources[i])  # type: int  # line 623
                sources.insert(index, sources.pop(i))  # bubble up the action right before conflict  # line 624
                targets.insert(index, targets.pop(i))  # line 625
                clean = False  # line 626
            except:  # target not found in sources: good!  # line 627
                continue  # target not found in sources: good!  # line 627
        if clean:  # line 628
            break  # line 628
        last -= 1  # we know that the last entry in the list has the least conflicts, so we can disregard it in the next iteration  # line 629
    if exitOnConflict:  # line 630
        for i in range(1, len(actions)):  # line 630
            if sources[i] in targets[:i]:  # line 630
                Exit("There is no order of renaming actions that avoids copying over not-yet renamed files: '%s' is contained in matching source filenames" % (targets[i]))  # line 630
    return _coconut_tail_call(list, zip(sources, targets))  # convert to list to avoid generators  # line 631

def relativize(root: 'str', filepath: 'str') -> 'Tuple[str, str]':  # line 633
    ''' Determine OS-independent relative folder path, and relative pattern path. Always expects a file and determines its folder's relative path. '''  # line 634
    relpath = os.path.relpath(os.path.dirname(os.path.abspath(filepath)), root).replace(os.sep, SLASH)  # line 635
    return relpath, os.path.join(relpath, os.path.basename(filepath)).replace(os.sep, SLASH)  # line 636

def parseArgumentOptions(cwd: 'str', options: 'List[str]') -> 'Tuple[_coconut.typing.Optional[FrozenSet[str]], _coconut.typing.Optional[FrozenSet[str]], List[str], List[str]]':  # line 638
    ''' Returns (root-normalized) Tuple with set of [f{--only], f{--except}, [remotes], [noremotes]] arguments. '''  # line 639
    root = os.getcwd()  # type: str  # line 640
    onlys = []  # type: List[str]  # line 641
    excps = []  # type: List[str]  # line 641
    remotes = []  # type: List[str]  # line 641
    noremotes = []  # type: List[str]  # line 641
    for keys, container in [(("--only", "--include"), onlys), (("--except", "--exclude"), excps), (("--remote", "--remotes", "--only-remote", "--only-remotes", "--include-remote", "--include-remotes"), remotes), (("--except-remote", "--except-remotes", "--exclude-remote", "--exclude-remotes"), noremotes)]:  # line 642
        founds = [i for i in range(len(options)) if any([options[i].startswith(key + "=") or options[i] == key for key in keys])]  # assuming no more than one = in the string  # line 643
        for i in reversed(founds):  # line 644
            if "=" in options[i]:  # line 645
                container.extend(safeSplit(options[i].split("=")[1], ";"))  # TODO keep semicolon or use comma?  # line 646
            elif i + 1 < len(options):  # in case last --only has no argument  # line 647
                container.extend(safeSplit(options[i + 1], ";"))  # TODO test this  # line 648
                del options[i + 1]  # line 649
            del options[i]  # reverse removal  # line 650
    return (frozenset((oo for oo in (relativize(root, os.path.normpath(os.path.join(cwd, o)))[1] for o in onlys) if not oo.startswith(PARENT + SLASH))) if onlys else None, frozenset((ee for ee in (relativize(root, os.path.normpath(os.path.join(cwd, e)))[1] for e in excps) if not ee.startswith(PARENT + SLASH))) if excps else None, [os.path.abspath(os.path.normpath(_)) for _ in remotes], [os.path.abspath(os.path.normpath(_)) for _ in noremotes])  # line 651
