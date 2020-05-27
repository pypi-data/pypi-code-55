import os
import platform
import subprocess
import sys
from pathlib import Path
import re
from typing import List

import os_release


def log_debug(msg):
    if 'CCM_JAVA8_DEBUG' in os.environ:
        print(msg, file=sys.stderr)


def get_java_env():
    (java_bin_path, loc) = (f'{os.environ["JAVA_HOME"]}/bin/java', 'in JAVA_HOME') if 'JAVA_HOME' in os.environ else ('java', 'on PATH')

    try:
        current_version = subprocess.check_output([java_bin_path, '-version'], stderr=subprocess.STDOUT).decode('utf-8').split('\n')[0]
        if 'version "1.8.' in current_version:
            return {}

        log_debug(f'Java {loc} is: {current_version}.')

    except (subprocess.CalledProcessError, FileNotFoundError):
        log_debug(f'Java not found {loc}')
        pass

    system = platform.system()

    if system == 'Darwin':  # ie, macOS (for all intents and purposes)
        return {
            'JAVA_HOME': subprocess.check_output(['/usr/libexec/java_home', '-v', '1.8']).decode('utf-8').strip()
        }

    elif system == 'Linux':
        current_release = os_release.current_release()

        def handle_jvms(jvms: List, type) -> dict:
            jvms = [str(jvm) for jvm in jvms]

            if len(jvms) > 1:
                log_debug(f'Found multiple Java 8 {type}s: {dict(enumerate(jvms, start=1))}. Using the first {type}.')

            elif len(jvms) == 0:
                raise Exception(f'Java 8 {type} not found.')

            return {
                'JAVA_HOME': jvms[0]
            }

        if current_release.is_like('arch'):  # Arch Linux (and derivatives)
            installs = list(Path('/usr/lib/jvm').glob("java-8*"))

            return handle_jvms(installs, 'installation')

        elif current_release.is_like('debian'):  # Debian-based distros (any that uses `update-alternatives`)
            alternatives = subprocess.check_output(['update-alternatives', '--list', 'java']).decode('utf-8').split('\n')
            alternatives = [alt.strip('/bin/java') for alt in alternatives if "-8-" in alt]

            return handle_jvms(alternatives, 'alternative')

        elif current_release.is_like('rhel'):  # RHEL-based distros
            alternatives = subprocess.check_output(['alternatives', '--display', 'java']).decode('utf-8').split('\n')

            regex = re.compile(r'^(?P<path>/usr/lib/jvm/.*(-8-|-1.8.0-).*)/bin/java.*')

            alternatives = [match.group('path') for match in filter(None, map(regex.match, alternatives))]

            return handle_jvms(alternatives, 'alternative')

        else:
            raise Exception(f'Automatic Java 8 environment configuration not available for this distribution ({current_release.id}).')

    # TODO: implement other platform support here

    else:
        raise Exception(f'Automatic Java 8 environment configuration not available for this platform ({system}).')


def set_java_env():
    env = get_java_env()
    log_debug(f'New Java 8 environment: {env}')
    os.environ.update(env)


if __name__ == '__main__':
    os.environ['CCM_JAVA8_DEBUG'] = 'please'
    set_java_env()
