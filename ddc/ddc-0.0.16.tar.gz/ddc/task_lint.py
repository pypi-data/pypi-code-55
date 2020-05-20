from ddc.utils import stream_exec_cmd


def start_lint(cwd, lang):
    stream_exec_cmd("docker run --rm -v {cwd}:/usr/app apisgarpun/pronto-linter-{lang}".format(
        cwd=cwd,
        lang=lang
    ))
