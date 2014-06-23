# -*- coding: utf-8 -*-

__author__ = 'aclemen1'

import unittest
import main


class TestStringModifiers(unittest.TestCase):
    def test_diacritics(self):
        self.assertEqual(
            'eeaauoc',
            main.remove_diacritics('éèàäüöç')
        )

    def test_non_printable(self):
        self.assertEqual(
            '',
            main.remove_non_printable('/\\%&()=?!$£§°<>-*+,;.:')
        )

    def test_multiple_spaces(self):
        self.assertEqual(
            '',
            main.remove_multiple_spaces('  ')
        )
        self.assertEqual(
            'a b c',
            main.remove_multiple_spaces('  a  b  c  ')
        )

    def test_underscore_to_space(self):
        self.assertEqual(
            'A_B',
            main.substitute_underscore_to_space('A_ B')
        )
        self.assertEqual(
            'A_B',
            main.substitute_underscore_to_space('A _B')
        )
        self.assertEqual(
            'A_B_C_D_E',
            main.substitute_underscore_to_space('A B C D E')
        )
        self.assertEqual(
            'A_B',
            main.substitute_underscore_to_space('A  B')
        )
        self.assertEqual(
            'A__B',
            main.substitute_underscore_to_space('A_  _B')
        )

    def test_underscore_to_minus(self):
        self.assertEqual(
            'A_B',
            main.substitute_underscore_to_minus('A_-B')
        )
        self.assertEqual(
            'A_B',
            main.substitute_underscore_to_minus('A-_B')
        )
        self.assertEqual(
            'A_B_C_D_E',
            main.substitute_underscore_to_minus('A-B-C-D-E')
        )
        self.assertEqual(
            'A_B',
            main.substitute_underscore_to_minus('A--B')
        )
        self.assertEqual(
            'A__B',
            main.substitute_underscore_to_minus('A_--_B')
        )

    def test_underscore_to_periods(self):
        self.assertEqual(
            'A_B',
            main.substitute_underscore_to_periods('A_.B')
        )
        self.assertEqual(
            'A_B',
            main.substitute_underscore_to_periods('A._B')
        )
        self.assertEqual(
            'A_B_C_D_E',
            main.substitute_underscore_to_periods('A.B.C.D.E')
        )
        self.assertEqual(
            'A_B',
            main.substitute_underscore_to_periods('A..B')
        )
        self.assertEqual(
            'A__B',
            main.substitute_underscore_to_periods('A_.._B')
        )

    def test_underscores(self):
        self.assertEqual(
            'A',
            main.strip_underscores('_A_')
        )

    def test_standardize(self):
        self.assertEqual(
            'vie_est__super__long_fleuve_tranquille_pas_douter',
            main.standardize('la vie, est un __super__ long fleuve tranquille, à n\'en pas douter .-*+&%/()')
        )


if __name__ == '__main__':
    unittest.main()
