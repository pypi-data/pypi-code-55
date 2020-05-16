import argparse
import crypt
import distro
import getpass
import os
import os.path
import paramiko
import pwd
import random
import string
import subprocess
import sys
import tempfile

import logging
from _socket import AF_ALG
logger = logging.getLogger(__name__)

def main(argv=sys.argv):
    command = SaltBootstrapSSH(argv)
    try:
        return command.run()
    except KeyboardInterrupt:
        return 1

class SaltBootstrapSSH:
    
    parser = argparse.ArgumentParser(
        description="""\
Bootstrap key based SSH authentication to a Salt Master

This streamlines the effort to enable a Salt master to use salt-ssh on a minion.
This script should be run on a minion you would like to control via a named
Salt master.

You will be prompted for a Salt master SSH password unless the
SALT_BOOTSTRAP_SSH_MASTER_PASSWD environment variable is set.

Supports recent (systemd based) versions of Ubuntu and Redhat.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Shortcut to enable all script options.  This infers '
        '--install-ssh, --enable-ssh, --create-user, and --grant-sudo',
    )
    parser.add_argument(
        '--install-ssh',
        action='store_true',
        help='Install a local ssh server if needed.  The will leverage the '
        'local package management system.',
    )
    parser.add_argument(
        '--enable-ssh',
        action='store_true',
        help='Enable local ssh server if needed.  The will leverage the '
        'local service manager.',
    )
    parser.add_argument(
        '--user',
        action='store',
        default=getpass.getuser(),
        help='Named user to bootstrap, defaults to current user.'
        '(i.e. current user)',
    )
    parser.add_argument(
        '--create-user',
        action='store_true',
        help='Create named user if needed.  User created will have '
        'a randomly generated large complex password assigned with '
        '/home/{user} home directory and /bin/bash shell',
    )
    parser.add_argument(
        '--grant-sudo',
        action='store_true',
        help='Named user will be added to /etc/sudoers with NOPASSWD '
        'privilege (e.g. the user can leverage sudo without providing'
        'a password',
    )
    parser.add_argument(
        '--master-ssh-user',
        action='store',
        default='root',
        help='The user to authenticate to Salt master with.  This user'
        'should either have access to the Salt master PKI directory, or'
        'have sudo capabilities to cat the Salt master public RSA key',
    )
    parser.add_argument(
        '--master-pki-dir',
        action='store',
        default='/etc/salt/pki/master',
        help='The base Salt PKI directory on the Salt master.  The master'
        'RSA public key will be referenced from here.',
    )
    parser.add_argument(
        'salt_master',
        help='The hostname or IP address of the Salt master to bootstrap '
        'against',
    )
    
    def _add_authorized_key(self):
        sftp, transport = None, None
        try:
            transport = paramiko.Transport((self.args.salt_master, 22))
            self._print(
                "Attempting to connect to {} as {}".format(
                    self.args.salt_master, self.args.master_ssh_user))
            transport.connect(None, 
                              self.args.master_ssh_user, self.master_ssh_passwd)
            filepath = self.args.master_pki_dir + "/ssh/salt-ssh.rsa.pub"
            self._print("Attempting to download Master ssh public key at {}".format(filepath))
            sftp = paramiko.SFTPClient.from_transport(transport)
            key_file = tempfile.NamedTemporaryFile()
            localpath = key_file.name
            sftp.get(filepath,localpath) #we now have the key_file
        
        except Exception as e:
            self._print("error downloading Master ssh public key file: {}".format(e))
            exit(1)
            
        finally:
            if sftp: sftp.close()
            if transport: transport.close()
        
        #add to authorized keys, if needed
        try:
            authorized_keys_path = pwd.getpwnam(self.args.user).pw_dir + '/.ssh/authorized_keys'
            if os.path.isfile(authorized_keys_path):
                with open(authorized_keys_path) as f:
                    authorized_keys = f.readlines()
            else:
                #create missing file
                open(authorized_keys_path, 'a').close()
                authorized_keys = []
            key = key_file.readline().decode('ascii')
            
            if key not in authorized_keys:
                authorized_keys.append(key)
                with open(authorized_keys_path, 'a') as f:
                    f.write(key)
                self._print("Salt master public ssh key added to authorized_keys for user {}".format(self.args.user))
            else:
                self._print("Found existing entry in authorized_keys.")
        except Exception as e:
            logger.exception(e)
            self._print("unknown error occurred while checking authorized_keys file: {}".format(e))
            exit(1)

    def __init__(self, argv, quiet=False):
        self.args = self.parser.parse_args(argv[1:])
        self.quiet = quiet
        self.master_ssh_passwd = os.getenv('SALT_BOOTSTRAP_SSH_MASTER_PASSWD')
        if not self.master_ssh_passwd:
                self.master_ssh_passwd = getpass.getpass(
                    'Salt master {} ssh password for {}: '.format(
                        self.args.salt_master, self.args.master_ssh_user))
        
    def run(self):
        if self.args.install_ssh or self.args.all:
            self._install_ssh()
        if self.args.enable_ssh or self.args.all:
            self._enable_ssh()
        if self.args.create_user or self.args.all:
            self._create_user()
        if self.args.grant_sudo or self.args.all:
            self._grant_sudo()
        self._add_authorized_key()
    
    def _print(self, message):
        if not self.quiet:
            print(message)
    
    def _exit(self, code, message=''):
        self._print(message)
        exit(code)
    
    def _install_ssh(self):
        if distro.id() in ['ubuntu', 'debian']:
            cp = self._install_ssh_apt()
            if cp:
                cp.returncode and \
                    self._exit(1, 
                               'ssh installation error: {}'.format(cp.stdout))
            else:
                self._print("ssh package already installed.")
        else: # ['centos', 'redhat', 'fedora']:
            cp = self._install_ssh_yum()
            if cp:
                cp.returncode and \
                    self._exit(1, 
                               'ssh installation error: {}'.format(cp.stdout))
            else:
                self._print("ssh package already installed.")
            
    def _install_ssh_apt(self):
        #check if package is installed already
        cp = subprocess.run(['dpkg','-l','ssh'], stdout=subprocess.DEVNULL)
        if cp.returncode:
            self._print("Attempting to install ssh package.")
            return subprocess.run(['apt-get','install','ssh'],
                                  capture_output=True)
    
    def _install_ssh_yum(self):
        #check if package is installed already
        cp = subprocess.run(['yum','list','installed', 'openssh'], 
                                                    stdout=subprocess.DEVNULL)
        if cp.returncode:
            self._print("Attempting to install ssh package.")
            return subprocess.run(['yum','install','openssh'],
                                  capture_output=True)
    
    def _enable_ssh(self):
        pkg_name = 'ssh'
        if distro.id() in ['centos', 'redhat', 'fedora']:
            pkg_name = 'sshd'
        #enable service if needed
        cp = subprocess.run(['systemctl','is-enabled',pkg_name], 
                                                    stdout=subprocess.DEVNULL)
        if cp.returncode:
            self._print("Attempting to enable ssh daemon.")
            cp = subprocess.run(['systemctl','enable',pkg_name],
                                  capture_output=True)
            cp.returncode and \
                self._exit(1, 
                           'ssh service enable error: {}'.format(cp.stdout))
        else:
            self._print("ssh service already enabled.")
            
        #start service if needed
        cp = subprocess.run(['systemctl','is-active',pkg_name], 
                                                    stdout=subprocess.DEVNULL)
        if cp.returncode:
            self._print("Attempting to start ssh daemon.")
            cp = subprocess.run(['systemctl','start',pkg_name],
                                  capture_output=True)
            cp.returncode and \
                self._exit(1, 
                           'ssh service start error: {}'.format(cp.stdout))
        else:
            self._print("ssh service already started.")
    
    def _create_user(self):
        self._print("Looking for /etc/passwd entry for user {}".format(self.args.user))
        for pwd_entry in pwd.getpwall():
            if self.args.user == pwd_entry.pw_name:
                return self._print("Found existing user {}".format(self.args.user))
        self._print("Attempting to create new system user {}.".format(self.args.user))
        cp = subprocess.run(['useradd','-s', '/bin/bash', '-d', 
                             '/home/{}'.format(self.args.user),
                             '-m', '{}'.format(self.args.user)])
        cp.returncode and \
                self._exit(1, 
                           'user creation error: {}'.format(cp.stdout))
        self._print("User created: {}".format(self.args.user))
        self._print("Attempting to update password for user {}.".format(self.args.user))
        passwd = self._generate_password()
        passwd_crypt = crypt.crypt(passwd)
        p = subprocess.Popen(['chpasswd','-e'], stdout=subprocess.PIPE,
                                                stdin=subprocess.PIPE, 
                                                stderr=subprocess.PIPE)
        chpasswd_input = '{}:{}'.format(self.args.user, passwd_crypt)
        p_stdout = p.communicate(input=chpasswd_input.encode())[0]
        p.returncode and \
                self._exit(1, 
                           'password update error: {}'.format(p_stdout))
        self._print("Password updated: {}".format(self.args.user))
    
    def _generate_password(self, length=32):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*'
        passwd = ''
        
        for c in range(length):
            passwd += random.choice(chars)
        return passwd or self._exit('unknown error generating random password')

    def _grant_sudo(self):
        cp = subprocess.run(['grep','{}'.format(self.args.user), '/etc/sudoers'], 
                                                    stdout=subprocess.DEVNULL)
        if cp.returncode:
            self._print(
                "Attempting to grant sudo for user: {}".format(self.args.user))
        
            sudoers = open('/etc/sudoers', 'a')
            sudoers.write("{} ALL=(ALL:ALL) NOPASSWD:ALL\n".format(self.args.user))
            sudoers.close()
            self._print("User granted sudo: {}".format(self.args.user))
            
        else:
            self._print("user already granted sudo: {}".format(self.args.user))
if __name__ == '__main__':
    sys.exit(main() or 0)