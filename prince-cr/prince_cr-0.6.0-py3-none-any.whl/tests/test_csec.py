# Test whether cross section are correctly created.

import numpy as np

import prince_cr.config as config
from prince_cr import cross_sections

species_talys = {
'species': [0, 11, 12, 20, 21, 101, 201, 301, 302, 402, 603, 703, 704, 904, 1004, 1005, 1105, 1206, 1306, 1406, 1407] ,
'incl': [(301, 201), (302, 201), (402, 201), (402, 302), (603, 201), (603, 301), (603, 302), (603, 402), (703, 201), (703, 301), (703, 402), (703, 603), (704, 603), (904, 402), (1004, 904), (1005, 402), (1005, 904), (1105, 1005), (1206, 201), (1206, 301), (1206, 302), (1206, 402), (1206, 603), (1206, 703), (1206, 704), (1206, 904), (1206, 1004), (1206, 1005), (1206, 1105), (1206, 1206), (1306, 201), (1306, 301), (1306, 302), (1306, 402), (1306, 603), (1306, 703), (1306, 704), (1306, 904), (1306, 1004), (1306, 1005), (1306, 1105), (1306, 1206), (1306, 1306), (1406, 201), (1406, 301), (1406, 302), (1406, 402), (1406, 603), (1406, 703), (1406, 704), (1406, 904), (1406, 1004), (1406, 1005), (1406, 1105), (1406, 1206), (1406, 1306), (1406, 1406), (1407, 201), (1407, 301), (1407, 302), (1407, 402), (1407, 603), (1407, 703), (1407, 704), (1407, 904), (1407, 1004), (1407, 1005), (1407, 1105), (1407, 1206), (1407, 1306), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407)] ,
'diff': [(201, 12), (201, 20), (201, 101), (301, 12), (301, 20), (301, 101), (302, 12), (302, 20), (302, 101), (402, 12), (402, 20), (402, 101), (603, 12), (603, 20), (603, 101), (703, 12), (703, 20), (703, 101), (704, 101), (904, 12), (904, 20), (904, 101), (1004, 12), (1004, 20), (1004, 101), (1005, 12), (1005, 20), (1005, 101), (1105, 12), (1105, 20), (1105, 101), (1206, 0), (1206, 11), (1206, 12), (1206, 20), (1206, 21), (1206, 101), (1306, 0), (1306, 11), (1306, 12), (1306, 20), (1306, 21), (1306, 101), (1406, 0), (1406, 11), (1406, 12), (1406, 20), (1406, 21), (1406, 101), (1407, 0), (1407, 11), (1407, 12), (1407, 20), (1407, 21), (1407, 101)] ,
}

