import re
from methinks.section import RE_SPLIT_SECTIONS


def parse_sections(text, triggers):

    reg = re.compile(RE_SPLIT_SECTIONS, re.MULTILINE | re.DOTALL)

    sections = []
    for match in reg.finditer(text):
        section, title = match['section'], match['title']
        title = title.strip()
        sec = triggers[title].from_text(section)
        sections.append(sec.propagate())
    return sections
