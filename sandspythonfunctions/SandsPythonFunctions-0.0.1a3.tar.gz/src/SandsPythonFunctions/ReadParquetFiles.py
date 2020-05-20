def read_parquet_current_folder(pattern, print_filenames):
    """This function takes a pattern (which can include wildcharacters *) and then globs
    in the folder of the script being executed for parquet files that match the pattern

    Arguments:
        pattern {string} -- this is the string that the user wants to load into a
            combined pandas dataframe
        print_filenames {string} -- this must be "yes" or "no" or "" if yes then the
            filenames of all of the matched files will be printed

    Returns:
        pandas.dataframe -- this returns the combined dataframe of all of hte matched
        parquet files
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
        for file in files:
            if dta is None:
                dta = pq.read_table(file)
                dta = dta.to_pandas()
            else:
                dta1 = pq.read_table(file)
                dta1 = dta1.to_pandas()
                pd.concat([dta, dta1])
        return dta

    path = pathlib.Path(".")
    dta = None
    if pattern == "":
        files = list(path.glob("*.parquet"))
        dta = read_in_parquet_files(files, dta)
    elif ".parquet" not in pattern:
        files = list(path.glob(f"{pattern}*.parquet"))
        dta = read_in_parquet_files(files, dta)
    else:
        files = list(path.glob(pattern))
        dta = read_in_parquet_files(files, dta)
    if not dta:
        print(
            f"function read_parquet_current_folder did not find any parquet files matching the pattern given in the current folder"
        )
    else:
        pprint([file.name for file in files])
        return dta
