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


class TestNavBar(unittest.TestCase):
    def test_active_tab_marked_en(self):
        html = s.nav_bar("profiles", "en")
        self.assertIn('nav-link active" href="/projects/deliberation-lab/profiles.html"', html)
        self.assertIn(">Profiles</a>", html)

    def test_switch_en_points_to_es_home(self):
        html = s.nav_bar("about", "en")
        self.assertIn('href="/projects/deliberation-lab/es/index.html"', html)
        self.assertIn(">Español</a>", html)

    def test_spanish_labels_base_and_switch(self):
        html = s.nav_bar("about", "es")
        self.assertIn('nav-link active" href="/projects/deliberation-lab/es/index.html"', html)
        for label in ["Inicio", "Declaraciones", "Conversaciones", "Reflexiones", "Perfiles"]:
            self.assertIn(f">{label}</a>", html)
        self.assertIn('href="/projects/deliberation-lab/index.html"', html)  # switch to EN
        self.assertIn(">English</a>", html)


class TestPageAssembly(unittest.TestCase):
    SAMPLE = "# Public Deliberations\n\nConversation: X\nTurns: 6\n\n## turn_0\n\nbody text\n"

    def test_strip_h1_and_intro(self):
        out = s.strip_h1_and_intro(self.SAMPLE)
        self.assertTrue(out.startswith("## turn_0"))
        self.assertNotIn("Public Deliberations", out)

    def test_front_matter_with_and_without_date(self):
        self.assertIn('date: "2026-06-27"', s.front_matter("H", "2026-06-27"))
        self.assertNotIn("date:", s.front_matter("H"))

    def test_build_page_orders_sections(self):
        page = s.build_page("Conversations", "conversations", "en", "## turn_0\n\nbody\n")
        self.assertTrue(page.startswith("---"))
        self.assertIn("nav nav-pills", page)
        self.assertTrue(page.rstrip().endswith("body"))

    def test_build_page_banner(self):
        page = s.build_page("T", "conversations", "es", "body\n", banner="NOTE-ES")
        self.assertIn("callout-note", page)
        self.assertIn("NOTE-ES", page)


class TestJointStatements(unittest.TestCase):
    SAMPLE = (
        "# Joint Statements\n\nStatements: 2\n\n"
        "## joint_000001\n\n- Published at: 2026-06-27T05:37:12.169264+00:00\n\n**Public statement**\n\nfirst\n\n"
        "## joint_000002\n\n- Published at: 2026-07-04T00:00:00+00:00\n\n**Public statement**\n\nsecond\n"
    )

    def test_parse_ids_published_body(self):
        stmts = s.parse_joint_statements(self.SAMPLE)
        self.assertEqual([x["id"] for x in stmts], ["joint_000001", "joint_000002"])
        self.assertEqual(stmts[0]["published_at"], "2026-06-27T05:37:12.169264+00:00")
        self.assertTrue(stmts[0]["body"].startswith("## joint_000001"))
        self.assertIn("first", stmts[0]["body"])

    def test_slug(self):
        stmts = s.parse_joint_statements(self.SAMPLE)
        self.assertEqual(s.statement_slug(stmts[0]), "2026-06-27-joint-000001")
        self.assertEqual(s.statement_slug(stmts[1]), "2026-07-04-joint-000002")


class TestRegender(unittest.TestCase):
    def test_regender_pronouns(self):
        self.assertEqual(s.regender("She begins from her lived experience"),
                         "He begins from his lived experience")

    def test_only_phenomenologist_block_changes(self):
        md = (
            "## Amélie Maturana\n\nShe holds objectivity in parenthesis.\n\n"
            "## Roberto Nothomb\n\nShe notices tone and her habit.\n\n"
            "## Oleo Cebaroa\n\nShe resists timeless definitions.\n"
        )
        out = s.regender_phenomenologist(md)
        self.assertIn("## Amélie Maturana\n\nShe holds", out)
        self.assertIn("## Oleo Cebaroa\n\nShe resists", out)
        self.assertIn("He notices tone and his habit", out)

    def test_does_not_touch_hermeneutic(self):
        self.assertEqual(s.regender("hermeneutic relations"), "hermeneutic relations")


if __name__ == "__main__":
    unittest.main()
