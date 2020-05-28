"""Functions for database validation content."""

import logging
import re
import sys
from collections import Counter, defaultdict
from typing import Callable

import cattr
import click

from .db import MGEdb, MgeType
from .io import parse_db_fasta_header

LOG = logging.getLogger(__name__)

_SEQ_PATTERN = re.compile(r'^[AGCT]+$', flags=re.I)

_SEQ_AMBIGIOUS_PATTERN = re.compile(r'^[AGCTYRWSKMDVHBXN]+$', flags=re.I)

_SEQ_UNKNOWN_NT_PATTERN = re.compile(r'^[XN]+$', flags=re.I)


class ValidationError(Exception):
    """Validation error catergory."""

    def __init__(self, names, **kwargs):
        self.names = map(str, names)
        self.kwargs = kwargs


class InvalidType(ValidationError):
    """Invalid MGE type."""

    pass


class InvalidName(ValidationError):
    """Invalid MGE name."""

    pass


class AccessionMissmatch(ValidationError):
    """Invalid accession."""

    pass


class SequenceLengthMissmatch(ValidationError):
    """Missmatch of sequence length between record and sequence."""

    pass


class SequenceError(ValidationError):
    """Generic errors relating to sequences."""

    pass


class NonStandardNucleotide(ValidationError):
    """Non standard nucleotides."""

    pass


class UnknownSequence(ValidationError):
    """Non standard nucleotides."""

    pass


class InvalidHeaderFormat(ValidationError):
    """Invalid MGE type."""

    pass


class DuplicatedSequence(ValidationError):
    """Duplicated sequence."""

    pass


class MissingSeqRecord(ValidationError):
    """Errors for missing sequence records."""

    pass


class InvalidCoordinate(ValidationError):
    """Errors for missing sequence records."""

    pass


def _validate_record_names(db) -> None:
    """Validate MGE record names."""
    LOG.info('Validate record names')
    names = db.nomenclature
    # cast as mge tpye class
    valid_types = [cattr.structure(type, MgeType) for type in names]
    records = db.records
    for _, r in records.items():
        if r.type not in valid_types:
            raise InvalidType(names=[r.name])
        if r.name not in names[r.type.value]:
            msg = f'Invalid MGE {r.type.value} name'
            raise ValidationError(names=[r.name], message=msg)


def _validate_record_information(db) -> None:
    """Validate MGE record information."""
    LOG.info('Validate record ')
    records = db.records
    for seq in db.record_sequences:
        header = parse_db_fasta_header(seq.title)
        rec_seq = records[header['name']].sequences[header['allele_no'] - 1]
        # validate accession
        if rec_seq.accession != header['accnr']:
            raise AccessionMissmatch(names=[rec_seq.accession, header['name']])

        # validate lenght mge annotation matches sequence
        record_chunks = []
        for coords in zip(rec_seq.start, rec_seq.end):
            start, end = sorted(coords)
            record_chunks.append(range(start, end + 1))
        record_length = sum(len(ch) for ch in record_chunks)
        if record_length != len(seq.seq):
            raise SequenceLengthMissmatch(names=[header['name']])

        # validate cds information
        for c in rec_seq.cds:
            for name in ['start', 'end']:
                cds_coord = getattr(c, name)
                # check if coordinate are whithin bounds
                if record_length <= cds_coord and cds_coord < 0:
                    raise InvalidCoordinate(f'{name}: {c.start}')


def _validate_sequence_links(db) -> None:
    """Validate that each record links to correct resources."""
    LOG.info('Validate links')
    records = db.records
    record_headers = {f'{r.name}|{seq_no}|{req_s.accession}'
                      for r in records.values()
                      for (seq_no, req_s) in enumerate(r.sequences, start=1)}
    seq_file_headers = {seq.title for seq in db.record_sequences}
    # get headers missing in either records annotation file or sequences
    missing_in_sequences = seq_file_headers - record_headers
    missing_in_records = record_headers - seq_file_headers

    if len(missing_in_sequences) > 0:
        raise MissingSeqRecord(names=missing_in_sequences)
    elif len(missing_in_records) > 0:
        raise MissingSeqRecord(names=missing_in_records)


def _validate_record_sequences(db):
    """Validate that record sequences are in valid fasta format."""
    LOG.info('Validate record sequences')
    entries = defaultdict(list)
    for seq_entry in db.record_sequences:
        entries[seq_entry.seq].append(seq_entry.title)

    # Check for duplicated sequences
    for seq_titles in entries.values():
        if len(seq_titles) > 1:
            raise DuplicatedSequence(names=seq_titles)

    # Verify that sequence is valid fasta format
    for seq, title in entries.items():
        title = title[0]  # Previously validated to be only one
        try:
            parse_db_fasta_header(title)
        except ValueError:
            raise InvalidHeaderFormat(names=[title])

        if not seq:
            raise SequenceError(names=[title])
        if not re.match(_SEQ_PATTERN, seq):
            nt_comp = {k: cnt for k, cnt in Counter(seq).most_common()}
            if re.match(_SEQ_AMBIGIOUS_PATTERN, seq):
                if re.match(_SEQ_UNKNOWN_NT_PATTERN, seq):
                    raise UnknownSequence(names=[title], **nt_comp)
                nt_comp = ' '.join([f'{k}={cnt}' for k, cnt in nt_comp.items()])
                LOG.warning(f'Sequence contains ambigious nt: {title}, nt_comp={nt_comp}')
            else:
                raise NonStandardNucleotide(names=[title], **nt_comp)


VALIDATOR_FNS: Callable[..., None] = [
    _validate_sequence_links,
    _validate_record_information,
    _validate_record_sequences,
    _validate_record_names,
]
