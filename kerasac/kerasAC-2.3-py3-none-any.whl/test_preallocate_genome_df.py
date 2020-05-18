import pandas as pd
import numpy as np
def preallocate_indices(chrom_sizes_file,chroms):
    '''
    preallocated a genome-wide index pandas df
    '''
    chrom_sizes=pd.read_csv(chrom_sizes_file,header=None,sep='\t')
    chrom_sizes_subset=chrom_sizes[chrom_sizes[0].isin(chroms)]
    genome_size=chrom_sizes_subset[1].sum()
    df=pd.DataFrame({'chrom':['']*genome_size,
                     'index':[0]*genome_size,
                     'upsample':[False]*genome_size})
    print("made empty df") 
    last_index=0
    for index,row in chrom_sizes_subset.iterrows():
        chrom=row[0]
        print(chrom) 
        chrom_size=row[1]
        df['chrom'][last_index:last_index+chrom_size]=chrom
        df['index'][last_index:last_index+chrom_size]=range(chrom_size)
    df['upsample']=0
    return df 

df=preallocate_indices("/mnt/data/annotations/by_release/hg38/hg38.chrom.sizes",["chr2","chr3","chr4","chr5","chr6","chr7","chr9" ,"chr11", "chr12", "chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX","chrY"])

