"""Functions for extracting CDS sequences from mgedb."""
import logging
import re
from typing import Iterator, List, Pattern

import attr
import click

from .db import MGEdb, MgeType, SeqRecord, Sequence, build_fasta_header
from .sequence import reverse_complement

LOG = logging.getLogger(__name__)

db = MGEdb()  # initialte mgedb

_SEQ_PATTERN = re.compile(rb'^[AGCT]+$', flags=re.I)
START_CODONS = [b'ATG', b'TTG', b'GTG']
STOP_CODONS = [b'TAG', b'TAA', b'TGA']


class CoordinateError(Exception):
    pass


class UndefinedCoordinatesError(CoordinateError):
    pass


class CoordOutOfBoundsError(CoordinateError):
    pass


def validate_type(ctx, param, value):
    """Validate mge type."""
    valid_types = [MgeType(t).name.lower() for t in db.nomenclature]
    for putative_type in value:
        if putative_type not in valid_types:
            valid = ', '.join(valid_types)
            m = f'{putative_type} is not a valid type. Valid types: {valid}'
            raise click.BadParameter(m)
    return value


def validate_sequence(seq):
    """Determine if a sequence is likely a functional gene."""
    seq = bytes(seq)
    if not re.match(_SEQ_PATTERN, seq):
        return False

    return True


def record_length(rec_seq):
    """Get length of record."""
    record_chunks = []
    for coords in zip(rec_seq.start, rec_seq.end):
        start, end = sorted(coords)
        record_chunks.append(range(start, end + 1))
    return sum(len(ch) for ch in record_chunks)


def is_type(cds, *valid_words):
    """Get genes with words in product or gene."""
    annot = [e.lower() for e in [cds.product, cds.gene] if e is not None]
    return any(w in annot for w in valid_words)


def refmt_title(cds, idx, header):
    """Reformat header and CDS."""
    if cds.product is None:
        product = str(cds.product)
    else:
        product = cds.product.lower().replace(' ', '_')
    return f'{product}|{str(cds.gene).lower()}|{idx}|{header}'


def get_seq():
    """Load recrods sequence and forward getter function."""
    LOG.info('Setup sequence extraction')
    record_sequences = {
        s.title: memoryview(s.seq.encode('ascii'))
        for s in db.record_sequences
    }

    def get_subsequence(start, end, strand, seq_id):
        """Get subsequence in entry with seq_id."""
        rec_seq = record_sequences[seq_id]
        sequence = rec_seq[start:end]
        if strand == -1:
            sequence = bytes(reverse_complement(sequence))

        if start < 0 or end < 0:
            raise CoordinateError

        if start > len(rec_seq) or end > len(rec_seq):
            raise CoordOutOfBoundsError

        if not validate_sequence(sequence):
            nt = ', '.join(set(bytes(sequence).decode('utf-8')))
            LOG.warning(f'{seq_id} - invalid sequence, contains chars: {nt}')
        return Sequence(title=None, seq=sequence)

    return get_subsequence


def _cds_by_regex(seq, regex):
    """Filter cds with gene or product matching regex."""
    for cds in seq.cds:
        for pattern in regex:
            for attrib in ['gene', 'product']:
                if re.search(pattern, str(getattr(cds, attrib))):
                    yield cds


def to_seq(entry, seq_id, get_seq):
    """Print entry in fasta format."""
    if entry.start is None and entry.end is None:
        raise UndefinedCoordinatesError

    sequence = get_seq(entry.start, entry.end, entry.strand, seq_id=seq_id)
    if isinstance(entry, SeqRecord):
        title = f'ir|{entry.start}|{entry.end}|{seq_id}'
    else:
        title = f'{entry.product}|{entry.gene}|{entry.start}|{entry.end}|{seq_id}'
    sequence = attr.evolve(sequence, title=title)

    if len(sequence.seq) == 0:  # skip empty sequences
        LOG.info(f'Empyt sequence: {seq_id}')
        return

    return sequence


def get_ir(seq, seq_id, get_seq):
    """Get inverted repeat sequence."""
    for cnt, i in enumerate(['irl', 'irr'], start=1):
        repeat = getattr(seq, i)
        if repeat is not None:
            sequence = get_seq(
                repeat.start, repeat.end, repeat.strand, seq_id=seq_id)
            title = f'{i}|{cnt}|{seq_id}'
            sequence = attr.evolve(sequence, title=title)

            if len(sequence.seq) == 0:  # skip empty sequences
                LOG.info(f'Empyt sequence: {seq_id}')
                continue
            yield sequence


def get_cds_by_regex(db: MGEdb, regex: List[Pattern]) -> Iterator[Sequence]:
    """Wrtie cds matching regex to file object."""
    get_sub_seq = get_seq()
    for rec in db.records.values():
        for seq_id, seq in enumerate(rec.sequences, start=1):
            header = build_fasta_header(
                name=rec.name, seq_id=seq_id, accession=seq.accession)
            # print filtered cds
            for cds in _cds_by_regex(seq, regex):
                try:
                    s = to_seq(cds, header, get_sub_seq)
                except (CoordOutOfBoundsError,
                        UndefinedCoordinatesError) as err:
                    LOG.warning(
                        f'{rec.name}: {err.__class__.__name__}, skipping')
                    continue

                if s is None:
                    continue

                yield s
