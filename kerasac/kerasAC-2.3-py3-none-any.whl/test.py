from tiledb_generators import *
import pdb 
tdbgen=TiledbGenerator(task_file="tasks.tsv",
                       chroms_to_use=['chr21'],
                       label_source='fc_bigwig',
                       label_flank=3000,
                       label_aggregation=None,
                       sequence_source='idr_peak',
                       sequence_flank=6500,
                       partition_attribute_for_upweight='idr_peak',
                       partition_threshold_for_upweight=1,
                       fraction_to_upweight=0.3)
pdb.set_trace() 
