#!python

import argparse
import csv
import pandas as pd
from pyvariantfilter.family import Family
from pyvariantfilter.family_member import FamilyMember
from pyvariantfilter.variant_set import VariantSet
from UPDog.utility_funcs import calculate_upd_metrics_per_chromosome, create_ax_for_plotting, replace_with_na,is_significant, merge_contiguous_blocks, apply_filters


parser = argparse.ArgumentParser(description='Find UPD events in NGS Trio Data')
parser.add_argument('--vcf', type=str, nargs=1, required=True,
				help='The path to the VCF file. Must be bgzipped and tabixed.')
parser.add_argument('--proband_id', type=str, nargs=1, required=True,
				help='The Sample ID of the proband in the VCF.')
parser.add_argument('--ped', type=str, nargs=1, required=True,
				help='A ped file describing the family relationships.')
parser.add_argument('--output', type=str, nargs=1, required=True, help='The output name prefix.')
parser.add_argument('--min_dp', type=int, nargs=1, required=True, help='The minimum genotype depth.')
parser.add_argument('--block_size', type=int, nargs=1, required=True, help='The block size for calculating areas of chromsome affected by UPD.')
parser.add_argument('--min_gq', type=int, nargs=1, required=True, help='The minimum genotype quality (GQ).')
parser.add_argument('--min_qual', type=int, nargs=1, required=True, help='The minimum QUAL value.')
parser.add_argument('--min_variants_per_block', type=int, nargs=1, required=True, help='The minimum number of variants in a block.')
parser.add_argument('--p_value', type=float, nargs=1, required=True, help='The maximum P value for statistical test for block significance.')
parser.add_argument('--chromosome', type=str, nargs=1, required=False, help='Restrict to single chromosome. WARNING: For testing purposes only.')
parser.add_argument('--min_blocks', type=int, nargs=1, required=True, help='The minimum number of contiguous blocks for a call not to be filtered.')
parser.add_argument('--min_proportion', type=float, nargs=1, required=True, help='If the proportion of UPD variants in a contiguous block is below this then apply a filter.')

args = parser.parse_args()

vcf = args.vcf[0]
proband_id = args.proband_id[0]
ped = args.ped[0]
output = args.output[0]
min_dp = args.min_dp[0]
min_gq = args.min_gq[0]
min_qual = args.min_qual[0]
p_value = args.p_value[0]
block_size = args.block_size[0]
min_variants_per_block = args.min_variants_per_block[0]
min_blocks = args.min_blocks[0]
min_proportion = args.min_proportion[0]


if args.chromosome != None:

	chromosome = args.chromosome[0]
	just_one_chromosome = True

else:

	just_one_chromosome = False


# read ped into df
ped_df = pd.read_csv(ped, sep='\t', names=['family_id', 'sample_id', 'paternal_id', 'maternal_id', 'sex', 'affected'])

# filter by proband
filtered_ped = ped_df[ped_df['sample_id']==proband_id]

# get mum nad dad ids
dad = filtered_ped['paternal_id'].iloc[0]
mum = filtered_ped['maternal_id'].iloc[0]
sex = filtered_ped['sex'].iloc[0]

# get family id
family_id = filtered_ped['family_id'].iloc[0]

# exit if we don't have mum and dad
if dad == '0' or mum == '0':
	print ('Cannot run program on this sample as we no not have the mother and father in the PED file.')
	exit()

# make a family object
my_family = Family(family_id)
my_family.read_from_ped_file(ped, family_id, proband_id)

# check which chromosomes to analyse
if just_one_chromosome == True:

	if sex == 1 and chromosome == 'X':

		print ('Chromosome cannot be X if proband is male.')
		exit()

	else:

		chromosomes_to_analyze = [chromosome]

else:

	if sex == 2:

		print ('Proband is Female - will analyse chromosomes 1-22 and X')
		chromosomes_to_analyze = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'X']

	else:

		print ('Proband is Male - will analyse chromosomes 1-22 only.')
		chromosomes_to_analyze = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']


# now calculate UPD metrics using calculate_upd_metrics_per_chromosome()
master_df = pd.DataFrame()
for chromosome in chromosomes_to_analyze:

	print (f'Calculating UPD Metrics for Chromosome {chromosome}')

	per_chrom_dict = calculate_upd_metrics_per_chromosome(vcf, chromosome, my_family, block_size, min_dp, min_gq, min_qual, proband_id)
	
	df = pd.DataFrame(per_chrom_dict).transpose()
	
	df['chrom'] = chromosome
	
	master_df = master_df.append(df)


