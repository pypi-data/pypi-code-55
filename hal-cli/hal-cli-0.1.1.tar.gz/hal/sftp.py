import stat
from pathlib import Path

from typer import Exit, confirm, progressbar
from wasabi import Printer


class SFTP:
    def __init__(self, ssh, n_files_to_warn=10):
        self.msg = Printer()
        self.sftp = ssh.open_sftp()
        self.n_files_to_warn = n_files_to_warn

    def format_paths(self, local_path, remote_path):
        local = Path(local_path).expanduser().resolve()
        remote = str(Path(remote_path).expanduser().resolve())
        return local, remote

    def looks_like_file_or_directory(self, path):
        # TODO this is hacky as hell and i HATE it - desperately needs reworking
        return "file_like" if "." in Path(path).name else "directory_like"

    def is_local_file_or_directory(self, path):
        if path.exists() and path.is_file():
            path_type = "file"
        elif path.exists() and path.is_dir():
            path_type = "directory"
        elif path.exists():
            self.msg.fail("local_path isn't a valid file or directory")
        else:
            path_type = self.looks_like_file_or_directory(path)

        return path_type

    def remote_path_exists(self, path):
        try:
            self.sftp.stat(path)
        except IOError:
            return False
        else:
            return True

    def is_remote_file_or_directory(self, path):
        try:
            remote_path_attr = self.sftp.lstat(path)
            if stat.S_ISDIR(remote_path_attr.st_mode):
                path_type = "directory"
            elif stat.S_ISREG(remote_path_attr.st_mode):
                path_type = "file"
            else:
                self.msg.fail("remote_path isn't a valid file or directory")
                raise Exit()
        except FileNotFoundError:
            path_type = self.looks_like_file_or_directory(path)

        return path_type

    def confirm_large_transfer(self, n_files):
        self.msg.warn(f"HAL is about to transfer {n_files} files.")
        if not confirm("Are you sure you want to go ahead?"):
            self.msg.fail("Aborted!")
            raise Exit()

    def recurse_remote_directory(self, remote_path):
        all_paths = []
        for path in self.sftp.listdir():
            remote_path_type = self.is_remote_file_or_directory(path)
            if remote_path_type == "directory":
                all_paths.extend(self.recurse_remote_directory(path))
            else:
                all_paths.append(path)
        return all_paths

    def walk_remote_directory(self, local_path, remote_path):
        remote_file_paths = self.recurse_remote_directory(remote_path)

        file_path_pairs = []
        for remote_file_path in remote_file_paths:
            remote_file_path_type = self.is_remote_file_or_directory(
                remote_file_path
            )
            if remote_file_path_type in ["file", "file_like"]:
                relative_path = Path(remote_file_path).relative_to(remote_path)
                local_file_path = local_path / relative_path
                file_path_pairs.append([local_file_path, remote_file_path])

        return file_path_pairs

    def walk_local_directory(self, local_path, remote_path):
        local_file_paths = local_path.rglob("*")

        file_path_pairs = []
        for local_file_path in local_file_paths:
            if local_file_path.is_file():
                relative_path = local_file_path.relative_to(local_path)
                remote_file_path = str(Path(remote_path) / relative_path)
                file_path_pairs.append((local_file_path, remote_file_path))

        return file_path_pairs

    def file_path_pairs_for_put(self, local_path, remote_path):
        with self.msg.loading("Checking paths"):
            local_path_type = self.is_local_file_or_directory(local_path)
            remote_path_type = self.is_remote_file_or_directory(remote_path)

            if local_path_type == "file" and remote_path_type in [
                "file",
                "file_like",
            ]:
                file_path_pairs = [(local_path, remote_path)]

            if local_path_type == "file" and remote_path_type in [
                "directory",
                "directory_like",
            ]:
                full_remote_path = Path(remote_path) / Path(local_path).name
                file_path_pairs = [(local_path, full_remote_path)]

            if local_path_type == "directory" and remote_path_type in [
                "file",
                "file_like",
            ]:
                self.msg.fail("Can't write a directory into a file!")
                raise Exit()

            if local_path_type == "directory" and remote_path_type in [
                "directory",
                "directory_like",
            ]:
                file_path_pairs = self.walk_local_directory(
                    local_path, remote_path
                )

        return file_path_pairs

    def file_path_pairs_for_get(self, local_path, remote_path):
        with self.msg.loading("Checking paths"):
            local_path_type = self.is_local_file_or_directory(local_path)
            remote_path_type = self.is_remote_file_or_directory(remote_path)

            if remote_path_type == "file" and local_path_type in [
                "file",
                "file_like",
            ]:
                file_path_pairs = [(local_path, remote_path)]

            if remote_path_type == "file" and local_path_type in [
                "directory",
                "directory_like",
            ]:
                full_local_path = Path(local_path) / Path(remote_path).name
                file_path_pairs = [(full_local_path, remote_path)]

            if remote_path_type == "directory" and local_path_type in [
                "file",
                "file_like",
            ]:
                self.msg.fail("Can't write a directory into a file!")
                raise Exit()

            if remote_path_type == "directory" and local_path_type in [
                "directory",
                "directory_like",
            ]:
                file_path_pairs = self.walk_remote_directory(
                    local_path, remote_path
                )

        return file_path_pairs

    def put_file(self, local_path, remote_path):
        # check whether the remote parent dir exists. if not, create it
        remote_parent_dir = str(Path(remote_path).parent)
        if not self.remote_path_exists(remote_parent_dir):
            self.sftp.mkdir(remote_parent_dir)

        pbar = ProgressBarWrapper(local_path)
        with pbar:
            self.sftp.put(
                str(local_path), str(remote_path), callback=pbar.viewBar
            )

    def get_file(self, local_path, remote_path):
        # check whether the local parent dir exists. if not, create it
        Path(local_path).parent.mkdir(exist_ok=True)

        pbar = ProgressBarWrapper(local_path)
        with pbar:
            self.sftp.get(
                str(remote_path), str(local_path), callback=pbar.viewBar
            )

    def get(self, local_path, remote_path):
        local_path, remote_path = self.format_paths(local_path, remote_path)
        file_path_pairs = self.file_path_pairs_for_get(local_path, remote_path)

        n_files = len(file_path_pairs)
        if n_files > self.n_files_to_warn:
            self.confirm_large_transfer(n_files)

        for local_file_path, remote_file_path in file_path_pairs:
            self.get_file(local_file_path, remote_file_path)
        print()
        self.msg.good(f"Successfully transferred {n_files} file(s)!")

    def put(self, local_path, remote_path):
        local_path, remote_path = self.format_paths(local_path, remote_path)
        file_path_pairs = self.file_path_pairs_for_put(local_path, remote_path)

        n_files = len(file_path_pairs)
        if n_files > self.n_files_to_warn:
            self.confirm_large_transfer(n_files)

        for local_file_path, remote_file_path in file_path_pairs:
            self.put_file(local_file_path, remote_file_path)
        print()
        self.msg.good(
            f"Successfully transferred {n_files} "
            f"file{'s' if n_files != 1 else ''}!"
        )


class ProgressBarWrapper:
    def __init__(self, local_path):
        self.progressbar = progressbar(
            [],
            label=local_path.name,
            show_percent=True,
            bar_template="%(label)s ▕%(bar)s▏ %(info)s",
            fill_char="█",
            empty_char=" ",
        )
        self.progressbar.short_limit = 0
        self.progressbar.render_finish = print()

    def viewBar(self, bytes_transferred, bytes_to_transfer):
        self.progressbar.length = bytes_to_transfer
        self.progressbar.update(bytes_transferred - self.progressbar.pos)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False
