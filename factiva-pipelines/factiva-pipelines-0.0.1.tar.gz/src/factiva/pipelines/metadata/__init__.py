from factiva.core import dicts


def extract_country_field(region_codes, country_list, country_ix):
    ret_list = []
    rcodes = region_codes.split(',')
    for code in rcodes:
        if code in country_list.index:
            ret_list.append(country_list.loc[code][country_ix])
    return ret_list


def expand_country_codes(articles_df):
    ref_countries = dicts.countries_list()
    articles_df['country_names'] = articles_df['region_codes'].apply(lambda x: extract_country_field(x, ref_countries, 'common_name'))
    articles_df['country_alpha2'] = articles_df['region_codes'].apply(lambda x: extract_country_field(x, ref_countries, 'alpha2'))
    articles_df['country_alpha3'] = articles_df['region_codes'].apply(lambda x: extract_country_field(x, ref_countries, 'alpha3'))
    return articles_df


def extract_industry_field(industry_codes, industry_list, ind_field):
    ret_list = []
    icodes = industry_codes.split(',')
    for code in icodes:
        if code in industry_list.index:
            if ind_field == 'ind_fcode':
                ret_list.append(code)
            else:
                ret_list.append(industry_list.loc[code][ind_field])
    return ret_list


def expand_industry_codes(articles_df):
    ref_industries = dicts.industries_hierarchy()
    ref_industries['ind_fcode'] = ref_industries['ind_fcode'].str.lower()
    ref_industries.set_index('ind_fcode', inplace=True)
    articles_df['industry_names'] = articles_df['industry_codes'].apply(lambda x: extract_industry_field(x, ref_industries, 'name'))
    articles_df['industry_fcodes'] = articles_df['industry_codes'].apply(lambda x: extract_industry_field(x, ref_industries, 'ind_fcode'))
    return articles_df
