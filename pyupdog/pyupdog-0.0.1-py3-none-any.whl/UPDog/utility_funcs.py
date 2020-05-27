#!/usr/bin/env python

from pysam import VariantFile
from pyvariantfilter.variant import Variant
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
sns.set()

def calculate_upd_metrics_per_chromosome(vcf, chromosome_to_analyze, family, block_size, min_dp ,min_gq, min_qual, proband_id):
	
	family_member_ids = family.get_all_family_member_ids()

	bcf_in = VariantFile(vcf)

	variant_count = 0
	matches_paternal_uniparental_ambiguous_count = 0
	matches_maternal_uniparental_ambiguous_count = 0
	matches_paternal_uniparental_isodisomy_count = 0
	matches_maternal_uniparental_isodisomy_count = 0
	alleles_identical_to_dad_count = 0
	alleles_identical_to_mum_count = 0
	is_homozygous_count = 0
	is_biparental_count = 0

	block_dict = {}

	last_block = 0
	block_count = 1

	for rec in bcf_in.fetch(chromosome_to_analyze):

		chrom = rec.chrom
		pos = rec.pos
		ref = rec.ref
		alt = rec.alts
		filter_status = rec.filter.keys()
		info = rec.info
		quality = rec.qual

		if len(alt) != 1:

			continue

		alt = alt[0]

		if alt == '*':
			continue

		if quality < min_qual:

			continue

		new_variant = Variant(chrom=chrom, pos=pos, ref=ref, alt=alt, filter_status=filter_status, quality=quality)
		new_variant.add_family(family)

		for family_member_id in family_member_ids:

			sample_genotype_data = rec.samples[family_member_id]

			ref_and_alt = [ref, alt]

			gts =[]
			ads =[]

			for allele in sample_genotype_data['GT']:

				if allele == None:

					gts.append('.')

				else:

					gts.append(ref_and_alt[allele])

			if gts[0] == '.' and gts[1] == '.':

					ads.append(0)
					ads.append(0)

			elif len(sample_genotype_data['AD']) == 1 and sample_genotype_data['AD'][0] == None:

					ads.append(0)
					ads.append(0)

			else:

				assert len(sample_genotype_data['AD']) == 2

				for ad in sample_genotype_data['AD']:

					if ad == None:

						ads.append(0)

					else:

						ads.append(ad)

			gq = sample_genotype_data['GQ']

			if gq == None:

				gq = 0

			dp = sample_genotype_data['DP']

			if dp == None:

				dp  = 0

			new_variant.add_genotype(family_member_id, gts, ads, gq, dp)


		# now we have created variant object let us count the number for each block

		if new_variant.is_snp() and new_variant.all_samples_pass_genotype_quality(min_dp, min_gq):

			paternal_uniparental_ambiguous = new_variant.matches_paternal_uniparental_ambiguous(min_parental_gq = min_gq, min_parental_depth = min_dp)
			maternal_uniparental_ambiguous = new_variant.matches_maternal_uniparental_ambiguous(min_parental_gq = min_gq, min_parental_depth = min_dp)

			paternal_uniparental_isodisomy = new_variant.matches_paternal_uniparental_isodisomy(min_parental_gq = min_gq, min_parental_depth = min_dp)
			maternal_uniparental_isodisomy = new_variant.matches_maternal_uniparental_isodisomy(min_parental_gq = min_gq, min_parental_depth = min_dp)

			alleles_identical_to_dad =  new_variant.alleles_identical_to_dad(min_parental_gq = min_gq, min_parental_depth = min_dp)
			alleles_identical_to_mum = new_variant.alleles_identical_to_mum(min_parental_gq = min_gq, min_parental_depth = min_dp)

			is_homozygous = new_variant.is_homozygous(proband_id)

			is_biparental = new_variant.is_biparental_inheritance(min_parental_gq = min_gq, min_parental_depth = min_dp)

			variant_count += 1

			if paternal_uniparental_ambiguous:

				matches_paternal_uniparental_ambiguous_count += 1

			if maternal_uniparental_ambiguous:

				matches_maternal_uniparental_ambiguous_count += 1

			if paternal_uniparental_isodisomy:

				matches_paternal_uniparental_isodisomy_count += 1

			if maternal_uniparental_isodisomy:

				matches_maternal_uniparental_isodisomy_count += 1

			if alleles_identical_to_dad:

				alleles_identical_to_dad_count += 1

			if alleles_identical_to_mum:

				alleles_identical_to_mum_count += 1

			if is_homozygous:

				is_homozygous_count += 1

			if is_biparental:

				is_biparental_count += 1

			# have we crossed a new block 
			if new_variant.pos > last_block + block_size:

				block_dict[block_count] = {
					'end': block_count * block_size,
					'variant_count' : variant_count,
					'matches_paternal_uniparental_ambiguous_count' : matches_paternal_uniparental_ambiguous_count,
					'matches_maternal_uniparental_ambiguous_count': matches_maternal_uniparental_ambiguous_count,
					'matches_paternal_uniparental_isodisomy_count': matches_paternal_uniparental_isodisomy_count,
					'matches_maternal_uniparental_isodisomy_count': matches_maternal_uniparental_isodisomy_count,
					'alleles_identical_to_dad_count': alleles_identical_to_dad_count,
					'alleles_identical_to_mum_count': alleles_identical_to_mum_count,
					'is_homozygous_count': is_homozygous_count,
					'is_biparental_count': is_biparental_count

				}



				variant_count = 0
				matches_paternal_uniparental_ambiguous_count = 0
				matches_maternal_uniparental_ambiguous_count = 0
				matches_paternal_uniparental_isodisomy_count = 0
				matches_maternal_uniparental_isodisomy_count = 0
				alleles_identical_to_dad_count = 0
				alleles_identical_to_mum_count = 0
				is_homozygous_count = 0
				is_biparental_count = 0

				last_block = last_block + block_size


				block_count = block_count +1


	return block_dict

