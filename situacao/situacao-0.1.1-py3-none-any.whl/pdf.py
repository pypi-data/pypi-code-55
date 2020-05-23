import pdftotext

from . import util


def extract_text(reports):
    text = {}
    for d in reports:
        p = util.report_filename(d)
        with open(p, "rb") as f:
            pdf = pdftotext.PDF(f, raw=True)
            try:
                text[d] = pdf[2]
            except Exception:
                continue
    return text
