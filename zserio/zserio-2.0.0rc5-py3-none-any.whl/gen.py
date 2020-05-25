import os
import subprocess
import sys
import shutil


class JavaNotFoundException(Exception):
    """
    This exception is raised if the Java executable is not found
    either through $JAVA_HOME or $PATH.
    """
    def __init__(self):
        super(self).__init__("Java was not found (checked $JAVA_HOME and $PATH).")


zs_jar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zserio.jar")
java_path = None


def find_java():
    global java_path
    if java_path:
        return java_path
    java_path = os.getenv("JAVA_HOME", None)
    if java_path:
        java_path = os.path.join(java_path, "bin/java")
        print(f"Using Java at {java_path} (found through JAVA_HOME).")
    else:
        java_path = shutil.which("java")
        if java_path:
            print(f"Using Java at {java_path} (found through PATH).")
        else:
            raise JavaNotFoundException()
    return java_path


def generate(src_file: str = "", module_name: str = "") -> None:
    """
    Description:

        Translate zserio code to python, and add the generated package
        to pythonpath. The generated sources will be placed under
        <src_file.zs>/../.zs-python-package[/module_name]. This path
        will be added to `sys.path`.

        The `module_name` argument allows to set a top-level python module name,
        under which the generated sources will be placed.

    Possible exceptions:

        `zserio.JavaNotFoundException`: Java was not found,
          therefore zserio.jar cannot be called.

        `subprocess.CalledProcessError`: Raised if
          `java -jar zserio.jar ...` produced a non-zero returncode.

    Examples:

        With top-level package:
            ```
            import zserio
            zserio.generate("myfile.zs", "mypackage")
            from mypackage.myfile import *
            ```

        Without top-level package:
            ```
            import zserio
            zserio.generate("myfile.zs")
            from myfile import *
            ```

    :param src_file: Source zserio file.
    :param module_name: (Optional) Top-level package directory name.
    :return: True if succesfull, False otherwise.
    """
    global zs_jar_path
    zs_pkg_path = os.path.dirname(os.path.abspath(src_file))
    zs_build_path = os.path.join(zs_pkg_path, ".zs-python-package")
    subprocess.run([
        find_java(), "-jar", zs_jar_path,
        "-src", zs_pkg_path,
        "-python", zs_build_path,
        *(("-setTopLevelPackage", module_name) if module_name else tuple()),
        os.path.basename(src_file)],
        check=True)
    if zs_build_path not in sys.path:
        sys.path.append(zs_build_path)
