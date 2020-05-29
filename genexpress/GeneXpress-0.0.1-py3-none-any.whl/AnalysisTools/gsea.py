import os
import gseapy

databases = ('huMAP',
             'Tissue_Protein_Expression_from_Human_Proteome_Map',
             'Tissue_Protein_Expression_from_ProteomicsDB',
             'Transcription_Factor_PPIs',
             'Rare_Diseases_AutoRIF_Gene_Lists',
             'Rare_Diseases_GeneRIF_Gene_Lists',
             'PheWeb_2019',
             'MSigDB_Computational',
             'MGI_Mammalian_Phenotype_Level_4_2019',
             'Ligand_Perturbations_from_GEO_down',
             'Ligand_Perturbations_from_GEO_up',
             'Human_Phenotype_Ontology',
             'GO_Molecular_Function_2018',
             'GO_Cellular_Component_2018',
             'GO_Biological_Process_2018',
             'DSigDB',
             'WikiPathways_2019_Human',
             'WikiPathways_2019_Mouse',
             'KEGG_2019_Human',
             'KEGG_2019_Mouse',
             'GO_Molecular_Function_2018',
             'GO_Cellular_Component_2018',
             'GO_Biological_Process_2018',
             )

hallmarks_db = os.path.join('gsea_databases', 'msigdb_hallmarks.gmt')
gsea_methods = ('signal_to_noise', 't_test', 'ratio_of_classes',
                'diff_of_classes', 'log2_ratio_of_classes')
ssgsea_methods = ('rank', 'log', 'log_rank')


class GSEAnalysis:
    def __init__(self, base_out_directory, extension='/gsea'):
        self.base_out = base_out_directory
        self.gsea_save = self.base_out + extension

        if not os.path.isdir(self.gsea_save):
            os.makedirs(self.gsea_save)

    def run_gsea(self, ordered_df, classes, db=None, db_name=None,
                 processes=4, no_plot=True, method='signal_to_noise',
                 permutation_type='gene_set'):
        if db is None:
            db = hallmarks_db
        if db_name is None:
            db_name = db.split("/")[-1]
        gsea_analysis = gseapy.gsea(ordered_df,
                                    gene_sets=db,
                                    cls=classes,
                                    outdir=os.path.join(self.gsea_save, db_name),
                                    method=method,
                                    no_plot=no_plot,
                                    processes=processes,
                                    permutation_type=permutation_type)
        return gsea_analysis

    def run_ssGSEA(self, ordered_df, db,
                   method='rank', no_plot=True,
                   processes=4):
        ssgsea_analysis = gseapy.ssgsea(ordered_df,
                                        gene_sets=db,
                                        outdir='ss_'+self.gsea_save,
                                        sample_norm_method=method,
                                        no_plot=no_plot,
                                        processes=processes)
        return ssgsea_analysis

    @classmethod
    def construct_classes(cls, disease_name, healthy_name,
                           disease_num, healthy_num):
        return [*[disease_name]*disease_num, *[healthy_name]*healthy_num]

