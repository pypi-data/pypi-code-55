from arrow import now
from inform import Error, comment, debug, display, error, fmt, narrate, os_error
from shlib import Run, cd, mkdir, rm, to_path, set_prefs as shlib_set_prefs
shlib_set_prefs(use_inform=True, log_cmd=True)

# today's date
date = now().format('YYYY-MM-DD')

# run a command
def run(cmd, stdin=None, modes=None):
    comment('    running:', *cmd)
    Run(cmd, stdin=stdin, modes=modes)

# run an sftp command
def run_sftp(server, cmds):
    cmd = ['sftp', '-q', '-b', '-', server]
    comment(fmt('    sftp {server}:'), '; '.join(cmds))
    try:
        Run(cmd, stdin='\n'.join(cmds), modes='sOEW')
    except KeyboardInterrupt:
        display('Continuing')
    except Error as e:
        e.reraise(culprit=server)

# test access to host
def test_access(host):
    try:
        narrate(fmt('Testing connection to {host}.'))
        payload = fmt('test payload for {host}')
        ref = to_path('.ref')
        test = to_path('.test')
        ref.write_text(payload)
        rm(test)
        run_sftp(host, [
            fmt('put {ref}'),
            fmt('get {ref} {test}'),
            fmt('rm {ref}')
        ])
        if test.read_text() == payload:
            comment('connection successful.', culprit=host)
        else:
            error('unable to connect.', culprit=host)
    except Error:
        error('unable to connect.', culprit=host)
    rm(ref, test)

# clean host
def clean(host):
    try:
        narrate(fmt('Cleaning {host}.'))
        run_sftp(host, ['rm .ssh/*.provisional'])
    except Error as e:
        if 'no such file or directory' in str(e).lower():
            comment(e)
        else:
            error('unable to connect.', culprit=host)