# convert columns to proportions e.g. proportion of variants with errors
master_df['prop_alleles_identical_to_dad_count'] = master_df['alleles_identical_to_dad_count']/master_df['variant_count']
master_df['prop_alleles_identical_to_mum_count'] = master_df['alleles_identical_to_mum_count']/master_df['variant_count']
master_df['prop_is_biparental_count'] = master_df['is_biparental_count']/master_df['variant_count']
master_df['prop_is_homozygous_count'] = master_df['is_homozygous_count']/master_df['variant_count']
master_df['prop_matches_maternal_uniparental_ambiguous_count'] = master_df['matches_maternal_uniparental_ambiguous_count']/master_df['variant_count']
master_df['prop_matches_maternal_uniparental_isodisomy_count'] = master_df['matches_maternal_uniparental_isodisomy_count']/master_df['variant_count']
master_df['prop_matches_paternal_uniparental_ambiguous_count'] = master_df['matches_paternal_uniparental_ambiguous_count']/master_df['variant_count']
master_df['prop_matches_paternal_uniparental_isodisomy_count'] = master_df['matches_paternal_uniparental_isodisomy_count']/master_df['variant_count']
master_df['prop_me'] = master_df['prop_matches_maternal_uniparental_ambiguous_count'] + master_df['prop_matches_maternal_uniparental_isodisomy_count'] + master_df['prop_matches_paternal_uniparental_ambiguous_count'] + master_df['prop_matches_paternal_uniparental_isodisomy_count']

master_df['prop_alleles_identical_to_dad_count'] = master_df.apply(replace_with_na, axis=1, args=('prop_alleles_identical_to_dad_count', min_variants_per_block,))
master_df['prop_alleles_identical_to_mum_count'] = master_df.apply(replace_with_na, axis=1, args=('prop_alleles_identical_to_mum_count', min_variants_per_block,))
master_df['prop_is_biparental_count'] = master_df.apply(replace_with_na, axis=1, args=('prop_is_biparental_count', min_variants_per_block,))
master_df['prop_is_homozygous_count'] = master_df.apply(replace_with_na, axis=1, args=('prop_is_homozygous_count', min_variants_per_block,))
master_df['prop_matches_maternal_uniparental_ambiguous_count'] = master_df.apply(replace_with_na, axis=1, args=('prop_matches_maternal_uniparental_ambiguous_count', min_variants_per_block,))
master_df['prop_matches_maternal_uniparental_isodisomy_count'] = master_df.apply(replace_with_na, axis=1, args=('prop_matches_maternal_uniparental_isodisomy_count', min_variants_per_block,))
master_df['prop_matches_paternal_uniparental_ambiguous_count'] = master_df.apply(replace_with_na, axis=1, args=('prop_matches_paternal_uniparental_ambiguous_count', min_variants_per_block,))
master_df['prop_matches_paternal_uniparental_isodisomy_count'] = master_df.apply(replace_with_na, axis=1, args=('prop_matches_paternal_uniparental_isodisomy_count', min_variants_per_block,))
master_df['prop_me'] = master_df.apply(replace_with_na, axis=1, args=('prop_me', min_variants_per_block,))


# plot data and save to file
prop_df = master_df[[
		   'prop_is_homozygous_count',
		   'prop_matches_maternal_uniparental_ambiguous_count',
		   'prop_matches_maternal_uniparental_isodisomy_count',
		   'prop_matches_paternal_uniparental_ambiguous_count',
		   'prop_matches_paternal_uniparental_isodisomy_count',
		   'end',
		  'chrom']]

for chromosome in chromosomes_to_analyze:

	print (f'Plotting Metrics for chromosome: {chromosome}')

	plot_location = f'{output}_chr{chromosome}_UPD.png'

	create_ax_for_plotting(chromosome, prop_df, block_size, plot_location)


# get mean so we know what expected ratio is i.e. that caused by errors - hmm what if every chromosome is UPD?
mean_matches_maternal_uniparental_isodisomy_count = master_df['matches_maternal_uniparental_isodisomy_count'].sum() / master_df['variant_count'].sum()
mean_matches_maternal_uniparental_ambiguous_count = master_df['matches_maternal_uniparental_ambiguous_count'].sum() / master_df['variant_count'].sum()

