# Note that we need to fall back to the hard-coded version if either
# setuptools_scm can't be imported or setuptools_scm can't determine the
# version, so we catch the generic 'Exception'.
try:
    from setuptools_scm import get_version
    version = get_version(root='..', relative_to=__file__)
except Exception:
    version = '4.1rc1'
else:
    del get_version  # clean up namespace


# We use LooseVersion to define major, minor, micro, but ignore any suffixes.
def split_version(version):
    pieces = [0, 0, 0]

    try:
        from distutils.version import LooseVersion

        for j, piece in enumerate(LooseVersion(version).version[:3]):
            pieces[j] = int(piece)

    except Exception:
        pass

    return pieces


major, minor, bugfix = split_version(version)

del split_version  # clean up namespace.

release = 'dev' not in version
