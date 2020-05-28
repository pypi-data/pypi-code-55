"""Functions for generic IO operations."""
import io
import json
import logging
import pathlib
from typing import TextIO, Tuple, Union

import attr
import cattr
import tabulate
from Bio.SeqIO.FastaIO import SimpleFastaParser
from click.utils import LazyFile as ClickFh

from .sequence import reverse_complement

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class Sequence:
    """Container for sequences."""

    title: str
    seq: str

    def __len__(self):
        return len(self.seq)

    def get_motif(self, motif):
        """Get sequence from mgedb.record sequence motif."""
        s = self.seq[motif.start:motif.end]
        return s if motif.strand == 1 else reverse_complement(s)


# Decalre types
SequencesType = Tuple[Sequence, ...]


def read_fasta(path: pathlib.Path) -> Sequence:
    """Read compressed fasta file."""
    with open(path) as f:
        logger.info(f'reading fa file: {path}')
        for title, seq in SimpleFastaParser(f):
            yield Sequence(title=title, seq=seq)


def write_fasta(file: Union[pathlib.Path, ClickFh, TextIO],
                entries: Union[SequencesType, Sequence],
                width=60) -> None:
    """Write sequence entries to path.

    Entries shall consist of a Tuple where the first entry is
    the header and the second entry is the sequence.
    """
    def print_seqs(entries, out):
        """Print sequence."""
        for e in entries:
            if not isinstance(e.title, (str, bytes)):
                m = f'Cannot write fasta sequence: invalid sequence {e.title}'
                raise ValueError(m)

            print(f'>{e.title}', file=out)  # Write header
            for ch in chunk(e.seq, width):
                ch = bytes(ch).decode('utf-8') if isinstance(
                    ch, (memoryview, bytes)) else ch
                print(ch, file=out)

    # convert to SequencesType
    entries = (entries, ) if isinstance(entries, Sequence) else entries
    if isinstance(file, (ClickFh, io.IOBase)):  # if click filehandle or textIO
        print_seqs(entries, file)
    else:  # if path object or sting is given
        with open(file, 'w') as o:
            logger.info(f'writing fasta file: {file}')
            print_seqs(entries, o)


def read_json(path: pathlib.Path):
    """Safely read json file from path."""
    with open(path) as f:
        return json.load(f)


def write_db_file(path: pathlib.Path, db, format=None) -> None:
    """Write database to file in json format."""
    logger.info(f'writing databse databse to: {path}')
    path = path if isinstance(path, pathlib.Path) else pathlib.Path(path)
    if path.suffix[1:] == 'json':
        format = 'json'

    with open(path, 'w') as o:
        data = cattr.unstructure(db)  # de serialize data
        if format == 'json':
            json.dump(data, o, indent=3)
        else:
            m = f'Unknown output format {path}, try manually specifying format'
            raise ValueError(m)


def parse_db_fasta_header(header: str):
    """Parse mgedb fasta header for cds and dna sequences.

    returns dictionary with:
    - name
    - allele number
    - accession number
    - gene name (cds only)
    - relative start pos (cds only)
    - relative end pos (cds only)
    """
    if header.count('|') == 2:
        name, seq_no, accnr = header.split('|')
        result = {'name': name, 'allele_no': int(seq_no), 'accnr': accnr}
    elif header.count('|') == 5:
        name, seq_no, accnr, prod_name, start, end = header.split('|')
        result = {
            'name': name,
            'allele_no': int(seq_no),
            'accnr': accnr,
            'product': prod_name,
            'start': int(start),
            'end': int(end)
        }
    else:
        raise ValueError('invalid fasta header')
    return result


def chunk(chars, length):
    """Chunk strings into substrings with length."""
    for i in range(0, len(chars), length):
        yield chars[i:i + length]


def _expand_db_link(link, mge_type=None):
    """Expand db link to url."""
    if link.name == 'isfinder':
        return f'https://www-is.biotoul.fr/scripts/ficheIS.php?name={link.db_id}'
    elif link.name == 'iceberg':
        iceberg_base_url = 'http://202.120.12.136:7913/ICEberg2'
        if mge_type == 'ice':
            return f'{iceberg_base_url}/feature_page.php?ice_id={link.db_id}'
        elif mge_type == 'ime':
            return '{iceberg_base_url}/feature_page_IME.php?ime_id={link.db_id}'
        elif mge_type == 'cime':
            return f'{iceberg_base_url}/feature_page_CIME.php?cime_id=${link.db_id}'
        else:
            raise ValueError(f'Unknown iceberg link: {link}')
    elif link.name == 'tn_registry':
        return 'https://transposon.lstmed.ac.uk/tn-registry'
    else:
        raise ValueError(f'unknown link: {link}')


def _print_seq_entry(seq_entry):
    coords = ','.join(f'{start}-{end}'
                        for start, end
                        in zip(seq_entry.start, seq_entry.end))

    entry = [
        ['accession', seq_entry.accession],
        ['partial', seq_entry.partial],
        ['coordinates', coords],
        ['irr', f'{seq_entry.irr.start}-{seq_entry.irr.end}, strand: {seq_entry.irr.strand}'],
        ['irl', f'{seq_entry.irl.start}-{seq_entry.irl.end}, strand: {seq_entry.irl.strand}'],
    ]

    # print basic sequence entry information
    tbl = tabulate.tabulate(entry, ['Sequence', '']).replace('\n', '\n  ')
    print('  ' + tbl + '\n')

    # print basic sequence entry information
    num_cds = len(seq_entry.cds)
    for e, cds in enumerate(seq_entry.cds, start=1):
        cds_entries = [
            ['coords', f'{cds.start}-{cds.end}, strand: {cds.strand}'],
            ['gene', cds.gene],
            ['product', cds.product]]

        if hasattr(cds, 'chemistry'):
            cds_entries.append(['chemistry',
                                cds.chemistry.value
                                if cds.chemistry
                                else ''])

        tbl = tabulate.tabulate(cds_entries, [f'CDS {e}', '']).replace('\n', '\n    ')
        print('    ' + tbl)
        if e != num_cds:
            print()


def print_formatted_db_entry(entry):
    """Format output."""
    mge_type = entry.type.name.lower().replace('_', ' ')
    entry_tbl = [
        ['name', entry.name],
        ['synonyms', ', '.join(entry.synonyms)],
        ['family', entry.family],
        ['group', entry.group],
        ['type', mge_type],
        ['evidence level', entry.evidence_lvl.value],
        ['organism', ','.join(f'{o.name}, {o.taxid}' if o.taxid else f'{o.name}'
                              for o in entry.organism)],
        ['data source', '\n'.join(_expand_db_link(l, mge_type)
                                    for l in entry.link)],
    ]
    # print basic entry information
    tbl = tabulate.tabulate(entry_tbl, [entry.name, ''])
    print(tbl)
    print()
    # print sequnce information
    for seq_entry in entry.sequences:
        _print_seq_entry(seq_entry)
    return max(len(r) for r in tbl.split('\n'))