mean_matches_paternal_uniparental_ambiguous_count = master_df['matches_paternal_uniparental_ambiguous_count'].sum() / master_df['variant_count'].sum()
mean_matches_paternal_uniparental_isodisomy_count = master_df['matches_paternal_uniparental_isodisomy_count'].sum() / master_df['variant_count'].sum()



master_df['sig_prop_matches_maternal_uniparental_ambiguous_count'] = master_df.apply(is_significant, axis=1, args=(mean_matches_maternal_uniparental_ambiguous_count, 'matches_maternal_uniparental_ambiguous_count', ))
master_df['sig_prop_matches_maternal_uniparental_isodisomy_count'] = master_df.apply(is_significant, axis=1, args=(mean_matches_maternal_uniparental_isodisomy_count, 'matches_maternal_uniparental_isodisomy_count', ))
master_df['sig_prop_matches_paternal_uniparental_ambiguous_count'] = master_df.apply(is_significant, axis=1, args=(mean_matches_paternal_uniparental_ambiguous_count, 'matches_paternal_uniparental_ambiguous_count', ))
master_df['sig_prop_matches_paternal_uniparental_isodisomy_count'] = master_df.apply(is_significant, axis=1, args=(mean_matches_paternal_uniparental_isodisomy_count, 'matches_paternal_uniparental_isodisomy_count', ))

# save raw data to file
print ('Saving Raw UPD Metrics file to disk.')
master_df.to_csv(f'{output}_raw_data.csv', sep='\t', index=False)


print ('Calculating statistically significiant UPD events.')
# adjust supplied p value by the number of tests we are going to do - one for each type of mendellian error and block
p_value =  p_value / master_df.shape[0] / 4 

# now restrict to statistically significiant parts of chromosomses and merge contiguous blocks together
mat_amb = master_df[(master_df['sig_prop_matches_maternal_uniparental_ambiguous_count'] < p_value)]
mat_iso = master_df[(master_df['sig_prop_matches_maternal_uniparental_isodisomy_count'] < p_value)]
pat_amb = master_df[(master_df['sig_prop_matches_paternal_uniparental_ambiguous_count'] < p_value)]
pat_iso = master_df[(master_df['sig_prop_matches_paternal_uniparental_isodisomy_count'] < p_value)]


mat_amb_blocks = merge_contiguous_blocks(mat_amb, block_size, 'sig_prop_matches_maternal_uniparental_ambiguous_count','prop_matches_maternal_uniparental_ambiguous_count')
mat_iso_blocks = merge_contiguous_blocks(mat_iso, block_size, 'sig_prop_matches_maternal_uniparental_isodisomy_count','prop_matches_maternal_uniparental_isodisomy_count')
pat_amb_blocks = merge_contiguous_blocks(pat_amb, block_size, 'sig_prop_matches_paternal_uniparental_ambiguous_count','prop_matches_paternal_uniparental_ambiguous_count')
pat_iso_blocks = merge_contiguous_blocks(pat_iso, block_size, 'sig_prop_matches_paternal_uniparental_isodisomy_count','prop_matches_paternal_uniparental_isodisomy_count')

# save calls to file

upd_calls_list = []

	
for row in mat_amb_blocks:

	upd_calls_list.append(row + ['maternal_uniparental_ambiguous'])

for row in mat_iso_blocks:

	upd_calls_list.append(row + ['maternal_uniparental_isodisomy'])

for row in pat_amb_blocks:

	upd_calls_list.append(row + ['paternal_uniparental_ambiguous'])

for row in pat_iso_blocks:

	upd_calls_list.append(row + ['paternal_uniparental_isodisomy'])


# create dataframe from call list
calls_df = pd.DataFrame(upd_calls_list, columns =['chromosome', 'start', 'end', 'mean_p_value', 'mean_proportion_me', 'upd_event_signature'])

# if empty then write empty df
if calls_df.shape[0] == 0:

	calls_df = pd.DataFrame(upd_calls_list, columns =['chromosome', 'start', 'end', 'mean_p_value', 'mean_proportion_me', 'upd_event_signature', 'filter'])
	calls_df.to_csv(f'{output}_UPD_calls.csv', sep='\t', index=False)

else:
	
	# apply a filter  and write df
	calls_df['filter'] = calls_df.apply(apply_filters, axis=1, args=(min_blocks, min_proportion, block_size,))
	calls_df.sort_values('chromosome').to_csv(f'{output}_UPD_calls.csv', sep='\t', index=False)