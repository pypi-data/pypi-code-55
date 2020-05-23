import datetime

from . import data
from . import settings


class UnknownMunicipality(Exception):
    pass


def _parse_line(l):
    tokens = l.split()
    return " ".join(tokens[:-1]), int(tokens[-1].rstrip("\u200b"))


def _proto_dataset(text):
    min_date = max(
        settings.FIRST_REPORT_WITH_MUNICIPAL_DATA, settings.FIRST_SUPPORTED_REPORT
    )
    max_date = max(text)
    date_range = [
        min_date + datetime.timedelta(d) for d in range((max_date - min_date).days + 1)
    ]
    return {m: {d: 0 for d in date_range} for m in data.MUNICIPALITIES}


def _is_interesting_line(l):
    return (
        not any(ignore_pattern in l for ignore_pattern in settings.IGNORE_LINE_PREFIXES)
        and l != ""
    )


def _is_number(t):
    try:
        int(t.rstrip("\u200b"))
        return True
    except ValueError:
        return False


def _filter_uninteresting_lines(text):
    lines = [l.strip() for l in text.split("\n")]
    interesting_lines = []
    for l in lines:
        if _is_interesting_line(l):
            interesting_lines.append(l)
            if l.startswith(settings.LAST_MUNICIPALITY):
                break
    return interesting_lines


def _extract_counts(lines):
    counts = []
    leftovers = []
    for l in lines:
        tokens = l.split()
        last_token = tokens[-1]
        if _is_number(last_token):
            counts.append(int(last_token.rstrip("\u200b")))
            if len(tokens) > 1:
                leftovers.append(" ".join(tokens[:-1]))
        else:
            leftovers.append(l)
    return counts, leftovers


def _coalesce_lines(lines):
    counts, leftovers = _extract_counts(lines)
    coalesced = []
    i = 0
    while i < len(leftovers):
        l = _normalize_municipality(leftovers[i])
        if l not in data.MUNICIPALITIES and len(leftovers[i + 1].split()) == 1:
            coalesced.append(" ".join([l, leftovers[i + 1]]))
            i += 2
        else:
            coalesced.append(l)
            i += 1

    return [" ".join([m, str(c)]) for m, c in zip(coalesced, counts)]


def _text_to_lines(text):
    interesting_lines = _filter_uninteresting_lines(text)
    return _coalesce_lines(interesting_lines)


def _normalize_municipality(m):
    m = (
        m.replace("Fig.", "Figueira")
        .replace("V.", "Vila")
        .replace("R.", "Real")
        .replace("Reg.", "Reguengos")
        .replace("Sta.", "Santa")
        .replace("St", "Santa")
        .replace("Carraz.", "Carrazeda")
        .replace("Cast.", "Castelo")
        .replace("Mac.", "Macedo")
        .replace("N.", "Nova")
        .replace("S.", "Santo")
    )
    subs = [
        ("Vila Nova Barquinha", "Vila Nova da Barquinha"),
        ("Vila Nova Cerveira", "Vila Nova de Cerveira"),
        ("Vila Nova Famalicão", "Vila Nova de Famalicão"),
        ("Vila Real Santo António", "Vila Real de Santo António"),
        ("Reguengos Monsaraz", "Reguengos de Monsaraz"),
        ("Salvaterra Magos", "Salvaterra de Magos"),
        ("Santa Maria Feira", "Santa Maria da Feira"),
        ("Vila Praia da Vitória", "Vila da Praia da Vitória"),
        ("Santa Marta Penaguião", "Santa Marta de Penaguião"),
        ("Carrazeda Ansiães", "Carrazeda de Ansiães"),
    ]
    for s in subs:
        m = m.replace(*s)
    if m == "Pedrógão":
        m = "Pedrógão Grande"
    tokens = m.split()
    return " ".join([t for t in tokens if not t.startswith("(")])


def from_text(report_texts):
    dataset = _proto_dataset(report_texts)
    for d, t in report_texts.items():
        try:
            lines = _text_to_lines(t)
            for l in lines:
                try:
                    m, count = _parse_line(l)
                except Exception:
                    raise
                municipality = _normalize_municipality(m)
                if not municipality in dataset:
                    raise UnknownMunicipality(f"{d}: {municipality}")
                dataset[municipality][d] = count
        except Exception:
            break
    return dataset
