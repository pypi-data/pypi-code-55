# Create your tests here.
import unittest

from db.models import Member


class TestThemesList(unittest.TestCase):
    themes = {
        "THEME_DEFAULT": "muses_default",
        "THEME_CLASSIC": "muses_classic",
        "THEME_ROSE": "muses_rose",
        "THEME_BLUE": "muses_blue",
        "THEME_GREEN": "muses_green",
        "THEME_ORANGE": "muses_orange",
    }

    def test_themes_in_choices(self):
        m = Member()
        for k in self.themes:
            self.assertEquals(self.themes[k], getattr(m, k), msg=f"Member not contains {self.themes[k]}")


if __name__ == '__main__':
    unittest.main()
