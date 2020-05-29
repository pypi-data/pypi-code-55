import os
import sys
import csv
import re
import argparse
import json
import shutil
import subprocess

from path import Path

import pdftotext
import docx2txt
from striprtf.striprtf import rtf_to_text


# The types that can be handled are : csv, doc, docx, html, md, pdf, rtf, txt, xml


def extract(path):
    """Extract texts from documents in the given folder and its subfolders and store them at the same location in files called '.<TYPE>-----<NAME>.txt'."

    Arguments:
        path {str} -- path to the folder where the files to extract are

    Returns:
        None
    """

    path = Path(path)

    extract_folders(path, first_call=True)


def extract_folders(path, first_call=False):
    """Recursively extracts text

    Arguments:
        path {Path} -- path to the folder where the files to extract are

    Keyword Arguments:
        first_call {bool} -- for monitoring purpose : must be True if the current call is not recursive (default: {False})

    Returns:
        None
    """

    if first_call:
        print("New extraction")
        count_folder = 0

    targets = os.listdir(path)

    for f in targets:

        current_path = path / f

        if os.path.isdir(current_path):

            if first_call:
                print(f"Loading : {int(100 * count_folder / len(targets))} %", end="\r")
                count_folder += 1

            extract_folders(current_path)

        elif not re.match(r"\.\w{2,4}\-{5}.*", f):

            name, file_type = re.findall(r"^(.+)\.(\w{2,4})$", f.lower())[0]

            if not os.path.isfile(path / f".{file_type}-----{name}.txt"):

                if file_type == "pdf":

                    try:

                        extract_pdf2txt(
                            current_path, path / f".pdf-----{name}.txt",
                        )

                    except (pdftotext.Error):
                        txt_file_path = path / f".pdf-----{name}.txt"
                        if os.path.exists(txt_file_path):
                            os.remove(txt_file_path)

                elif file_type == "docx":

                    extract_docx2txt(
                        current_path, path / f".docx-----{name}.txt",
                    )

                elif file_type == "doc":

                    extract_doc2txt(
                        current_path, path / f".doc-----{name}.txt",
                    )

                elif file_type == "rtf":

                    extract_rtf2txt(
                        current_path, path / f".rtf-----{name}.txt",
                    )

                elif file_type in {"csv", "html", "md", "txt", "xml"}:

                    shutil.copyfile(current_path, path / f".{file_type}-----{name}.txt")

    if first_call:
        print("Extraction terminated !")


def extract_pdf2txt(input_path, output_path):
    """Extracts the text from a pdf document and store it in a txt document

    Arguments:
        input_path {Path} -- pdf file to extract text from
        output_path {Path} -- txt file to store text in

    Returns:
        bool -- True if the pdf document could not be processed (probably because it's a scanned document)
    """

    with open(input_path, "rb") as f:
        pdf = pdftotext.PDF(f)
    if all(page == "" for page in pdf):
        return True
    with open(output_path, "w+") as f:
        for page in pdf:
            f.write(page)
            f.write("\n\n$$END OF PAGE$$\n\n")
    return False


def extract_docx2txt(input_path, output_path):
    """Extracts the text from a docx document and store it in a txt document

    Arguments:
        input_path {Path} -- docx file to extract text from
        output_path {Path} -- txt file to store text in

    Returns:
        None
    """

    with open(output_path, "w+") as f:
        f.write(docx2txt.process(input_path))


def extract_doc2txt(input_path, output_path):
    """Extracts the text from a doc document and store it in a txt document. It creates a tempoary docx file from the doc one and removes it after extraction.

    Arguments:
        input_path {Path} -- doc file to extract text from
        output_path {Path} -- txt file to store text in

    Returns:
        None
    """

    subprocess.call(
        [
            "sudo",
            "lowriter",
            "--headless",
            "--convert-to",
            "docx",
            "--outdir",
            f"{input_path.rsplit('/', 1)[0]}",
            f"{input_path}",
        ]
    )
    extract_docx2txt(f"{input_path}x", output_path)
    os.remove(f"{input_path}x")


def extract_rtf2txt(input_path, output_path):
    """Extracts the text from a rtf document and store it in a txt document

    Arguments:
        input_path {Path} -- rtf file to extract text from
        output_path {Path} -- txt file to store text in

    Returns:
        None
    """

    with open(output_path, "w+",) as f:
        f.write(rtf_to_text(open(input_path).read()))


def reset_cache(path):
    """Clear all cached files in a folder. The files to erase are called '.<TYPE>-----<NAME>.txt'.

    Arguments:
        path {Path} -- folder to clear the cached files in

    Returns:
        None
    """

    path = Path(path)

    for f in os.listdir(path):

        current_path = path / f

        if os.path.isdir(current_path):

            reset_cache(current_path)

        elif re.match(r"\.\w{2,4}\-{5}.*", f):

            os.remove(current_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "path", metavar="P", type=str, help="the path to the folder to preprocess"
    )
    parser.add_argument(
        "--reset", dest="reset", action="store_true", help="to clean the cached files"
    )

    args = parser.parse_args()

    reset_cache(args.path) if args.reset else extract(args.path)