species_peanut = {
'species': [11, 12, 20, 21, 101, 201, 301, 302, 402, 603, 703, 704, 904, 1004, 1005, 1105, 1206, 1306, 1406, 1407] ,
'incl': [(301, 201), (301, 302), (302, 201), (302, 301), (402, 201), (402, 301), (402, 302), (402, 402), (603, 201), (603, 301), (603, 302), (603, 402), (603, 603), (703, 201), (703, 301), (703, 302), (703, 402), (703, 603), (703, 703), (703, 704), (704, 201), (704, 301), (704, 302), (704, 402), (704, 603), (704, 703), (704, 704), (904, 201), (904, 301), (904, 302), (904, 402), (904, 603), (904, 703), (904, 704), (904, 904), (1004, 201), (1004, 301), (1004, 302), (1004, 402), (1004, 603), (1004, 703), (1004, 704), (1004, 904), (1004, 1004), (1004, 1005), (1005, 201), (1005, 301), (1005, 302), (1005, 402), (1005, 603), (1005, 703), (1005, 704), (1005, 904), (1005, 1004), (1005, 1005), (1105, 201), (1105, 301), (1105, 302), (1105, 402), (1105, 603), (1105, 703), (1105, 704), (1105, 904), (1105, 1004), (1105, 1005), (1105, 1105), (1206, 201), (1206, 301), (1206, 302), (1206, 402), (1206, 603), (1206, 703), (1206, 704), (1206, 904), (1206, 1004), (1206, 1005), (1206, 1105), (1206, 1206), (1306, 201), (1306, 301), (1306, 302), (1306, 402), (1306, 603), (1306, 703), (1306, 704), (1306, 904), (1306, 1004), (1306, 1005), (1306, 1105), (1306, 1206), (1306, 1306), (1406, 201), (1406, 301), (1406, 302), (1406, 402), (1406, 603), (1406, 703), (1406, 704), (1406, 904), (1406, 1004), (1406, 1005), (1406, 1105), (1406, 1206), (1406, 1306), (1406, 1406), (1406, 1407), (1407, 201), (1407, 301), (1407, 302), (1407, 402), (1407, 603), (1407, 703), (1407, 704), (1407, 904), (1407, 1004), (1407, 1005), (1407, 1105), (1407, 1206), (1407, 1306), (1407, 1406), (1407, 1407), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704), (704, 704)] ,
'diff': [(101, 12), (101, 20), (101, 101), (201, 12), (201, 20), (201, 101), (301, 12), (301, 20), (301, 101), (302, 12), (302, 20), (302, 101), (402, 12), (402, 20), (402, 101), (603, 12), (603, 20), (603, 101), (703, 12), (703, 20), (703, 101), (704, 12), (704, 20), (704, 101), (904, 11), (904, 12), (904, 20), (904, 21), (904, 101), (1004, 11), (1004, 12), (1004, 20), (1004, 21), (1004, 101), (1005, 11), (1005, 12), (1005, 20), (1005, 21), (1005, 101), (1105, 11), (1105, 12), (1105, 20), (1105, 21), (1105, 101), (1206, 11), (1206, 12), (1206, 20), (1206, 21), (1206, 101), (1306, 11), (1306, 12), (1306, 20), (1306, 21), (1306, 101), (1406, 11), (1406, 12), (1406, 20), (1406, 21), (1406, 101), (1407, 11), (1407, 12), (1407, 20), (1407, 21), (1407, 101)] ,
}

