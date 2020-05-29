import os
import csv
import argparse
from path import Path
from unidecode import unidecode
import json
import sys
import re

from .extract import extract


def search(query, input_path, output_path, scale="row", update_cache=True):
    """Searchs a query in extracted files the given input folder and its subfolders and stores the results at the given output folder.

    Arguments:
        query {str} -- query : words must be separated with spaces, for mandatory words use +, for forbidden words use -, for complex expressions use ""
        input_path {str} -- folder to search in
        output_path {str} -- folder to store the results in

    Keyword Arguments:
        scale {str} -- scale of the research : the possible values are "row" and "doc" (default: {"row"})
        update_cache {bol} -- `True` to update the cached files (default: {False})
    
    Returns:
        None
    """

    if update_cache:
        extract(input_path)

    input_path = Path(input_path)
    output_path = Path(output_path)

    assert scale in {
        "row",
        "doc",
    }, f"Wrong scale value. It must be row or doc, not {scale}."

    query = query.split(" ")

    clean_query = preprocess(query)
    result, count_dict = search_folder(clean_query, input_path, scale, first_call=True)

    output_path = output_path / normalize("__".join(query)).replace("/", "").replace(
        " ", "_"
    )

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    print(f"Found {count_dict['nb']} results.")

    with open(output_path / "folders.json", "w+",) as f:
        json.dump(count_dict, f, indent=4)

    with open(output_path / "results.csv", "w+",) as f:
        writer = csv.writer(f)
        for row in result:
            if scale == "row":
                writer.writerow(row)
            else:
                writer.writerow(row[0])


def search_folder(query, path, scale, first_call=False):
    """Recursively searchs a query in a given folder at a given scale

    Arguments:
        query {list[list[str]]} -- preprocessed query to search
        path {Path} -- folder to search in
        scale {row} -- scale of the research : the possible values are "row" and "doc" (default: {"row"})

    Keyword Arguments:
        first_call {bool} -- for monitoring purpose : must be True if the current call is not recursive (default: {False})

    Returns:
        dict -- the key 'nb' refers to the total number of occurrences recursively found in the given folder, the key 'result' is the list of the results
    """

    path = Path(path)

    if first_call:
        print("New research")
        count_folder = 0

    result = [["path", "row", "context"]]
    count_dict = {}
    count = 0
    targets = os.listdir(path)

    for f in targets:

        current_path = path / f

        if os.path.isdir(current_path):

            if first_call:
                print(f"Loading : {int(100 * count_folder / len(targets))} %", end="\r")
                count_folder += 1

            local_result, local_dict = search_folder(query, current_path, scale)
            result += local_result[1:]
            count += local_dict["nb"]

            if f in count_dict.keys():
                count_dict[f]["nb"] += local_dict["nb"]
                count_dict[f]["path"].update(local_dict["path"])
            else:
                count_dict[f] = local_dict

        else:
            if re.match(r"\.\w{2,4}\-{5}.+", f.lower()):
                local_result = search_file(query, current_path, scale)[1:]
                result += local_result
                count += len(local_result)

    if len(count_dict) > 0:
        return result, {"nb": count, "path": count_dict}
    else:
        return result, {"nb": count}


def search_file(query, path, scale):
    """Searchs a query in a given file at a given scale

    Arguments:
        query {list[list[str]]} -- preprocessed query to search
        path {Path} -- file to search in
        scale {row} -- scale of the research : the possible values are "row" and "doc" (default: {"row"})

    Returns:
        list -- list of occurrences found. For each occurrence, we store the file path, the row number and the context. In 'doc' scale, the row number and the context are None.
    """

    path = Path(path)
    result = [["path", "row", "context"]]
    with open(path, "r") as f:
        if scale == "row":
            for i, row in enumerate(f):
                if search_str(query, row):
                    file_type, file_name = re.findall(
                        r"\.(\w{2,4})\-{5}(.+\.)txt", path
                    )[0]
                    result.append(
                        [
                            path.rsplit("/", 1)[0] + "/" + file_name + file_type,
                            i,
                            row[:-1],
                        ]
                    )
        elif scale == "doc":
            txt = f.read()
            if search_str(query, txt):
                result.append([str(path), None, None])
    return result


def search_str(query, txt):
    """Searchs a query in a given string

    Arguments:
        query {list[list[str]]} -- preprocessed query to search
        txt {str} -- string to search in

    Returns:
        bool -- True if an occurrence has been found
    """

    for token in query[0]:
        if normalize(txt).find(normalize(token)) < 0:
            return False
    for token in query[1]:
        if normalize(txt).find(normalize(token)) >= 0:
            return False
    for token in query[2]:
        if normalize(txt).find(normalize(token)) >= 0:
            return True
    return False


def normalize(txt):
    """Normalizes text

    Arguments:
        txt {str} -- text to normalize

    Returns:
        str -- normalized text
    """

    assert type(txt) == str
    return unidecode(txt.lower())


def preprocess(args_list):
    """Preprocesses a query

    Arguments:
        args_list {list[str]} -- list of words (for mandatory words use +, for forbidden words use -, for complex expressions use)

    Returns:
        list[lst[str]] -- preprocessed query
    """

    OR = []
    AND = []
    NOT = []

    i = 0
    while i < len(args_list):
        arg = args_list[i]

        if arg[0] not in {"+", "-"}:
            arg = "§" + arg

        if arg[1] in {"'", '"'}:
            part = arg

            while not part[-1] in {'"', "'"}:

                if i >= len(args_list) - 1:
                    raise Exception("missing quote mark in the query.")

                i += 1
                part = args_list[i]
                arg += " " + part

            arg = arg[0] + arg[2:-1]

        if arg[0] == "+":
            AND.append(arg[1:])
        elif arg[0] == "-":
            NOT.append(arg[1:])
        else:
            assert arg[0] == "§"
            OR.append(arg[1:])

        i += 1

    return [AND, NOT, OR]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "query",
        metavar="Q",
        type=str,
        nargs="+",
        help='your query with several words seperated by spaces. Use + for mandatory words, - for forbidden words and "" for complex expressions.',
    )
    parser.add_argument(
        "--d",
        dest="doc_scale",
        action="store_true",
        default=False,
        help="to search at the doc scale instead of at the row scale",
    )
    parser.add_argument(
        "--input_path",
        dest="input_path",
        action="store",
        help="path to the folder to search in",
    )
    parser.add_argument(
        "--output_path",
        dest="output_path",
        action="store",
        help="path to the folder to put the results in",
    )

    args = parser.parse_args()

    scale = "doc" if args.doc_scale else "row"

    search(" ".join(args.query), args.input_path, args.output_path, scale=scale)
