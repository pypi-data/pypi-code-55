import os
import unittest
import numpy as np
import pandas as pd
from caeli.drought_indices import spi, spi_monthly, spei, spei_monthly
from caeli.time_series import monthly_series


class CaeliTestCase(unittest.TestCase):

    @staticmethod
    def read_csv(f):
        df = pd.read_csv(f, sep=';', index_col=0, parse_dates=[0])
        df.index.name = 'Date'
        return df

    def test_spi01(self):
        df0 = self.read_csv('cordex_1971_2000/pr/pr.csv')
        for acc in [3, 6, 12]:
            s = 'cordex_1971_2000/spi_{:02d}M/spi_2000_accum_{:02d}M_starting_month_'.format(acc, acc)
            sr0 = monthly_series(df0['pr'], aggregation=acc)
            for m_beg in range(1, 13):
                m_end = (m_beg + acc - 2) % 12 + 1
                pr = sr0[sr0.index.month == m_end]
                spi0 = spi(pr)
                spi1 = self.read_csv(os.path.join('{}{:02d}.csv'.format(s, m_beg)))['spi'].values
                self.assertTrue(np.allclose(spi0, spi1))

    def test_spi02(self):
        df = self.read_csv('cordex_1971_2000/pr/pr.csv')
        for acc in [3, 6, 12]:
            spi_ = spi_monthly(df, aggregation=acc)
            s = 'cordex_1971_2000/spi_{:02d}M/spi_2000_accum_{:02d}M_starting_month_'.format(acc, acc)
            for m_beg in range(1, 13):
                m_end = (m_beg + acc - 2) % 12 + 1
                spi0 = spi_['SPI{:02d}-{:02d}'.format(m_beg, m_end)]
                idx0, idx1 = spi0.first_valid_index(), spi0.last_valid_index()
                spi0 = spi0.loc[idx0:idx1]
                spi1 = self.read_csv(os.path.join('{}{:02d}.csv'.format(s, m_beg)))['spi'].values
                self.assertTrue(np.allclose(spi0, spi1))

    def test_spei01(self):
        df_pr = self.read_csv('cordex_1971_2000/pr/pr.csv')['pr']
        df_pet = self.read_csv('cordex_1971_2000/pet/pet.csv')['PET_Haude']
        df_bal = df_pr - df_pet
        for acc in [3, 6, 12]:
            s = 'cordex_1971_2000/spei_{:02d}M/spei_bal_accum_{:02d}M_starting_month_'.format(acc, acc)
            sr0 = monthly_series(df_bal, aggregation=acc)
            for m_beg in range(1, 13):
                m_end = (m_beg + acc - 2) % 12 + 1
                spi0 = spei(sr0[sr0.index.month == m_end])
                spi1 = self.read_csv(os.path.join('{}{:02d}.csv'.format(s, m_beg)))['spei'].values
                self.assertTrue(np.allclose(spi0, spi1))

    def test_spei02(self):
        df_pr = self.read_csv('cordex_1971_2000/pr/pr.csv')['pr']
        df_pet = self.read_csv('cordex_1971_2000/pet/pet.csv')['PET_Haude']
        df_bal = df_pr - df_pet
        for acc in [3, 6, 12]:
            spei_ = spei_monthly(df_bal, aggregation=acc)
            s = 'cordex_1971_2000/spei_{:02d}M/spei_bal_accum_{:02d}M_starting_month_'.format(acc, acc)
            for m_beg in range(1, 13):
                m_end = (m_beg + acc - 2) % 12 + 1
                spi0 = spei_['SPEI{:02d}-{:02d}'.format(m_beg, m_end)]
                idx0, idx1 = spi0.first_valid_index(), spi0.last_valid_index()
                spi0 = spi0.loc[idx0:idx1]
                spi1 = self.read_csv(os.path.join('{}{:02d}.csv'.format(s, m_beg)))['spei'].values
                self.assertTrue(np.allclose(spi0, spi1))


if __name__ == '__main__':
    unittest.main()
