import os
from ddc.utils import stream_exec_cmd, __build_path


def start_test(cwd: str, lang: str, save_test_results: bool = False):
    all_output = []
    exit_code = -1
    try:
        if lang == "py":
            image_tag: str = "ddc_local/tmp:latest"
            exit_code, mix_output = stream_exec_cmd(
                "docker build -t " + image_tag + " " + cwd
            )
            if exit_code:
                all_output.append("DDC: Build docker image for test")
                all_output.append(mix_output)

                raise StopIteration()

            rwmeta_path = __build_path("/.rwmeta/")

            if not os.path.exists(cwd + "/tests"):
                all_output.append("DDC: Directory /tests is not exists")
                raise StopIteration()

            all_output.append("DDC: Run tests")
            mounts = [
                "-v {rwmeta_path}:/root/.rwmeta".format(rwmeta_path=rwmeta_path),
                "-v {cwd}/test-reports:/usr/app/test-reports".format(cwd=cwd),
            ]
            pytest_args = "--reruns 2"
            if save_test_results:
                pytest_args += (
                    " -o junit_family=xunit2 --junitxml=/usr/app/test-reports/tests.xml"
                )
            exit_code, mix_output = stream_exec_cmd(
                "docker run --rm {mounts} {image_tag} pytest ./tests {pytest_args}".format(
                    image_tag=image_tag,
                    mounts=" ".join(mounts),
                    pytest_args=pytest_args,
                )
            )

            all_output.append(mix_output)
            if exit_code:
                raise StopIteration()

    except StopIteration:
        pass
    return exit_code, "\n".join(all_output)


if __name__ == "__main__":
    exit_code2, mix_output2 = start_test(
        "/Users/arturgspb/PycharmProjects/api-billinginternal", "py"
    )

    print(mix_output2)
    print(exit_code2)
