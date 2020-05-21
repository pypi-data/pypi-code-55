import os

import pandas as pd


class Properties:
    def __init__(self, data_frame):
        self.assay = data_frame["Assay"].value_counts(dropna=False)
        self.assemblies = data_frame["Assembly"].value_counts(dropna=False)
        self.cell_types = data_frame["Biosample term name"].value_counts(dropna=False)
        self.experiments = data_frame["Experiment accession"].value_counts(dropna=False)
        self.formats = data_frame["File format"].value_counts(dropna=False)
        self.outputs = data_frame["Output type"].value_counts(dropna=False)
        self.statuses = data_frame["File Status"].value_counts(dropna=False)


def test_data_curation(data):
    org = data["Biosample organism"].unique()
    assert len(org) == 1, "There's more than one organism in the data set!"
    cell = data["Biosample type"].unique()
    assert len(cell) == 1, "There's more than one type of sample (e.g. primary cell) in the data set!"
    return


path = "D:/Utilizador HDD/OneDrive - Nova Medical School Faculdade de Ciências Médicas da " \
       "UNL/1-Research/3-Vencode/Fantom5/Files/Validation_files/ENCODE/"
file = os.path.join(path, "metadata.tsv")

data = pd.read_csv(file, engine="python", sep='\t', header=0)
data_properties = Properties(data)

data_bed = data.loc[data["File format"].str.contains("bed") & ~data['File format'].str.contains("big")]
data_bed_properties = Properties(data_bed)

data_hg19 = data.loc[data["Assembly"] == "hg19"]
data_hg19_properties = Properties(data_hg19)

data_released = data.loc[data["File Status"] == "released"]
data_released_properties = Properties(data_released)

data_temp = data_bed.loc[data_bed["Assembly"] == "hg19"]
data_bed_hg19_released = data_temp.loc[data_temp["File Status"] == "released"]
data_bed_hg19_released_properties = Properties(data_bed_hg19_released)

data_curated = data_bed_hg19_released.copy(deep=True)
data_curated = data_curated.loc[data_curated["Assay"] != "comparative genomic hybridization by array"]
data_curated = data_curated.loc[data_curated["Assay"] == "DNase-seq"]

for experiment in data_curated["Experiment accession"].unique():
    temp = data_curated.loc[data_curated["Experiment accession"] == experiment]
    outputs = temp["Output type"].values
    if "stable peaks" in outputs or "replicated peaks" in outputs:  # clean Histone ChIP-seq data
        temp = temp[temp["Output type"] == "peaks"]
        data_curated.drop(temp.index, inplace=True)
    elif "hotspots" in outputs or "enrichment" in outputs:  # clean DNase-seq data
        temp = temp[temp["Output type"] != "peaks"]
        data_curated.drop(temp.index, inplace=True)
    elif "optimal IDR thresholded peaks" in outputs:  # clean TF ChIP-seq data
        temp = temp[temp["Output type"] != "optimal IDR thresholded peaks"]
        data_curated.drop(temp.index, inplace=True)
    elif "conservative IDR thresholded peaks" in outputs:  # further clean TF ChIP-seq data
        temp = temp[temp["Output type"] != "conservative IDR thresholded peaks"]
        data_curated.drop(temp.index, inplace=True)
    elif "pseudoreplicated IDR thresholded peaks" in outputs:  # clean unreplicated TF ChIP-seq data
        temp = temp[temp["Output type"] != "pseudoreplicated IDR thresholded peaks"]
        data_curated.drop(temp.index, inplace=True)
    elif "transcription start sites" in outputs:  # clean CAGE/RAMPAGE data
        if "bed idr_peak" in temp["File format"].values:
            temp = temp[temp["File format"] != "bed idr_peak"]
            data_curated.drop(temp.index, inplace=True)
    elif "filtered transcribed fragments" in outputs:
        temp = temp[temp["Output type"] != "filtered transcribed fragments"]
        data_curated.drop(temp.index, inplace=True)
    elif "methylation state at CpG" in outputs:
        temp = temp[temp["Output type"] == "methylation state at CpG"]
        data_curated.drop(temp.index, inplace=True)
    else:
        pass

data_curated_properties = Properties(data_curated)
test_data_curation(data_curated)

file_urls = data_curated["File download URL"]
file_name = "Change name to Files.txt"
file_urls.to_csv(file_name, index=False)

metadata_name = "Metadata_curated_hotspots.csv"
data_curated.to_csv(metadata_name, sep="\t", index=False)

