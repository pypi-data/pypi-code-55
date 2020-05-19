#!/usr/bin/env python

def parse_arguments():
    import argparse
    # Description
    parser = argparse.ArgumentParser(description='Tools to Wrangle data to and from BibExcel')
    # input
    parser.add_argument('-i', '--input', help='input filename')
    # input_matrix
    parser.add_argument('-m', '--input_matrix', default='adjacency_matrix.csv', help='input adjacency matrix')
    # encoding
    # parser.add_argument('-e', '--encoding', default='utf8', help="desired enco=ding (default 'utf8')")
    # type
    parser.add_argument('-t', '--type', help="either 'scopus' or 'wos'")
    # functionality
    parser.add_argument('-f', '--function', help="either 'bibexceltojson', 'jsontobibexcel', 'jsontoexcel', 'filtercoupling'")
    # output
    parser.add_argument('-o', '--output', help='output filename')
    # defaults
    arguments = vars(parser.parse_args())
    return(arguments)


def main(input=None, input_matrix=None, type=None, function=None, output=None):
    import bibexcel
    if function == 'bibexceltojson':
        bibexcel.bibexceltojson(input_name=input, type=type, encoding='utf8', output_name=output)
    if function == 'jsontobibexcel':
        bibexcel.jsontobibexcel(input_name=input, type=type, encoding='utf8', output_name=output)
    if function == 'jsontoexcel':
        bibexcel.jsontoexcel(input_json=input, encoding='utf8')
    if function == 'filtercoupling':
        bibexcel.filtercoupling(input_matrix=input_matrix, input_json=input, type=type, encoding='utf8', output_name=output)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(**arguments)
