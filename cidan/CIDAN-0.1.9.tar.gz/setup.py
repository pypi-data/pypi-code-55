from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='CIDAN',
    version='0.1.9',
    description='CIDAN-Calcium Imaging Data ANalysis',
    license="MIT",
    long_description=long_description,
    author='Sam Schickler',
    author_email='sschickl@ucsd.edu',
    # url="http://www.foopackage.com/",
    packages=find_packages(),
    install_requires=["QtPy", "QDarkStyle", "pyqtgraph==0.11.0rc0", "Pyside2", "numpy",
                      "dask[complete]", "matplotlib", "scipy", "tiffile",
                      "scikit-image", "hnswlib", "pillow",
                      'tifffile'],  # TODO add external packages as dependencies
    scripts=[
        "CIDAN/LSSC/process_data.py",
        "CIDAN/LSSC/SpatialBox.py",
        'CIDAN/LSSC/functions/data_manipulation.py',
        "CIDAN/LSSC/functions/eigen.py",
        "CIDAN/LSSC/functions/embeddings.py",
        "CIDAN/LSSC/functions/pickle_funcs.py",
        "CIDAN/LSSC/functions/roi_extraction.py",
        "CIDAN/LSSC/functions/save_test_images.py",
        "CIDAN/LSSC/functions/temporal_correlation.py",
        "CIDAN/GUI/Console/__init__.py",
        "CIDAN/GUI/Console/ConsoleWidget.py",
        "CIDAN/GUI/Data_Interaction/__init__.py",
        "CIDAN/GUI/Data_Interaction/DataHandler.py",
        "CIDAN/GUI/Data_Interaction/PreprocessThread.py",
        "CIDAN/GUI/Data_Interaction/ROIExtractionThread.py",
        "CIDAN/GUI/Data_Interaction/Signals.py",
        "CIDAN/GUI/Data_Interaction/Thread.py",
        "CIDAN/GUI/Data_Interaction/loadDataset.py",
        "CIDAN/GUI/ImageView/__init__.py",
        "CIDAN/GUI/ImageView/ImageViewModule.py",
        "CIDAN/GUI/Inputs/__init__.py",
        "CIDAN/GUI/Inputs/Input.py",
        "CIDAN/GUI/Inputs/BoolInput.py",
        "CIDAN/GUI/Inputs/FileInput.py",
        "CIDAN/GUI/Inputs/FloatInput.py",
        "CIDAN/GUI/Inputs/Int3DInput.py",
        "CIDAN/GUI/Inputs/IntInput.py",
        "CIDAN/GUI/Inputs/OptionInput.py",
        "CIDAN/GUI/ListWidgets/__init__.py",
        "CIDAN/GUI/ListWidgets/ROIItemModule.py",
        "CIDAN/GUI/ListWidgets/ROIItemWidget.py",
        "CIDAN/GUI/ListWidgets/ROIListModule.py",
        "CIDAN/GUI/ListWidgets/TrialListWidget.py",
        "CIDAN/GUI/SettingWidget/__init__.py",
        "CIDAN/GUI/SettingWidget/SettingBlockModule.py",
        "CIDAN/GUI/SettingWidget/SettingsModule.py",
        'CIDAN/GUI/Tabs/__init__.py',
        "CIDAN/GUI/Tabs/FileOpenTab.py",
        "CIDAN/GUI/Tabs/PreprocessingTab.py",
        "CIDAN/GUI/Tabs/ROIExtractionTab.py",
        "CIDAN/GUI/Tabs/Tab.py",
        "CIDAN/__init__.py",
        "CIDAN/__main__.py"
        ]
)
