import os
import getpass
import shlex
import click
import paramiko

@click.command()
@click.option("-h", "--host", help="required.")
@click.option("-P", "--port", type=int, default=22, help="default to 22.")
@click.option("-u", "--user", default="root", help="default to root.")
@click.option("-i", "--private-key", default=os.path.abspath(os.path.expanduser("~/.ssh/id_rsa")), help="default to ~/.ssh/id_rsa")
@click.option("-p", "--password", help="NO password means using public key auth.")
@click.argument("command", nargs=-1)
def sshrun(host, port, user, private_key, password, command):
    """Run command on remote server via ssh channel.

    Example:
    
    1. Create ssh channel by user and password, and then run the command:

        sshrun -h SERVER -P port -u root -p PASSWORD -- ping -c 4 127.0.0.1

    2.  Create ssh channel by user test and the given private key, and then run the command:

        sshrun -h SERVER -P port -u test -i ~/.ssh/id_rsa -- echo hi

    3. Create ssh channel by user root and the default private key, and then run the command:

        sshrun -h SERVER -- echo hello

    Note:

    "--" means all arguments after "--" are options or arguments of the command

    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if password:
            ssh.connect(host, port, user, password)
        else:
            rsa_key = paramiko.RSAKey.from_private_key_file(private_key)
            ssh.connect(host, port, user, pkey=rsa_key)
        stdin, stdout, stderr = ssh.exec_command(" ".join(map(shlex.quote, command)))
        os.sys.stdout.buffer.write(stdout.read())
    except Exception as error:
        print(error)

if __name__ == "__main__":
    sshrun()
