from datetime import date
from pathlib import Path
import os


URL = "https://covid19.min-saude.pt/relatorio-de-situacao/"
LINK_TEXT_PREFIX = "Relatório de Situação nº "
CACHE_DIR = os.path.join(Path.home(), ".situacao", "cache")
FIRST_REPORT_WITH_MUNICIPAL_DATA = date(2020, 3, 24)
FIRST_SUPPORTED_REPORT = date(2020, 4, 9)
IGNORE_LINE_PREFIXES = (
    "RELATÓRIO",
    "NOVO",
    "COVID",
    "CARACTERIZAÇÃO",
    "Notas",
    "apresentados",
    "Dados",
    "Atualizado",
    "CONCELHO",
    "NÚMERO",
    "DE CASOS",
    "CASOS",
    "por ordem alf",
    "alfabética",
    "A informação",
)
LAST_MUNICIPALITY = "Vouzela"
MUNICIPALITIES_PATH = "m.txt"
