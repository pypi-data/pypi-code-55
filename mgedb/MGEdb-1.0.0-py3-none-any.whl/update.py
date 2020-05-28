"""Update current MGEdb with records generated from iscraper tool."""
import logging
import os
import tarfile
from collections import defaultdict
from datetime import datetime
from itertools import chain
from typing import Dict, List, Tuple

import attr
import click

from .db import (EvidenceLvl, MGEdb, MGErecord, MgeRecordsType, MgeSeqEntry,
                 ReferencesType, _get_top_level_dir)
from .io import Sequence, parse_db_fasta_header

SequencesType = Tuple[Sequence, ...]
MgeSeqEntries = List[MgeSeqEntry]

LOG = logging.getLogger(__name__)


class MergeConflictError(Exception):
    """Conflict when merging records."""

    pass


@attr.s(frozen=True, auto_attribs=True, slots=True)
class ExecutionContext:
    """Container for execution parameters and utility functions."""

    backup_dir: str
    db_dir: str = os.path.dirname(__file__)
    exec_start = datetime.now()

    def path(self, *rel_path) -> str:
        """Generate absolute path from path relatvie from output directory.

        Keyword Arguments:
        *path -- relative path components
        """
        new_path = os.path.join(self.db_dir, *rel_path)
        if os.path.isfile(new_path):
            return new_path
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        return new_path

    def checked_path(self, *rel_path) -> str:
        """Generate a absolute path to an existing file."""
        new_path = os.path.join(self.db_dir, *rel_path)
        if os.path.isfile(new_path):
            return os.path.relpath(new_path, self.db_dir)
        raise FileNotFoundError


def merge_references(old_db: MGEdb, new_db: MGEdb) -> ReferencesType:
    """Merge references on old_db with references in new_db and resolve conflicts.

    Entries in new_db with duplicated id will be omitted.
    Keyword Arguments:
    old_db: MGEdb -- Database instance of old database
    new_db: MGEdb -- Database instance of new database
    """
    LOG.info('merge references')
    old_references: ReferencesType = old_db.references
    updated_references: ReferencesType = {}

    ref_id: int
    reference: ReferencesType
    for ref_id, reference in new_db.references.items():
        if ref_id in old_references:  # In case of conflict
            if old_references[ref_id] != reference:
                raise MergeConflictError
            else:
                continue
        else:
            updated_references[ref_id] = reference
    return {**old_references, **updated_references}  # TODO return imutable


def merge_sequences(old_db: MGEdb, new_db: MGEdb) -> SequencesType:
    """Merge sequences in old_db with new_db omitting duplicates in new_db.

    Keyword Arguments:
    old_db: MGEdb -- instance of old database
    new_db: MGEdb -- instance of new database
    """
    old_sequences = {s.title: s for s in old_db.record_sequences}
    results: List[Sequence] = list(old_sequences.values())
    for new_seq in new_db.record_sequences:
        if new_seq.title in old_sequences:
            if new_seq != old_sequences[new_seq.title]:
                raise MergeConflictError
            else:
                continue
        results.append(new_seq)
    return tuple(results)


def make_synonyms_index(records: MgeRecordsType) -> Dict[str, str]:
    """Make a dictionary index with all synonyms in the database.

    Duplicates in synonyms are not allowed and will raise error
    """
    LOG.info('Make index of synonymous mge names')
    synonyms_index = {}
    for mge_name, rec in records.items():
        if mge_name in synonyms_index:
            m = f'Mge name: {mge_name} - in synonyms in another entry'
            LOG.error(m)
            raise ValueError(m)
        synonyms_index[mge_name] = mge_name
        for syn_name in rec.synonyms:
            synonyms_index[syn_name] = mge_name
    return synonyms_index


def _get_identical_sequences(old_db: MGEdb, new_db: MGEdb):
    """Find and extract identical sequences in old and new db."""
    LOG.info('Get identical sequences')
    new_seqs = {r.seq: r.title for r in new_db.record_sequences}
    dupl_seqs = {}
    for old_sequence in old_db.record_sequences:
        if old_sequence.seq in new_seqs:
            old_header = parse_db_fasta_header(old_sequence.title)
            new_header = parse_db_fasta_header(new_seqs[old_sequence.seq])
            if old_header['name'] in dupl_seqs:
                m = f'Mge: {old_header["name"]} is duplicated'
                LOG.error(m)
                raise ValueError()
            dupl_seqs[old_header['name']] = {
                'old': old_header,
                'new': new_header
            }
    return dupl_seqs


def _is_na(val):
    """Check if NA value."""
    if val.lower() == 'none':
        return None
    else:
        return val


