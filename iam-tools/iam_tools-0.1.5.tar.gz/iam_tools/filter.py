#!/usr/bin/env python3
"""
Filter the IAM csv file and export the subset.
The filter use regexp for each selector.
"""

import sys
import argparse
import pandas as pd
import scipy.io as sio

selectors = ['model', 'scenario', 'region', 'variable']


def filter(df, **kwargs):
    """
    Filter pandas.DataFrame using keywords arguments selectors.
    The values of selectors are processed as regexp.

    Parameters
    ----------
    df: pandas DataFrame
        Input dataframe to be filtered.
    kwargs:
        Selectors to filter using regexp.
        The selectors as a kwargs keys are:
            - model
            - scenario
            - region
            - variable

    Returns
    -------
    pandas.DataFrame
        The filtered subset of original input DataFrame.

    """
    df.columns = map(str.lower, df.columns)

    for param in kwargs.items():
        # remove null
        df = df[df[param[0]].notnull()]
        df = df[df[param[0]].str.contains(param[1], regex=True)]
        df = df.reset_index(drop=True)
    return df


def export(df, output_file=None):
    """
    Export pandas DataFrame to output file with specified format.
    If the output_file is None teh DataFrame will be output
    to console std out.

    Parameters
    ----------
    df: pandas DataFrame
        Input dataframe to be filtered.
    output_file: str
        Output filename path with specified format which can be
        .csv, .mat or .h5.  If None the console std out will be used.

    Raises
    ------
    NotImplementedError
        If not supported file format is used

    """
    if output_file:
        if output_file.endswith('.csv'):
            df.to_csv(output_file, index=False)
        elif output_file.endswith('.mat'):
            # we prepend all column which starts with digit (all years columns)
            # with 'y' as matlab cell array does not like columns names starting with
            # digit.
            df.columns = ['y{}'.format(col) if col[0].isdigit() else col for col in df.columns]
            d = df.to_dict(orient='list')
            sio.savemat(output_file, d)
        elif output_file.endswith('.h5'):
            df.to_hdf(output_file, key='test', index=False)
        else:
            raise NotImplementedError("The output format: {} is not supported."
                                      .format(output_file.split('.')[-1]))

    else:
        df.to_string(sys.stdout, index=False)
        sys.stdout.write('\n')


def main():
    """
    main function
    """
    example_text = '''examples:
     Command line examples after installing to system:

     Print all unique models:
     >>>filter_IAM iam_input.csv -unique model

     Print to console all rows where variables starts with "Capacity|Electricity|":
     >>>filter_IAM iam_input.csv -variable "^Capacity\|Electricity\|.*"

     Export all rows where variable column start with Secondary Energy|Electricity| to my_output.mat [cell array] file:
     >>>filter_IAM iam_input.csv -variable "^Secondary Energy\|Electricity\|.*" -output my_output.mat

     Export all rows where variable column contains "450-" and "-OPT"  to my_output.csv file:
     >>>filter_IAM iam_input.csv -scenario "450-.*.-OPT" -output my_output.csv

     Print all rows where models are GCAM or REMIND:
     >>>filter_IAM iam_input.csv -model "GCAM|REMIND"

     Print unique regions of rows where model is GCAM:
     >>>filter_IAM iam_input.csv -model "GCAM" -unique region

     Export all rows where variable column start with Emissions|CO2 to my_output.csv file:
     >>>filter_IAM iam_input.csv -variable "^Emissions\|CO2.*" -output my_output.csv
     '''

    parser = argparse.ArgumentParser(description="Filter and export csv file with IAM data. The filter use regexp"
                                                 "for selectors values.",
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="path to input IAM csv file.")
    parser.add_argument("-unique", type=str,
                        help="Show unique values of specified column. The result will be "
                             "printed to standard console output.")
    parser.add_argument("-model", type=str,
                        help="Filter model column using regexp.")
    parser.add_argument("-scenario", type=str,
                        help="Filter scenario column using regexp.")
    parser.add_argument("-region", type=str,
                        help="Filter region column using regexp.")
    parser.add_argument("-variable", type=str,
                        help="Filter variable column using regexp.")
    parser.add_argument("-output", type=str,
                        help="Output file name. The filename should contain file format."
                             "Supported formats are csv, mat and h5. If not specified the result will be"
                             "printed to console output."
                             "If not supported file format is used the script will raise error.")
    if len(sys.argv)==1:
            parser.print_help(sys.stderr)
            sys.exit(1)
    args = parser.parse_args()
    args_dict = vars(args)

    params = {selector: args_dict[selector] for selector in selectors if args_dict[selector]}

    try:
        df = pd.read_csv(args.input, delimiter=',', engine='python')
    # the file might be in latin_1 encoding
    except UnicodeDecodeError:
        df = pd.read_csv(args.input, delimiter=',', encoding='latin_1', engine='python')

    res_df = filter(df, **params)

    # we always print to console if user wants unique values
    if args_dict['unique']:
        out = list(res_df[args_dict['unique']].unique())
        sys.stdout.write(", ".join(str(x) for x in out))
        sys.stdout.write('\n')
        sys.exit(0)

    export(res_df, args_dict['output'])


if __name__ == "__main__":
    main()
