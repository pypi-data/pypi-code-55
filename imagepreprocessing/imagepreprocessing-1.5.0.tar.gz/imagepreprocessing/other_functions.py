def __run_shell_command(command):
    import subprocess
    output = subprocess.check_output(command, shell=True).decode("ascii")
    return output
