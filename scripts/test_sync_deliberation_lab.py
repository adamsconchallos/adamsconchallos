# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import sync_deliberation_lab as s


class TestRename(unittest.TestCase):
    def test_full_names(self):
        self.assertEqual(s.rename("Nora Varela said hello"), "Amélie Maturana said hello")
        self.assertEqual(s.rename("Sima Rao and Faye Lin"), "Oleo Cebaroa and Roberto Nothomb")

    def test_first_names(self):
        self.assertEqual(s.rename("Thank Nora and ask Ian"), "Thank Amélie and ask Humberto")
        self.assertEqual(s.rename("Tomas warns; Faye notes"), "Nicanor warns; Roberto notes")

    def test_word_boundaries_do_not_touch_substrings(self):
        self.assertEqual(s.rename("linguistic Iranian"), "linguistic Iranian")


if __name__ == "__main__":
    unittest.main()
