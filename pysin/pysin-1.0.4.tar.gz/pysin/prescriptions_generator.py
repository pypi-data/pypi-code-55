import os
from fpdf import FPDF
from faker import Factory
from random import randint, choice
import pandas as pd
from unidecode import unidecode
from path import Path
from warnings import simplefilter

simplefilter("ignore")

MEDIC = [
    "DOLIPRANE",
    "DAFALGAN",
    "IMODIUM",
    "SPASFON",
    "TAHOR",
    "SPEDIFEN",
    "VOLTARENE",
    "ELUDRIL",
    "IXPRIM",
    "PARACETAMOL BIOGARAN",
    "FORLAX",
    "MAGNE B6",
    "HELICIDINE",
    "CLAMOXYL",
    "PIASCLEDINE",
    "LAMALINE",
    "GAVISCON",
    "DAFLON",
    "ANTARENE",
    "RHINOFLUIMUCIL",
    "PLAVIX",
    "MOPRAL",
    "SUBUTEX",
    "AERIUS",
    "ORELOX",
    "INEXIUM",
    "METEOSPASMYL",
    "AUGMENTIN",
    "TOPLEXIL",
    "PIVALONE",
    "VASTAREL",
    "ADVIL",
    "EUPANTOL",
    "DEXERYL",
    "RENUTRYL 500",
    "XANAX",
    "EMLAPATCH",
    "LASILIX",
    "ENDOTELON",
    "DEROXAT",
    "TEMESTA",
    "EFFEXOR",
    "PARACETAMOL SANDOZ",
    "VENTOLINE",
    "SOLUPRED",
    "DEXTROPROPOXYPHENE PARAC BIOG",
    "PNEUMOREL",
    "INIPOMP",
    "PREVISCAN",
    "ASPEGIC",
    "GINKOR",
    "CRESTOR",
    "MEDIATOR",
    "SERESTA",
    "MOTILIUM",
    "PARACETAMOL MERCK",
    "CELESTENE",
    "AMLOR",
    "DIAMICRON",
    "TANAKAN",
    "ATARAX",
    "DERINOX",
    "XYZALL",
    "DEXTROPROPOXYPHENE PARAC SAND",
    "SERETIDE",
    "COVERSYL",
    "PROPOFAN",
    "HEXAQUINE",
    "APROVEL",
    "PARIET",
    "ZALDIAR",
    "DIPROSONE",
    "PARACETAMOL TEVA",
    "BETADINE",
    "LYSANXIA",
    "ALODONT",
    "LEXOMIL",
    "DACRYOSERUM",
    "FUCIDINE",
    "STILNOX",
    "KETUM",
    "STABLON",
    "ART",
    "BIOCALYPTOL",
    "THIOVALONE",
    "DEBRIDAT",
    "PYOSTACINE",
    "TIORFAN",
    "SPECIAFOLDINE",
    "OGAST",
    "RIVOTRIL",
    "TOPALGIC",
    "NASONEX",
]

POSO_TYPE = ["cp", "injections", "comprimés"]

POSO_FREQ = [
    "le matin",
    "le soir",
    "matin, midi et soir",
    "avant les repas",
    "après les repas",
    "par jour",
]

POSO_DURATION = [f"pendant {n} jours" for n in {3, 5, 7, 10, 15, 30}] + ["si douleur"]

MONTHS = [
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
]

FONTS_FOLDER_PATH = Path(os.path.dirname(__file__)) / "utils/fonts/"

SIGNATURE_FONTS = [
    FONTS_FOLDER_PATH / name
    for name in os.listdir(FONTS_FOLDER_PATH)
    if name.endswith(".ttf")
]

MAIN_FONTS = ["Arial", "Courier", "Helvetica", "Times"]

fake = Factory.create("fr_FR")


def add_block(pdf, txt, align="L"):
    """Adds paragraph to the pdf object

    Arguments:
        pdf {fpdf.fpdf.FPDF} -- current pdf object
        txt {str} -- paragraph to add

    Keyword Arguments:
        align {str} -- text alignment : the possible values are "L", "C" and "R" (default: {"L"})
    """

    for row in txt.split("\n"):
        pdf.cell(200, 5, txt=row, ln=1, align=align)


