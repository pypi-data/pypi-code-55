from setuptools import setup,find_packages
import os
from setuptools import setup, find_packages
packages=["SCImputer"]
requires=["pandas","impyute","fancyimpute","sklearn"]


setup(
    name = 'SCImputer',
    version = '0.0.1',
    author = '马纬彧',
    author_email = '740988193@qq.com',
    url = 'https://github.com/histmeisah/SC-sequencing-imputer',
    description = '利用11种插补算法来填补单细胞测序数据缺失值',
    packages=packages,
    install_requires = [],
    zip_safe=False,
    keywords = 'imputation',
    entry_points={
        'console_scripts':[
            'divide=SCImputer:divide',
            'evaluate=SCImputer:evaluate'
            'mean_impute=SCImputer:mean_impute'
            'random_impute=SCImputer:random_impute'
            'mode_impute=SCImputer:mode_impute'
            'median_impute=SCImputer:median_impute'
            'EM_impute=SCImputer:EM_impute'
            'fast_knn_impute=SCImputer:fast_knn_impute'
            'KNN_impute=SCImputer:KNN_impute'
            'IterativeImpute=SCImputer:IterativeImpute'
            'IterativeSVD_Impute=SCImputer:IterativeSVD_Impute'
            'MatrixFactorization_Impute=SCImputer:MatrixFactorization_Impute'
            'NuclearNormMinimization_Impute=SCImputer:NuclearNormMinimization_Impute'
            'load_data=SCImputer:load_data'
        ]
    },
    license='GPL=3.0'
    
    
    
    
)