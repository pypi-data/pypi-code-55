from abc import ABCMeta, abstractmethod
from typing import Optional, Dict

from sardine.lang.manifest.builder import StackManifestBuilder
from sardine.lang.parser.objects import StackDeclaration
from sardine.lang.parser.parser import Parser
from sardine.lang.tokenizer.tokenizer import Tokenizer
from sardine.types import STACK_DECLARATIONS_TYPE

_cached_manifest: Optional[Dict[str, StackDeclaration]] = None


class BaseManifestResolver(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def manifest_exists(cls) -> bool:
        raise NotImplementedError

    @classmethod
    def load_manifest(cls) -> STACK_DECLARATIONS_TYPE:
        global _cached_manifest
        if _cached_manifest is None:
            unparsed_manifest = cls._load_manifest()
            tokenized_manifest = Tokenizer.tokenize(unparsed_manifest)
            parsed_declarations = Parser(tokenized_manifest).parse()
            stack_declarations = StackManifestBuilder.build(parsed_declarations)
            _cached_manifest = stack_declarations
        return _cached_manifest

    @classmethod
    @abstractmethod
    def create_directories(cls) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _load_manifest(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _manifest_path(cls) -> str:
        raise NotImplementedError
