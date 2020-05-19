from pathlib import Path
import csv


__all__ = ["text_writer", "str_file_read", "file_locate"]


def str_file_read(file_path, encoding="utf-8"):
    """
    Returns a file's contents as a string.

    Parameters
    ----------
    file_path : str
        Path to GCA file to read
    encoding : str
        Encoding method to use. (Default: "utf-8)

    Returns
    -------
    contents : str
        The gca file's contents as a string
    """

    file_path = Path(file_path)

    # read egf file
    file_contents = file_path.read_text(encoding=encoding)

    return file_contents


def file_locate(folder_path, file_extension=None, return_paths=True):
    """
    Locates '.egf' files within a specified folder and returns their absolute paths in a list.

    Parameters
    ----------
    folder_path : str
        The path to a folder containing one or more '.egf' files
    file_extension : str
        file extension (example: ".txt")
    return_paths : bool
        False will return file names instead of paths

    Returns
    -------
    egf_file_paths : list of str
        A list of absolute paths to '.egf' files in folder or their files names.

    Notes
    -----
    Function will return None of no '.egf' files are found
    """

    folder_path = Path(folder_path)

    # Locate files of specified extension in folder
    if file_extension is None:
        file_paths = [item for item in folder_path.iterdir() if item.is_file()]
    else:
        file_paths = [item for item in folder_path.iterdir() if item.is_file() and item.suffix == file_extension]

    # names of files
    file_names = [file.name for file in file_paths]

    # Create appropriate result for provided 'return_paths` value
    if return_paths is True:
        result = [str(path) for path in file_paths]
    elif return_paths is False:
        result = file_names
    else:
        result = None

    # Return None if the list of files is empty
    if len(file_paths) == 0:
        raise Exception(f"No Files of '{file_extension}' type were found in '{folder_path}'")

    return result


def text_writer(file_path, content_str):

    with open(file_path, "w") as f:
        f.write(content_str)


def read_csv(file_path, delimiter=",", encoding="utf-8"):
    """
    Reads a CSV file

    Parameters
    ----------
    file_path : str
    delimiter : str
    encoding : str

    Returns
    -------
    collection

    """

    with open(file_path, encoding=encoding) as file:
        data_in = list(csv.reader(file, delimiter=delimiter))

    return data_in


def write_csv(file_path, csv_data, delimiter=","):
    """
    Writes CSV file from 2D list

    Parameters
    ----------
    file_path : str
    csv_data : collection
    delimiter : str

    Returns
    -------
    None

    """

    with open(file_path, "w") as csv_out:
        write = csv.writer(csv_out, delimiter=delimiter, lineterminator='\n')
        for i in csv_data:
            write.writerow(i)