"""Read MGEdb."""
import logging
import pathlib
import subprocess
from enum import Enum, unique
from typing import Dict, Generator, List, Optional, Union

from pkg_resources import resource_filename

import attr
from cattr import structure

from .io import Sequence, read_fasta, read_json

LOG = logging.getLogger(__name__)


@attr.s(frozen=True, auto_attribs=True)
class Reference:
    """Contain reference information schema."""

    authors: List[str]
    date: str
    journal: str
    pmid: int
    title: str


@attr.s(frozen=True, auto_attribs=True)
class SeqRecord:
    """Container for mge position."""

    start: int
    end: int
    strand: int


@attr.s(frozen=True, auto_attribs=True)
class DbLink:
    """Link to external databases."""

    name: str
    db_id: str


@unique
class TransposaseChemistry(Enum):
    """Valid transposase chemistry denotions."""

    DDE = 'dde'
    DEDD = 'dedd'
    Y1 = 'y1'
    Y2 = 'y2'
    SERINE = 'serine'


@attr.s(frozen=True, auto_attribs=True)
class TransposaseRecord:
    """Container for sequence record information."""

    start: Optional[int]
    end: Optional[int]
    strand: Optional[int]
    gene: Optional[str]
    product: str
    chemistry: Optional[TransposaseChemistry]


@attr.s(frozen=True, auto_attribs=True)
class CDSRecord:
    """Container for sequence record information."""

    start: Optional[int]
    end: Optional[int]
    strand: Optional[int]
    gene: Optional[str]
    product: str


@unique
class MgeType(Enum):
    """Valid MGE types."""

    ICE = 'ice'
    IME = 'ime'
    AICE = 'aice'
    CIME = 'cime'
    MITE = 'mite'
    INSERTION_SEQUENCE = 'is'
    MOBILE_INSERTION_CASSETTE = 'mic'
    UNIT_TRANSPOSON = 'tn'
    COMPOSITE_TRANSPOSON = 'cn'
    RT = 'retrotransposon'
    IN = 'integron'
    OTHER = 'other'


@unique
class EvidenceLvl(Enum):
    """Valid MGE types."""

    EXPERIMENTAL = 'experimental'
    INSILICO = 'in-silico'
    UNKNOWN = 'unknown'


@attr.s(frozen=True, auto_attribs=True)
class Specie:
    """Specie information."""

    name: Optional[str]
    taxid: Optional[str]


@attr.s(frozen=True, auto_attribs=True)
class MgeSeqEntry:
    """Entry information for MGE allele sequence."""

    accession: str
    partial: bool
    cds: List[Union[TransposaseRecord, CDSRecord]]
    start: List[int]
    end: List[int]
    irl: Optional[SeqRecord]
    irr: Optional[SeqRecord]

    def __len__(self):
        """Return the lenght of the seqence."""
        return sum(e - s + 1
                   for s, e in map(sorted, zip(self.start, self.end)))


@attr.s(frozen=True, auto_attribs=True)
class MGErecord:
    """Reference information schema."""

    name: str
    type: MgeType
    family: str
    group: str
    link: List[DbLink]
    synonyms: List[str]
    evidence_lvl: EvidenceLvl
    organism: List[Specie]
    references: Optional[List[str]]
    sequences: List[MgeSeqEntry]


def _get_top_level_dir() -> Optional[pathlib.Path]:
    """Get path to project top level directory."""
    proc = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                          stdout=subprocess.PIPE)
    proc.check_returncode()  # Assert called working correctly
    path = pathlib.Path(proc.stdout.decode('utf-8').rstrip())
    if not path.is_dir():
        raise FileNotFoundError('Directory not found', str(path))
    return path


# Type declerations
MgeRecordsType = Dict[str, MGErecord]
ReferencesType = Dict[int, Reference]


class MGEdb:
    """Database handler for MGEdb."""

    records_fname: str = 'mge_records.json'
    references_fname: str = 'references.json'
    nomenclature_fname: str = 'mge_nomenclature.json'
    record_seq_fname: str = 'mge_records.fna'
    record_cds_fname: str = 'mge_cds.faa'

    def __init__(self, path: Optional[str] = None, cache: bool = True):
        """Initiate database.

        If cache is true the database will be kept in memory.

        Keyword Arguments:
        path -- (default None)
        cache -- (default True)
        """
        if path:
            self.database_path = pathlib.Path(path)
        else:
            self.database_path = self._resource_dir()
        LOG.info(f'mgedb instance: {self.database_path}')

        self.cache_data = cache
        self._mge_records_cache = None
        self._references_cache = None

    def _resource_dir(self):
        """Get file stream of file in package_data."""
        dta = pathlib.Path(resource_filename(__name__, 'data'))
        return dta.absolute()

    @property
    def references(self, cache=True) -> ReferencesType:
        """Return references to scientific publications."""
        if self.cache_data and cache:
            if self._references_cache is None:
                dta = self._load_set(self.references_fname,
                                     Dict[int, Reference])
                self._references_cache = dta
            else:
                dta = self._references_cache
        else:
            dta = self._load_set(self.references_fname, Dict[int, Reference])
        return dta

    @property
    def records(self, cache=True) -> MgeRecordsType:
        """Return mges in the database."""
        if self.cache_data and cache:
            if self._mge_records_cache is None:
                dta = self._load_set(self.records_fname, Dict[str, MGErecord])
                self._mge_records_cache = dta
            else:
                dta = self._mge_records_cache
        else:
            dta = self._load_set(self.records_fname, Dict[str, MGErecord])
        return dta

    @property
    def nomenclature(self) -> Dict[str, List[str]]:
        """Return set of genetic element names."""
        return self._load_set(self.nomenclature_fname, Dict[str, List[str]])

    @property
    def record_sequences(self) -> Dict[str, List[str]]:
        """Return set of genetic element names."""
        return self._load_seq(self.record_seq_fname)

    @property
    def record_sequences_path(self) -> pathlib.Path:
        """Return path to records sequences."""
        return self.database_path.joinpath('sequences.d',
                                           self.record_seq_fname)

    def _load_set(self, data: str, cls):
        """Load database file to memory and ensure structure."""
        fname, suffix = data.split('.')
        if suffix in ['fna', 'faa']:
            LOG.info(f'read {fname} sequences file')
        else:
            LOG.info(f'read {fname} records file')
        data_file = self.database_path.joinpath(data)
        if suffix == 'json':
            record = read_json(data_file)
        else:
            raise ValueError(f'Unexpected file format: {suffix}')
        return structure(record, cls)

    def _load_seq(self, file_name: str) -> Generator[Sequence, None, None]:
        """Load sequences to and ensure data structure.

        Keyword Arguments:
        seq_file: str -- sequence file to be loaded
        """
        seq_file = self.database_path.joinpath('sequences.d', file_name)
        return read_fasta(seq_file)


def build_fasta_header(**kwargs):
    """Build fasta header in mgedb format."""
    try:
        if len(kwargs) == 3:
            # for record sequences
            args = [kwargs['name'], kwargs['seq_id'], kwargs['accession']]
        elif len(kwargs) == 6:
            # for record cds protein sequences
            args = [
                kwargs['name'], kwargs['seq_id'], kwargs['accession'],
                kwargs['product'], kwargs['start'], kwargs['end']
            ]
        else:
            raise ValueError('Invalid number of arguments')
    except KeyError as err:
        raise ValueError(f'Missing data: {", ".join(err.args)}')
    except ValueError as err:
        raise err
    return '|'.join(map(str, args))