species_joined = {
'species': [0, 11, 12, 13, 14, 15, 16, 20, 21, 101, 201, 301, 302, 402, 603, 703, 704, 904, 1004, 1005, 1105, 1206, 1306, 1406, 1407] ,
'incl': [(301, 201), (302, 201), (402, 201), (402, 302), (603, 201), (603, 301), (603, 302), (603, 402), (703, 201), (703, 301), (703, 402), (703, 603), (704, 603), (904, 402), (1004, 904), (1005, 402), (1005, 904), (1105, 1005), (1206, 201), (1206, 301), (1206, 302), (1206, 402), (1206, 603), (1206, 703), (1206, 704), (1206, 904), (1206, 1004), (1206, 1005), (1206, 1105), (1206, 1206), (1306, 201), (1306, 301), (1306, 302), (1306, 402), (1306, 603), (1306, 703), (1306, 704), (1306, 904), (1306, 1004), (1306, 1005), (1306, 1105), (1306, 1206), (1306, 1306), (1406, 201), (1406, 301), (1406, 302), (1406, 402), (1406, 603), (1406, 703), (1406, 704), (1406, 904), (1406, 1004), (1406, 1005), (1406, 1105), (1406, 1206), (1406, 1306), (1406, 1406), (1407, 201), (1407, 301), (1407, 302), (1407, 402), (1407, 603), (1407, 703), (1407, 704), (1407, 904), (1407, 1004), (1407, 1005), (1407, 1105), (1407, 1206), (1407, 1306), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407), (1407, 1407)] ,
'diff': [(101, 0), (101, 11), (101, 12), (101, 13), (101, 14), (101, 15), (101, 16), (101, 20), (101, 21), (101, 101), (201, 0), (201, 11), (201, 12), (201, 13), (201, 14), (201, 15), (201, 16), (201, 20), (201, 21), (201, 101), (301, 0), (301, 11), (301, 12), (301, 13), (301, 14), (301, 15), (301, 16), (301, 20), (301, 21), (301, 101), (302, 0), (302, 11), (302, 12), (302, 13), (302, 14), (302, 15), (302, 16), (302, 20), (302, 21), (302, 101), (402, 0), (402, 11), (402, 12), (402, 13), (402, 14), (402, 15), (402, 16), (402, 20), (402, 21), (402, 101), (603, 0), (603, 11), (603, 12), (603, 13), (603, 14), (603, 15), (603, 16), (603, 20), (603, 21), (603, 101), (703, 0), (703, 11), (703, 12), (703, 13), (703, 14), (703, 15), (703, 16), (703, 20), (703, 21), (703, 101), (704, 0), (704, 11), (704, 12), (704, 13), (704, 14), (704, 15), (704, 16), (704, 20), (704, 21), (704, 101), (904, 0), (904, 11), (904, 12), (904, 13), (904, 14), (904, 15), (904, 16), (904, 20), (904, 21), (904, 101), (1004, 0), (1004, 11), (1004, 12), (1004, 13), (1004, 14), (1004, 15), (1004, 16), (1004, 20), (1004, 21), (1004, 101), (1005, 0), (1005, 11), (1005, 12), (1005, 13), (1005, 14), (1005, 15), (1005, 16), (1005, 20), (1005, 21), (1005, 101), (1105, 0), (1105, 11), (1105, 12), (1105, 13), (1105, 14), (1105, 15), (1105, 16), (1105, 20), (1105, 21), (1105, 101), (1206, 0), (1206, 11), (1206, 12), (1206, 13), (1206, 14), (1206, 15), (1206, 16), (1206, 20), (1206, 21), (1206, 101), (1306, 0), (1306, 11), (1306, 12), (1306, 13), (1306, 14), (1306, 15), (1306, 16), (1306, 20), (1306, 21), (1306, 101), (1406, 0), (1406, 11), (1406, 12), (1406, 13), (1406, 14), (1406, 15), (1406, 16), (1406, 20), (1406, 21), (1406, 101), (1407, 0), (1407, 11), (1407, 12), (1407, 13), (1407, 14), (1407, 15), (1407, 16), (1407, 20), (1407, 21), (1407, 101)] ,
}

config.x_cut = 1e-4
config.x_cut_proton = 1e-2
config.tau_dec_threshold = np.inf
config.max_mass = 14
config.debug_level = 0 # suppress into statements

import unittest
class TestCsec(unittest.TestCase):
    def test_talys(self):
        cs = cross_sections.TabulatedCrossSection('CRP2_TALYS')
        self.assertEqual(cs.known_species, species_talys['species'])
        self.assertEqual(cs.known_bc_channels, species_talys['incl'])
        self.assertEqual(cs.known_diff_channels, species_talys['diff'])

    def test_peanut(self):
        cs = cross_sections.TabulatedCrossSection('PEANUT_IAS')
        self.assertEqual(cs.known_species, species_peanut['species'])
        self.assertEqual(cs.known_bc_channels, species_peanut['incl'])
        self.assertEqual(cs.known_diff_channels, species_peanut['diff'])

    def test_joined(self):
        cs = cross_sections.CompositeCrossSection([
            (0., cross_sections.TabulatedCrossSection, ('CRP2_TALYS', )),
            (0.14, cross_sections.SophiaSuperposition, ())
        ])
        self.assertEqual(cs.known_species, species_joined['species'])
        self.assertEqual(cs.known_bc_channels, species_joined['incl'])
        self.assertEqual(cs.known_diff_channels, species_joined['diff'])


if __name__ == '__main__':
    unittest.main()