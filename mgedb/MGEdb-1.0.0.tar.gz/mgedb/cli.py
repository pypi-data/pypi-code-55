"""CLI for common database tools and operations."""
import logging
import logging.config
import pathlib
import re
import sys

import cattr
import click

from .db import MGEdb, MgeRecordsType, build_fasta_header
from .extract import (CoordOutOfBoundsError, UndefinedCoordinatesError,
                      get_cds_by_regex, get_seq, to_seq)
from .io import print_formatted_db_entry, write_db_file, write_fasta
from .update import (ExecutionContext, backup_db, merge_records,
                     update_nomenclature)
from .validate import VALIDATOR_FNS, ValidationError
from .version import __version__ as version

db = MGEdb()  # initialte mgedb

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem
    'formatters': {
        'standard': {
            'format': '[ %(levelname)s ] %(message)s',
        },
    },
    'handlers': {
        'default': {
            'formatter': 'standard',
            'level': logging.INFO,
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        },
    },
})


def _print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(version)
    ctx.exit()


@click.group()
@click.option('--version',
              is_flag=True,
              callback=_print_version,
              expose_value=False,
              is_eager=True)
def main():
    """Database tools."""
    pass


@main.command()
def validate():
    """Validate MGE database content."""
    LOG = logging.getLogger(__name__)
    LOG.info('Start validating database')

    for validator_fn in VALIDATOR_FNS:
        test_name = validator_fn.__doc__
        try:
            validator_fn(db)
            click.secho(f' ✓ {test_name}', fg='green')
        except ValidationError as err:
            names = ', '.join(err.names)
            msg = f'Error {err.__class__.__name__} - names: {names}'
            args = ', '.join(err.args)
            # append args and kwargs in errors
            if args:
                msg = f'{msg}; {args}'
            kwargs = ', '.join([f'{k}: {v}' for k, v in err.kwargs.items()])
            if kwargs:
                msg = f'{msg}; {kwargs}'
            LOG.error(msg)
            click.secho(f' ✖ {test_name}', fg='red')
            sys.exit(1)


@main.command()
@click.option('--name',
              type=str,
              help='Name of mobile element to view information on')
@click.option('--family',
              type=str,
              help='Family of mobile elements to view information on')
def view(name, family):
    """Get stored information on Mobile Element records."""
    if name is None and family is None:
        raise click.UsageError(
            'Your must select one element or family to view')

    LOG = logging.getLogger(__name__)
    records = db.records

    if name:
        if name not in records:
            raise click.UsageError(f'Name: {name}, not in database')
        entries = [records[name]]
    elif family:
        entries = [r for r in records.values() if r.family == family]
        if len(entries) == 0:
            raise click.UsageError(
                f'Specified family: {family} not in database')
    else:
        raise click.UsageError(
            'Your must select one element or family to view')

    num_entries = len(entries)
    for n, entry in enumerate(entries, start=1):
        l = print_formatted_db_entry(entry)
        click.secho('=' * l)
        # add new line for multiple entires
        if n != num_entries:
            click.secho()


@main.group()
def extract():
    """Extract sequences from MGEdb."""
    pass


@extract.command()
@click.argument('fasta_file', type=click.File('w'))
def ir(fasta_file):
    """Extract inverted repeats from MGEdb."""
    LOG = logging.getLogger(__name__)
    LOG.info('Extracting inverted repeats')

    LOG.info(f'writing sequences to fasta file: {fasta_file.name}')

    get_sub_seq = get_seq()
    num_entries = 0
    for rec in db.records.values():
        for seq_id, seq in enumerate(rec.sequences, start=1):
            header = build_fasta_header(name=rec.name,
                                        seq_id=seq_id,
                                        accession=seq.accession)

            for cnt, i in enumerate(['irl', 'irr'], start=1):
                repeat = getattr(seq, i)
                if repeat is not None:
                    try:
                        s = to_seq(repeat, header, get_sub_seq)
                    except (CoordOutOfBoundsError,
                            UndefinedCoordinatesError) as err:
                        LOG.warning(
                            f'{rec.name}: {err.__class__.__name__}, skipping')
                        continue

                    num_entries += 1
                    write_fasta(fasta_file, s)
    click.secho(f'Wrote {num_entries} to {fasta_file.name}', fg='green')


@extract.command()
@click.option('-r',
              '--regex',
              type=str,
              multiple=True,
              help='Regular expression to search gene and product')
@click.argument('fasta_file', type=click.File('w'))
def cds(fasta_file, regex):
    """Extract cds sequences from database."""
    LOG = logging.getLogger(__name__)

    if regex:
        LOG.info(f'Searching for phrases: {", ".join(regex)}')
    else:
        LOG.info('Extracting all cds sequences')

    LOG.info(f'writing sequences to fasta file: {fasta_file.name}')
    # compile regex
    pattern = [re.compile(r, re.I) for r in regex] if regex else [
        re.compile(r'.*'),
    ]

    num_entries = 0
    for seq in get_cds_by_regex(db, pattern):
        write_fasta(fasta_file, seq)
        num_entries += 1

    click.secho(f'Wrote {num_entries} to {fasta_file.name}', fg='green')


@main.command()
@click.pass_context
@click.argument('new_db', type=click.Path(resolve_path=True, exists=True))
@click.option(
    '-b',
    '--backup-dir',
    type=click.Path(resolve_path=True),
    default=pathlib.Path(__file__).parent.parent.joinpath('mgedb_backup'),
    help='Path to backup.',
)
@click.option('-n',
              '--dry-run',
              is_flag=True,
              help='Test run without creating new database files')
@click.option('--no-backup',
              is_flag=True,
              help='Dont create backups of current database')
def update(cli_ctx, backup_dir, new_db, no_backup, dry_run):
    """Update current MGEdb with records from another database."""
    LOG = logging.getLogger(__name__)
    if dry_run:
        LOG.info(f'Dry run, database files will not be altered')

    ctx = ExecutionContext(backup_dir)
    if not no_backup:
        backup_db(ctx, db)

    new_db = MGEdb(new_db)

    merged_records, merged_sequences = merge_records(db, new_db)

    # sanity check the mgedb structure before writing
    cattr.structure(cattr.unstructure(merged_records), MgeRecordsType)

    updt_nom = update_nomenclature(merged_records)

    # if not no_reference:
    #     LOG.info('Skip merging references')
    #     updated_refs: ReferencesType = merge_references(db, new_db)
    #     reference_path = ctx.path(db.database_path, db.references_fname)
    #     if not dry_run:
    #         write_db_file(reference_path, updated_refs)

    if not dry_run:
        # write files
        record_path = ctx.path(db.database_path, db.records_fname)
        write_db_file(record_path, merged_records)

        nomenclature_path = ctx.path(db.database_path, db.nomenclature_fname)
        write_db_file(nomenclature_path, updt_nom)

        record_seq_path = ctx.path(db.database_path, 'sequences.d',
                                   db.record_seq_fname)
        write_fasta(record_seq_path, merged_sequences)
    click.secho(f'Mge database updated: {db.database_path}', fg='green')
    cli_ctx.invoke(validate)  # validate new database upon completion


@main.command()
@click.option(
    '-b',
    '--backup-dir',
    type=click.Path(resolve_path=True),
    default=pathlib.Path(__file__).parent.parent.joinpath('mgedb_backup'),
    help='Path to backup.',
)
def backup(backup_dir):
    """Backup database."""
    ctx = ExecutionContext(backup_dir)
    backup_db(ctx, db)
    click.secho(f'Backup completed', fg='green')
