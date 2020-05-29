#!/usr/bin/env python

from expected_levenshtein import fit, sample
import numpy as np
import json


def main():
    # sample distances for lengths up to 6000, alphabet of 20 characters
    average_distances = sample.random_average_levenshtein(
        6000, 1000, np.arange(20))

    # make models
    rows, coeff, mse = fit.model_average_levenshtein(
        average_distances)

    # write file
    with open('./example_models.json', 'w') as fout:
        json.dump([rows.tolist(), coeff.tolist(), mse.tolist()], fout)


if __name__ == '__main__':
    main()
