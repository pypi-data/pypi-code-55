import logging

from borgmatic.execute import execute_command, execute_command_with_processes
from borgmatic.hooks import dump

logger = logging.getLogger(__name__)


def make_dump_path(location_config):  # pragma: no cover
    '''
    Make the dump path from the given location configuration and the name of this hook.
    '''
    return dump.make_database_dump_path(
        location_config.get('borgmatic_source_directory'), 'postgresql_databases'
    )


def dump_databases(databases, log_prefix, location_config, dry_run):
    '''
    Dump the given PostgreSQL databases to a named pipe. The databases are supplied as a sequence of
    dicts, one dict describing each database as per the configuration schema. Use the given log
    prefix in any log entries. Use the given location configuration dict to construct the
    destination path.

    Return a sequence of subprocess.Popen instances for the dump processes ready to spew to a named
    pipe. But if this is a dry run, then don't actually dump anything and return an empty sequence.
    '''
    dry_run_label = ' (dry run; not actually dumping anything)' if dry_run else ''
    processes = []

    logger.info('{}: Dumping PostgreSQL databases{}'.format(log_prefix, dry_run_label))

    for database in databases:
        name = database['name']
        dump_filename = dump.make_database_dump_filename(
            make_dump_path(location_config), name, database.get('hostname')
        )
        all_databases = bool(name == 'all')
        command = (
            (
                'pg_dumpall' if all_databases else 'pg_dump',
                '--no-password',
                '--clean',
                '--if-exists',
            )
            + (('--host', database['hostname']) if 'hostname' in database else ())
            + (('--port', str(database['port'])) if 'port' in database else ())
            + (('--username', database['username']) if 'username' in database else ())
            + (() if all_databases else ('--format', database.get('format', 'custom')))
            + (tuple(database['options'].split(' ')) if 'options' in database else ())
            + (() if all_databases else (name,))
            # Use shell redirection rather than the --file flag to sidestep synchronization issues
            # when pg_dump/pg_dumpall tries to write to a named pipe.
            + ('>', dump_filename)
        )
        extra_environment = {'PGPASSWORD': database['password']} if 'password' in database else None

        logger.debug(
            '{}: Dumping PostgreSQL database {} to {}{}'.format(
                log_prefix, name, dump_filename, dry_run_label
            )
        )
        if dry_run:
            continue

        dump.create_named_pipe_for_dump(dump_filename)

        processes.append(
            execute_command(
                command, shell=True, extra_environment=extra_environment, run_to_completion=False
            )
        )

    return processes


def remove_database_dumps(databases, log_prefix, location_config, dry_run):  # pragma: no cover
    '''
    Remove the database dumps for the given databases. The databases are supplied as a sequence of
    dicts, one dict describing each database as per the configuration schema. Use the log prefix in
    any log entries. Use the given location configuration dict to construct the destination path. If
    this is a dry run, then don't actually remove anything.
    '''
    dump.remove_database_dumps(
        make_dump_path(location_config), databases, 'PostgreSQL', log_prefix, dry_run
    )


def make_database_dump_pattern(
    databases, log_prefix, location_config, name=None
):  # pragma: no cover
    '''
    Given a sequence of configurations dicts, a prefix to log with, a location configuration dict,
    and a database name to match, return the corresponding glob patterns to match the database dump
    in an archive.
    '''
    return dump.make_database_dump_filename(make_dump_path(location_config), name, hostname='*')


def restore_database_dump(database_config, log_prefix, location_config, dry_run, extract_process):
    '''
    Restore the given PostgreSQL database from an extract stream. The database is supplied as a
    one-element sequence containing a dict describing the database, as per the configuration schema.
    Use the given log prefix in any log entries. If this is a dry run, then don't actually restore
    anything. Trigger the given active extract process (an instance of subprocess.Popen) to produce
    output to consume.
    '''
    dry_run_label = ' (dry run; not actually restoring anything)' if dry_run else ''

    if len(database_config) != 1:
        raise ValueError('The database configuration value is invalid')

    database = database_config[0]
    all_databases = bool(database['name'] == 'all')
    analyze_command = (
        ('psql', '--no-password', '--quiet')
        + (('--host', database['hostname']) if 'hostname' in database else ())
        + (('--port', str(database['port'])) if 'port' in database else ())
        + (('--username', database['username']) if 'username' in database else ())
        + (('--dbname', database['name']) if not all_databases else ())
        + ('--command', 'ANALYZE')
    )
    restore_command = (
        ('psql' if all_databases else 'pg_restore', '--no-password')
        + (
            ('--if-exists', '--exit-on-error', '--clean', '--dbname', database['name'])
            if not all_databases
            else ()
        )
        + (('--host', database['hostname']) if 'hostname' in database else ())
        + (('--port', str(database['port'])) if 'port' in database else ())
        + (('--username', database['username']) if 'username' in database else ())
    )
    extra_environment = {'PGPASSWORD': database['password']} if 'password' in database else None

    logger.debug(
        '{}: Restoring PostgreSQL database {}{}'.format(log_prefix, database['name'], dry_run_label)
    )
    if dry_run:
        return

    execute_command_with_processes(
        restore_command,
        [extract_process],
        output_log_level=logging.DEBUG,
        input_file=extract_process.stdout,
        extra_environment=extra_environment,
        borg_local_path=location_config.get('local_path', 'borg'),
    )
    execute_command(analyze_command, extra_environment=extra_environment)
