# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['samplics',
 'samplics.estimation',
 'samplics.sae',
 'samplics.sampling',
 'samplics.utils',
 'samplics.weighting']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1.3,<4.0.0',
 'numpy>=1.15,<2.0',
 'pandas>=0.25,<0.26',
 'scipy>=1.4,<2.0',
 'statsmodels>=0.10,<0.11']

setup_kwargs = {
    'name': 'samplics',
    'version': '0.0.11',
    'description': 'Select, weight and analyze complex sample data',
    'long_description': '==========\n*SAMPLICS*\n==========\n\n*samplics* is a python package for selecting, weighting\nand analyzing sample obtained from complex sampling design.\n\nSample Analytics\n----------------\nIn large scale surveys, often complex random mechanisms are used to select\nsamples. Estimations obtained from such samples must reflect the random\nmechanism to ensure accurate calculations. *samplics* implements a set of\nsampling techniques for complex survey designs.\n\nSelection\n================\nSince the full population cannot be observed, a sample is selected\nto estimate population parameters of interest. The assumption is\nthat the sample is **representative** of the population for the characteristics\nof interest. The selection methods in samplics are:\n\n* Simple random sampling (SRS)\n* Systematic selection (SYS)\n* Probability proportional to size (PPS)\n    * Systematic\n    * Brewer\'s method\n    * Hanurav-Vijayan method\n    * Murphy\'s method\n    * Sampford\'s method\n* Unequal sample selection\n\nWeighting\n=========\nSample weighting is the main mechanism used in surveys to formalize the\nrepresentivity of the sample. The base or design weights are usually\nadjusted to compensate for distorsions due nonresponse and other shorcomings\nof the operationalization of the sampling design.\n\n* Weight adjustment due to nonresponse\n* Weight poststratification, calibration and normalization\n* Weight replication i.e. Boostrap, BRR, and Jackknife\n\nEstimation\n==========\nThe estimation of the parameters of interest must reflect the sampling\nmechanism and the weight adjustments.\n\n * Taylor linearization procedures\n * Replicate-based estimation i.e. Boostrap, BRR, and Jackknife\n * Regression-based\n\nParameters of interest\n* Linear parameters e.g. total, mean, proportion\n* Non-linear (complex) parameters e.g. ratio, regression coefficient\n\nInstallation\n------------\n``pip install samplics``\n\nif both Python 2.x and python 3.x is installed on your computer,\nyou may have to use: ``pip3 install samplics``\n\nDependencies\n------------\nPython versions 3.6.x or newer and the following packages:\n\n* `numpy <https://numpy.org/>`_\n* `pandas <https://pandas.pydata.org/>`_\n* `scpy <https://www.scipy.org/>`_\n* `statsmodels <https://www.statsmodels.org/stable/index.h.tml>`_\n\nUsage\n------\n\nTo select a sample of primary sampling units using PPS method,\nwe can use a code similar to:\n\n.. code:: python\n\n    import samplics\n    from samplics.sampling import Sample\n\n    psu_frame = pd.read_csv("psu_frame.csv")\n    psu_sample_size = {"East":3, "West": 2, "North": 2, "South": 3}\n    pps_design = Sample(method="pps-sys", stratification=True, with_replacement=False)\n    frame["psu_prob"] = pps_design.inclusion_probs(\n        psu_frame["cluster"],\n        psu_sample_size,\n        psu_frame["region"],\n        psu_frame["number_households_census"]\n        )\n\nTo adjust the design sample weight for nonresponse,\nwe can use a code similar to:\n\n.. code:: python\n\n    import samplics\n    from samplics.weighting import SampleWeight\n\n    status_mapping = {\n        "in": "ineligible", "rr": "respondent", "nr": "non-respondent", "uk":"unknown"\n        }\n\n    full_sample["nr_weight"] = SampleWeight().adjust(\n        samp_weight=full_sample["design_weight"],\n        adjust_class=full_sample["region"],\n        resp_status=full_sample["response_status"],\n        resp_dict=status_mapping\n        )\n\n.. code:: python\n\n    import samplics\n    from samplics.estimation import TaylorEstimation, ReplicateEstimator\n\n    zinc_mean_str = TaylorEstimator("mean").estimate(\n        y=nhanes2f["zinc"],\n        samp_weight=nhanes2f["finalwgt"],\n        stratum=nhanes2f["stratid"],\n        psu=nhanes2f["psuid"],\n        exclude_nan=True\n    )\n\n    ratio_wgt_hgt = ReplicateEstimator("brr", "ratio").estimate(\n        y=nhanes2brr["weight"],\n        samp_weight=nhanes2brr["finalwgt"],\n        x=nhanes2brr["height"],\n        rep_weights=nhanes2brr.loc[:, "brr_1":"brr_32"],\n        exclude_nan = True\n    )\n\n\nContributing\n------------\nTBD\n\nLicense\n-------\n`MIT <https://github.com/survey-methods/samplics/blob/master/license.txt>`_\n\nProject status\n--------------\nThis is an alpha version. At this stage, this project is not recommended to be\nused for production or any project that the user depend on.\n\n\n\n\n',
    'author': 'Mamadou S Diallo',
    'author_email': 'msdiallo@quantifyafrica.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://samplics.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
