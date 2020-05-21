import re

from . import default_path
from ...errors import EopError


def read_table(subdir, elements):
    """Read IAU2000 tables:
        - 5.2a, 5.2b and 5.2d
        - 5.3a and 5.3b
    """

    pattern_j = "^j = (\d)  Number of terms = (\d*)$"
    pattern = "^\s*(\d*)\s*(\-?\d+.?\d*\s*)\s*(\-?\d+.?\d*\s*)\s*(\-?\d*\s*){14}$"

    out = []
    for element in elements:

        filepath = default_path / subdir / element

        total = []
        block = []
        n_terms_exp = 0
        with filepath.open() as fhd:
            lines = fhd.read().splitlines()
            for line in lines:
                line = line.strip()

                m_j = re.search(pattern_j, line)
                if m_j:
                    n_terms = len(block)
                    if n_terms_exp != n_terms:
                        raise EopError("Did not read the expected number of terms. Expected {} read {}".format(n_terms_exp, n_terms))
                    if block:
                        total.append(block)
                        block = []
                    n_terms_exp = int(m_j.group(2))
                else:
                    m = re.search(pattern, line)
                    if m:
                        values = line.split()
                        if len(values) > 0:
                            fields = [int(values[0])]
                            fields[1:3] = [float(x) for x in values[1:3]]
                            fields[3:] = [int(x) for x in values[3:]]
                            block.append(fields)
            if block:
                n_terms = len(block)
                if n_terms_exp != n_terms:
                    raise EopError(
                        "Did not read the expected number of terms. Expected {} read {}".format(n_terms_exp, n_terms))
                total.append(block)
        out.append(total)
    return out
