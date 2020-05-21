def read_parquet_current_folder(pattern=False, print_filenames=False, subfolder=False):
    """This function takes in arguments and reads and then joins together all parquet
    files that matches the pattern given

    Keyword Arguments:
        pattern {string} -- this will take the string given and use it as the pattern
            for the globbing of the parquetfiles (default: {False})
        print_filenames {bool} -- enter True if you want to see printed out all of the
            files that were used to create the dataframe (default: {False})
        subfolder {list of strings} -- if the parquet files you want to glob are in a 
            subfolder just enter that into the string (default: {False})

    Returns:
        dataframe -- this is the concatinated dataframe from the files globbed
    """
    import pathlib
    import pandas as pd
    import pyarrow.parquet as pq
    import pyarrow as pa
    from pprint import pprint

    def read_in_parquet_files(files, dta):
        """this function reads each file from the glob and merges them together into one
        pandas dataframe

        Arguments:
            files {list} -- this is list of pathlib path objects for parquet files
            dta {None} -- this is a NoneType for testing for previous dataframe reading

        Returns:
            dataframe -- this is the merged pandas dataframe
        """
        if len(files) == 0:
            print(
                f"function read_parquet_current_folder did not find any parquet files matching the pattern given in the current folder"
            )
        else:
            for file in files:
                if dta is None:
                    dta = pq.read_table(file)
                    dta = dta.to_pandas()
                else:
                    dta1 = pq.read_table(file)
                    dta1 = dta1.to_pandas()
                    pd.concat([dta, dta1])
            return dta

    path = pathlib.Path("__file__").parent
    if subfolder:
        for subdir in subfolder:
            path = path / subdir
    dta = None
    if pattern is False:
        files = list(path.glob("*.parquet"))
        dta = read_in_parquet_files(files, dta)
    elif ".parquet" not in pattern:
        files = list(path.glob(f"{pattern}*.parquet"))
        dta = read_in_parquet_files(files, dta)
    else:
        files = list(path.glob(pattern))
        dta = read_in_parquet_files(files, dta)
    if print_filenames is True:
        pprint([file.name for file in files])
    return dta


def concat_dataframes(dataframes):
    """this simple function concatinates all of the dataframes that are entered

    Arguments:
        dataframes {list of dataframes} -- a list of pandas dataframes

    Returns:
        pandas dataframes -- this is a combined dataframe
    """
    import pandas as pd

    return pd.concat(dataframes)


def display_full_dataframe(dta):
    """
    displays a dataframe without cutting anything off for being too long
    Arguments:
        dta {dataframe} -- a dataframe you wish to display
    """
    import pandas as pd

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(dta)
