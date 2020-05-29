from factiva.pipelines import snapshot_files as sf
from factiva.pipelines import metadata as fm

covid = sf.read_folder('/home/miballe/git/sentiment-exploration/data-covid-raw', only_stats=True)
print(covid.shape)
covid = fm.expand_country_codes(covid)
print(covid.shape)
covid = fm.expand_industry_codes(covid)
print(covid.shape)
print('Done!')
