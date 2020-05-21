#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
dendrogram_primary.py: file used to generate hierarchical clustering and subsequent dendrograms from FANTOM5 data
"""

import os
import sys

file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(file_dir)

from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

from VEnCode import internals
from VEnCode import common_variables as cv

no_ven_prom = ['Bronchial Epithelial Cell', 'CD14+ Monocytes', 'CD4+ T Cells',
               'CD4+CD25+CD45RA+ naive regulatory T cells',
               'CD4+CD25-CD45RA- memory conventional T cells', 'CD8+ T Cells', 'Eosinophils',
               'Esophageal Epithelial Cells',
               'Fibroblast - Cardiac', 'Fibroblast - Dermal', 'Fibroblast - Gingival',
               'Fibroblast - Periodontal Ligament',
               'Fibroblast - skin', 'Melanocyte', 'Neutrophil', 'Skeletal Muscle Cells',
               'Smooth Muscle Cells - Carotid',
               'Smooth Muscle Cells - Prostate', 'Smooth Muscle Cells - Pulmonary Artery']

no_ven_enha = ['Bronchial Epithelial Cell', 'CD4+ T Cells', 'CD4+CD25-CD45RA+ naive conventional T cells',
               'CD4+CD25-CD45RA- memory conventional T cells', 'CD8+ T Cells', 'Cardiac Myocyte', 'Chondrocyte',
               'Dendritic Cells - monocyte immature derived', 'Eosinophils', 'Esophageal Epithelial Cells',
               'Fibroblast - Cardiac', 'Fibroblast - Dermal', 'Fibroblast - Gingival', 'Fibroblast - Lymphatic',
               'Fibroblast - Mammary', 'Fibroblast - Periodontal Ligament', 'Fibroblast - Villous Mesenchymal',
               'Fibroblast - skin', 'Hepatic Sinusoidal Endothelial Cells', 'Keratocytes', 'Melanocyte',
               'Mesenchymal Stem Cells - bone marrow', 'Mesenchymal stem cells - adipose',
               'Mesenchymal stem cells - umbilical', 'Neutrophil', 'Schwann Cells', 'Skeletal Muscle Cells',
               'Smooth Muscle Cells - Aortic', 'Smooth Muscle Cells - Carotid',
               'Smooth Muscle Cells - Pulmonary Artery', 'Smooth muscle cells - airway', 'Trabecular Meshwork Cells',
               'common myeloid progenitor CMP', 'granulocyte macrophage progenitor', 'promyelocytes']

data = internals.DataTpmFantom5(file=cv.enhancer_file_name, sample_types="primary cells", data_type="enhancers",
                                files_path="outside")
data.merge_donors_primary(exclude_target=False)

columns_to_filter = ['Adipocyte - breast', 'Adipocyte - omental', 'Adipocyte - perirenal', 'Adipocyte - subcutaneous',
                     'Alveolar Epithelial Cells', 'Amniotic Epithelial Cells', 'amniotic membrane cells',
                     'Anulus Pulposus Cell', 'Astrocyte - cerebellum', 'Astrocyte - cerebral cortex', 'Basophils',
                     'CD133+ stem cells - adult bone marrow derived', 'CD133+ stem cells - cord blood derived',
                     'CD14+ CD16- Monocytes', 'CD14+ CD16+ Monocytes',
                     'CD14+ monocyte derived endothelial progenitor cells', 'CD19+ B Cells',
                     'CD34 cells differentiated to erythrocyte lineage', 'CD34+ Progenitors',
                     'CD34+ stem cells - adult bone marrow derived', 'CD4+CD25+CD45RA- memory regulatory T cells',
                     'chorionic membrane cells', 'Ciliary Epithelial Cells', 'Dendritic Cells - plasmacytoid',
                     'Endothelial Cells - Artery', 'Endothelial Cells - Lymphatic', 'Endothelial Cells - Microvascular',
                     'Endothelial Cells - Thoracic', 'Endothelial Cells - Umbilical vein', 'Endothelial Cells - Vein',
                     'Fibroblast - Aortic Adventitial', 'Fibroblast - Conjunctival', 'Fibroblast - Pulmonary Artery',
                     'gamma delta positive T cells', 'Gingival epithelial cells', 'Hair Follicle Dermal Papilla Cells',
                     'Hair Follicle Outer Root Sheath Cells', 'Hepatic Stellate Cells (lipocyte)', 'Hepatocyte',
                     'immature langerhans cells', 'Intestinal epithelial cells (polarized)',
                     'Iris Pigment Epithelial Cells', 'Keratinocyte - epidermal', 'Keratinocyte - oral',
                     'Lens Epithelial Cells', 'Macrophage - monocyte derived', 'Mallassez-derived cells',
                     'Mammary Epithelial Cell', 'Mast cell', 'mature adipocyte', 'Meningeal Cells',
                     'mesenchymal precursor cell - adipose', 'mesenchymal precursor cell - bone marrow',
                     'mesenchymal precursor cell - cardiac', 'Mesenchymal Stem Cells - amniotic membrane',
                     'Mesenchymal stem cells - hepatic', 'Mesenchymal Stem Cells - Vertebral',
                     'Mesenchymal Stem Cells - Wharton Jelly', 'Mesothelial Cells', 'migratory langerhans cells',
                     'Multipotent Cord Blood Unrestricted Somatic Stem Cells', 'Myoblast', 'nasal epithelial cells',
                     'Natural Killer Cells', 'Neural stem cells', 'Neurons', 'Nucleus Pulposus Cell',
                     'Olfactory epithelial cells', 'Oligodendrocyte - precursors', 'Osteoblast',
                     'Pancreatic stromal cells', 'Pericytes', 'Perineurial Cells', 'Placental Epithelial Cells',
                     'Preadipocyte - breast', 'Preadipocyte - omental', 'Preadipocyte - perirenal',
                     'Preadipocyte - subcutaneous', 'Preadipocyte - visceral', 'Prostate Epithelial Cells',
                     'Prostate Stromal Cells', 'Renal Cortical Epithelial Cells', 'Renal Epithelial Cells',
                     'Renal Mesangial Cells', 'Renal Proximal Tubular Epithelial Cell',
                     'Retinal Pigment Epithelial Cells', 'salivary acinar cells',
                     'Skeletal muscle cells differentiated into Myotubes', 'Skeletal Muscle Satellite Cells',
                     'Small Airway Epithelial Cells', 'Smooth Muscle Cells - Bladder',
                     'Smooth Muscle Cells - Brachiocephalic', 'Smooth Muscle Cells - Brain Vascular',
                     'Smooth Muscle Cells - Bronchial', 'Smooth Muscle Cells - Colonic',
                     'Smooth Muscle Cells - Esophageal', 'Smooth Muscle Cells - Intestinal',
                     'Smooth Muscle Cells - Umbilical artery', 'Smooth Muscle Cells - Uterine', 'Synoviocyte',
                     'tenocyte', 'Tracheal Epithelial Cells', 'Urothelial cells']

if columns_to_filter is not None:
    data.data = data.data[columns_to_filter]

if data.data_type == "promoters":
    no_ven_list = no_ven_prom
elif data.data_type == "enhancers":
    no_ven_list = no_ven_enha
else:
    raise AttributeError("data_type {} does not exist".format(data.data_type))

values = data.data.T.values
index = data.data.T.index

clustering = hierarchy.linkage(values, 'single')

plt.figure(figsize=(14, 14))
dn = hierarchy.dendrogram(clustering, labels=index, color_threshold=0, above_threshold_color='#333333',
                          leaf_rotation=0, orientation="left")
ax = plt.gca()

no_axes = False
no_border = True

if no_axes:
    ax.axis('off')
else:
    dflt_col = "#808080"
    dict_leaf_colors = dict()
    for i in no_ven_list:
        dict_leaf_colors[i] = "darkorange"
    for c in cv.primary_cell_list:
        if c not in dict_leaf_colors.keys():
            dict_leaf_colors[c] = dflt_col

    ylbls = ax.get_ymajorticklabels()
    for lbl in ylbls:
        lbl.set_color(dict_leaf_colors[lbl.get_text()])

    if no_border:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

path = "D:/Utilizador HDD\OneDrive - Nova Medical School Faculdade de Ciências Médicas da UNL/1-Research/3-Vencode/" \
       "Fantom5/Dendrograms/"
file_name = "dendro_primary_{}_noBorders_filtered.png".format(data.data_type)
output_path = os.path.join(path, file_name)

plt.savefig(output_path, dpi=600, bbox_inches="tight", transparent=True)

retrieve_leaves = True
if retrieve_leaves:
    leaves_list = dn["leaves"]
    leaves_names = [index[x] for x in leaves_list]
    with open("leaves.csv", "w") as f:
        for item in leaves_names:
            f.write("{}\n".format(item))
    print(leaves_names)
