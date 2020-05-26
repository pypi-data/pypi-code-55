import nox

FILEPATHS = ["noxfile.py", "setup.py", "__NAME__", "tests"]


@nox.session(python="3.7")
def lint(session):
    """run linters"""
    session.install("black")
    session.run("black", "--check", "--line-length", "100", *FILEPATHS)


@nox.session(python="3.7")
def reformat(session):
    """reformat src files"""
    session.install("black")
    session.run("black", "--line-length", "100", *FILEPATHS)


@nox.session(python="3.7")
def test(session):
    session.run("pip", "install", "-e", ".")
    session.run("pip", "install", "-r", "requirements.txt")
    session.install("pytest")
    session.run("pytest")
