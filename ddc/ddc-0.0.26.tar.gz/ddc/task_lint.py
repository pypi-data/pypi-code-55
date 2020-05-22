from ddc.utils import stream_exec_cmd, run_if_time_has_passed


def start_lint(cwd, lang):
    image_tag = "apisgarpun/pronto-linter-{lang}".format(lang=lang)

    def _pull():
        stream_exec_cmd("docker pull {image_tag}".format(image_tag=image_tag))

    run_if_time_has_passed("lint-" + lang, 10, _pull)
    exit_code, max_output = stream_exec_cmd(
        "docker run --rm -v {cwd}:/usr/app {image_tag}".format(
            cwd=cwd, image_tag=image_tag
        )
    )

    new_output = []
    cwd_prefix = cwd if cwd.endswith("/") else cwd + "/"
    for line in max_output.split("\n"):
        if str(line).startswith("./"):
            line = cwd_prefix + line[2:]
        new_output.append(line)
    return exit_code, "\n".join(new_output)