def replace_with_na(df, column, min_count):
	
	if df['variant_count'] < min_count:
		
		return np.nan
		
	else:
		
		return df[column]



def create_ax_for_plotting(chromosome, df, block_size, output):

	chrom_prop_df = df[df['chrom'] ==chromosome]

	plot_min = min(chrom_prop_df['end'])
	plot_max = max(chrom_prop_df['end'])

	# we want to scale the X axis labels so that it looks pretty
	chrom_size = plot_max

	if chrom_size > 100000000:
		
		scale_factor = 10
		
	else:
		
		scale_factor = 3

	xticks_chrom = np.arange(plot_min, plot_max, block_size*scale_factor)
	xticks_labels = np.arange(plot_min, plot_max, block_size*scale_factor)
	x_ticks_labels = [int(x/1000000) for x in xticks_chrom]

	# plot and format axis
	ax = chrom_prop_df.plot(x='end', figsize=(20,5))
	ax.set_xticks(xticks_chrom)
	ax.set_xlim([plot_min-1000000, plot_max+1000000])
	ax.set_ylim([-0.02, 1.05])
	ax.set_xticklabels(x_ticks_labels)
	ax.set_xlabel(f'Chromosome {chromosome} Position (Mb)')
	ax.set_ylabel('Proportion of Variants')
	ax.legend(loc='upper right')

	plt.savefig(output, format='png')

	plt.close("all")

def is_significant(df, expected, key):
	
	if df[key] == None:
		
		return None
	
	mendel_errors = df[key]
	
	variant_count = df['variant_count']
	
	
	return scipy.stats.binom_test(mendel_errors, variant_count, expected, alternative='greater')


def merge_contiguous_blocks(df, block_size, analysis, analysis2):

	if df.shape[0] == 0:

		return []

	contiguous_blocks = []

	last_chr = 'NA'
	last_start = None
	last_end = None

	current_block_start = None
	current_block_chr = None

	current_p_values = []
	current_proportions = []

	for row in df.itertuples():
		
		current_chr = row.chrom
		current_end = row.end
		current_start = current_end - block_size

		if current_chr != last_chr:
			
			if last_chr != 'NA':
				
				contiguous_blocks.append([last_chr, current_block_start, last_end, np.mean(current_p_values), np.mean(current_proportions)])
				
				current_p_values = []
				
			current_block_start = current_start
			last_chr = current_chr
			
		elif current_start != (last_start+block_size):
			
			contiguous_blocks.append([current_chr, current_block_start, last_end, np.mean(current_p_values), np.mean(current_proportions)])
			current_block_start = current_start
			current_p_values  =[]
			
		
		last_chr = current_chr
		last_start = current_start
		last_end = current_end
		current_p_values.append(row.__getattribute__(analysis))
		current_proportions.append(row.__getattribute__(analysis2))
			
	contiguous_blocks.append([last_chr, current_block_start, last_end, np.mean(current_p_values), np.mean(current_proportions)])

	return contiguous_blocks

def apply_filters(df, min_blocks, min_proportion, block_size):

	filters = []

	proportion = df['mean_proportion_me']
	start = df['start']
	end = df['end']

	if proportion < min_proportion:

		filters.append('low_proportion_me')

	block_length = end - start

	n_blocks = block_length / block_size

	if n_blocks < min_blocks:

		filters.append('min_block_length')

	if len(filters) == 0:

		return 'pass'

	else:

		return ';'.join(filters)