def signature(name):
    """Creates a fake signature

    Arguments:
        name {str} -- person name

    Returns:
        str -- signature
    """

    name_list = unidecode(name).split(" ")
    sign = ""
    for w in name_list[:-1]:
        if randint(0, 1):
            if randint(0, 1):
                sign += w[0]
            else:
                sign += w
            if randint(0, 1):
                sign += " "
    sign += name_list[-1]
    return sign


def prescription_generator(output_path, patient_name, year):
    """Generates a fake medical prescription

    Arguments:
        output_path {Path} -- path the ouput pdf file
        patient_name {str} -- patient name to use
        year {int} -- year of the prescription
    """

    pdf = FPDF(format="A4")
    pdf.add_page()
    font = choice(MAIN_FONTS)
    pdf.set_font(font, size=11)

    # En-tête

    txt = f"""À {fake.city()}, le {randint(2, 28)} {choice(MONTHS)} {year}     
    
    
    
    """
    add_block(pdf, txt, align="R")

    # Centre médical

    city = fake.city()
    postal_code = randint(1000, 10000) * 10

    txt = f"""
Centre Médical de {city}
{fake.street_address()}
{postal_code} {city}
{fake.phone_number()}


"""
    pdf.set_font(font, "B", size=11)
    add_block(pdf, txt, align="C")
    pdf.set_font(font, size=11)

    # Docteur

    doctor_name = fake.name()
    postal_code = randint(1000, 10000) * 10

    txt = f"""
        Docteur {doctor_name}
        {fake.street_address()}
        {postal_code} {fake.city()}
        Tél. : {fake.phone_number()}

"""
    add_block(pdf, txt)

    # Patient

    txt = f"""
        {patient_name}
        {randint(12, 100)} ans, {randint(30, 110)} kg

    """

    add_block(pdf, txt)

    # Prescription

    nb_medics = randint(1, 5)
    for _ in range(nb_medics):

        txt = f"""
        {choice(MEDIC)} {5 * randint(1, 10)} mg"""

        pdf.set_font(font, "B", size=11)
        add_block(pdf, txt)

        txt = f"""          {randint(1, 3)} {choice(POSO_TYPE)} {choice(POSO_FREQ)} {choice(POSO_DURATION)}
"""

        pdf.set_font(font, size=11)
        add_block(pdf, txt)

    # Signature

    pdf.add_font("Signature", "", choice(SIGNATURE_FONTS), uni=True)
    font_size = randint(20, 40)
    pdf.set_font("Signature", size=font_size)

    txt = f"""


{signature(doctor_name)}          {int((40 - font_size)/20) * randint(0, 20) * ' '}
"""
    add_block(pdf, txt, align="R")

    pdf.output(output_path)


def get_id():
    """Generates a random 6-digit id

    Returns:
        str -- random 6-digit id
    """

    return str(randint(1000, 100000)).zfill(6)


def generate(nb, output_path):
    """Generate several fake medical prescriptions

    Arguments:
        nb {int} -- number or fake medical prescriptions to generate
        output_path {str} -- folder to store the fake medical prescriptions in
    """

    output_path = Path(output_path)

    link = pd.DataFrame(
        columns=[
            "patient_id",
            "patient_surname",
            "patient_name",
            "date_folder",
            "prescription_id",
        ]
    )

    print("Generating data...")

    for i in range(nb):

        print(f"Loading : {int(100 * i / nb)} %", end="\r")

        patient_id = get_id()
        while not link[lambda row: row["patient_id"] == patient_id].empty:
            patient_id = get_id()

        prescription_id = get_id()
        while not link[lambda row: row["prescription_id"] == prescription_id].empty:
            prescription_id = get_id()

        patient_name = fake.first_name()
        patient_surname = fake.last_name()
        year = str(randint(2010, 2019))

        link = link.append(
            {
                "patient_id": patient_id,
                "patient_surname": patient_surname,
                "patient_name": patient_name,
                "date_folder": year,
                "prescription_id": prescription_id,
            },
            ignore_index=True,
        )

        if not os.path.isdir(output_path / year):
            os.mkdir(output_path / year)

        prescription_generator(
            f"{output_path}/{year}/prescription_{prescription_id}.pdf",
            patient_name + " " + patient_surname,
            year,
        )

    link.to_csv(output_path / "index.csv")

    print("Generation terminated !")
