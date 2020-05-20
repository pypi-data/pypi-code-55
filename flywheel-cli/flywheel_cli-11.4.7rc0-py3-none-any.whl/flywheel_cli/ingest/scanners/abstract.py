"""Provides AbstractScanner class"""

from abc import ABC, abstractmethod


class AbstractScanner(ABC):
    """Provides common interface for scanners"""

    def __init__(self, ingest_config, strategy_config, worker_config, walker, opts=None, context=None, get_subject_code_fn=None):
        self.ingest_config = ingest_config
        self.strategy_config = strategy_config
        self.worker_config = worker_config
        self.walker = walker
        self.opts = opts
        self.context = context
        self.get_subject_code_fn = get_subject_code_fn

    @abstractmethod
    def _scan(self, subdir):
        """Scanner specific implementation"""

    def _initialize(self):
        """Initialize scanner"""

    def scan(self, dirpath):
        """Run scan"""
        self._initialize()
        return self._scan(dirpath)

    @staticmethod
    def context_merge_subject_and_session(context):
        """Merge session & subject labels"""
        merged = False
        if 'session' in context and 'label' in context['session']:
            context.setdefault('subject', {})['label'] = context['session']['label']
            merged = True
        if not merged and 'subject' in context and 'label' in context['subject']:
            context.setdefault('session', {})['label'] = context['subject']['label']
            merged = True
        return merged

    @staticmethod
    def validate_opts(opts):
        """Validate the scanner options, raising a ValueError if invalid"""