def merge_records(old_db: MGEdb, new_db: MGEdb) -> MgeRecordsType:
    """Merge records in old_db with new_db omitting duplicates in new_db.

    Keyword Arguments:
    old_db: MGEdb -- instance of old database
    new_db: MGEdb -- instance of new database
    """
    LOG.info('merge records')
    old_records: MgeRecordsType = old_db.records
    syn_idx: Dict[str, str] = make_synonyms_index(old_records)

    # get names of identical sequences in old and new db
    identical_seqs = _get_identical_sequences(old_db, new_db)

    new_seq = {s.title: s for s in new_db.record_sequences}

    updated_sequences = []
    updated_records: MgeRecordsType = {}
    rec_id: str
    record: MGErecord
    for rec_id, new_record in new_db.records.items():
        new_rec_idx = [rec_id] + new_record.synonyms
        # synonym or name in old database
        if any(r in syn_idx for r in new_rec_idx):
            existing_syn = next(r for r in new_rec_idx if r in syn_idx)
            # translate name to record name and get old record
            old_name = syn_idx[existing_syn]
            old_record = old_records[old_name]
            if old_record == new_record:  # skip identical records
                continue


            upd_syn = list(
                set(old_record.synonyms + new_record.synonyms))
            upd_links = list(set(old_record.link + new_record.link))
            upd_type = new_record.type
            # update group

            upd_group = _merge_data_point(old_record.group, new_record.group)
            upd_family = _merge_data_point(old_record.family, new_record.family)
            upd_level = _update_evidence_lvl(old_record, new_record)

            if old_name in identical_seqs:
                # merge without adding new seqence
                upd_specie = old_record.organism
                if new_record.name not in upd_syn:
                    try:
                        upd_record_sequences = _update_record_seq(
                            old_record.sequences, new_record.sequences)
                    except KeyError as err:
                        m = f'Merge conflict: {old_record.name} - {err.args[0]}'
                        raise click.UsageError(f'{m}, resolve manually')
                else:
                    upd_record_sequences = old_record.sequences
            else:
                # TODO merge species on taxid if possible
                upd_specie = old_record.organism
                curr_seq_no = len(old_record.sequences)
                # iterate over new sequences, assign new header names as part of old record
                for seq_no, sequence in enumerate(
                        new_record.sequences, start=1):
                    curr_seq_no += 1
                    seq_name = f'{new_record.name}|{seq_no}|{sequence.accession}'
                    new_seq_entry = Sequence(
                        title=
                        f'{old_record.name}|{curr_seq_no}|{sequence.accession}',
                        seq=new_seq[seq_name].seq)
                    updated_sequences.append(new_seq_entry)
                # add new
                upd_record_sequences = old_record.sequences + new_record.sequences
            # update record
            updated_records[rec_id] = attr.evolve(
                old_record,
                evidence_lvl=upd_level,
                family=upd_family,
                group=upd_group,
                link=upd_links,
                organism=upd_specie,
                synonyms=upd_syn,
                type=upd_type,
                sequences=upd_record_sequences)
        else:
            updated_records[rec_id] = new_record
            for seq_no, sequence in enumerate(new_record.sequences, start=1):
                seq_name = f'{new_record.name}|{seq_no}|{sequence.accession}'
                updated_sequences.append(new_seq[seq_name])
            # add new sequence to record, simple append

    merged_seq = list(chain(old_db.record_sequences, updated_sequences))
    return {**old_records, **updated_records}, merged_seq


def backup_db(ctx: ExecutionContext, db: MGEdb) -> str:
    """Back up database as tar archive."""
    timestamp = ctx.exec_start.isoformat(timespec='minutes')
    fname = f'{timestamp}_mgedb_bak.tar.gz'
    backup_file_path = os.path.join(ctx.backup_dir, fname)
    LOG.info(f'backup old database to: {ctx.backup_dir}')
    os.makedirs(os.path.dirname(backup_file_path), exist_ok=True)
    with tarfile.open(backup_file_path, 'w|gz') as tar:
        tar.add(ctx.checked_path(db.database_path, db.references_fname))
        tar.add(ctx.checked_path(db.database_path, db.records_fname))
        tar.add(ctx.checked_path(db.database_path, db.nomenclature_fname))
        tar.add(
            ctx.checked_path(db.database_path, 'sequences.d',
                             db.record_seq_fname))
        tar.add(
            ctx.checked_path(db.database_path, 'sequences.d',
                             db.record_cds_fname))
    return backup_file_path


def _update_record_seq(old_seq: MgeSeqEntries,
                       new_seq: MgeSeqEntries) -> MgeSeqEntries:
    """Update old CDS annotations with new."""
    def _make_key(seq_entry):
        """Make unique dict key for entry."""
        return (seq_entry.accession, seq_entry.start[0], seq_entry.end[0])

    n_seq = {_make_key(s): s for s in new_seq}
    o_seq_id = [_make_key(seq) for seq in old_seq]
    if len(set(n_seq.keys()) - set(o_seq_id)) != 0:
        raise KeyError({'new_seq': list(n_seq.keys()),
                        'old_seq': list(o_seq_id)})

    return [attr.evolve(seq, cds=n_seq[_make_key(seq)].cds)
            for seq in old_seq
            if _make_key(seq) in n_seq]


def _merge_data_point(old, new):
    """Generic merging of data."""
    old, new = map(_is_na, [old, new])
    # if both are not null
    if old is not None and new is not None:
        if old == new:
            return old
        else:
            raise ValueError(old, new)

    # pick non null value over null
    if old is not None and new is None:
        return old
    elif new is not None and old is None:
        return new
    else:
        return None


def _update_evidence_lvl(old, new):
    """Update evidence level of records.

    higher level has presecende over lower
    """
    if any(r.evidence_lvl == EvidenceLvl.EXPERIMENTAL for r in [old, new]):
        upd_level = EvidenceLvl.EXPERIMENTAL
    elif any(r.evidence_lvl == EvidenceLvl.INSILICO for r in [old, new]):
        upd_level = EvidenceLvl.INSILICO
    else:
        upd_level = EvidenceLvl.UNKNOWN
    return upd_level


def update_nomenclature(mge_records):
    """Update nomenclature file."""
    LOG.info('Update mge nomenclature')
    grouper = defaultdict(set)
    for r in mge_records.values():
        grouper[r.type.value].add(r.name)
    return {k: sorted(list(v)) for k, v in grouper.items()}
