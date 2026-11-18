# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import sync_deliberation_lab as s


class TestRename(unittest.TestCase):
    def test_full_names(self):
        self.assertEqual(s.rename("Nora Varela said hello"), "Amélie Maturana said hello")
        self.assertEqual(s.rename("Tomas Echeverria and Ian Mercado"), "Nicanor Bolaño and Humberto Parra")

    def test_first_names(self):
        self.assertEqual(s.rename("Thank Nora and ask Ian"), "Thank Amélie and ask Humberto")
        self.assertEqual(s.rename("Tomas warns"), "Nicanor warns")

    def test_removed_agents_are_not_mapped(self):
        # Faye Lin / Sima Rao were removed; their names must pass through untouched
        self.assertEqual(s.rename("Faye Lin and Sima Rao"), "Faye Lin and Sima Rao")

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


class TestPresentation(unittest.TestCase):
    def test_wrap_tabset(self):
        out = s.wrap_tabset("## A\n\nx\n\n## B\n\ny\n")
        self.assertTrue(out.startswith("::: {.panel-tabset}"))
        self.assertTrue(out.rstrip().endswith(":::"))
        self.assertIn("## A", out)
        self.assertIn("## B", out)

    CONV = (
        "# Public Deliberations\n\nTurns: 2\n\n"
        "## turn_000000 | Round 0 | Amélie Maturana\n\n- Role: ontologist\n- Created at: X\n\nHello there.\n\n"
        "## turn_000005 | Round 5 | Public\n\n- Role: joint_statement\n- Created at: Y\n\nWe agree.\n"
    )

    def test_style_normal_turn(self):
        out = s.style_conversation(self.CONV)
        self.assertIn("### Amélie Maturana · Round 0", out)
        self.assertIn("*ontologist*", out)
        self.assertIn("Hello there.", out)
        self.assertIn("---", out)
        self.assertNotIn("## turn_", out)

    def test_style_joint_statement(self):
        out = s.style_conversation(self.CONV)
        self.assertIn('callout-note title="Joint statement · Round 5"', out)
        self.assertIn("We agree.", out)


import tempfile
from pathlib import Path


class TestSyncIntegration(unittest.TestCase):
    def _fixture(self, d: Path):
        (d / "public_deliberations.md").write_text(
            "# Public Deliberations\n\nTurns: 1\n\n"
            "## turn_000000 | Round 0 | Nora Varela\n\n- Role: Maturana-influenced ontologist\n"
            "- Created at: 2026-06-27T05:34:08+00:00\n\nNora speaks. Ask Ian.\n",
            encoding="utf-8")
        (d / "private_reflections.md").write_text(
            "# Private Reflections\n\n## Tomas Echeverria\n\nReflection by Tomas.\n", encoding="utf-8")
        (d / "agent_profiles.md").write_text(
            "# Agent Profiles\n\nCentral question: X\n\n"
            "## Ian Mercado\n\n- Role: instrumentalist\nHe judges by predictions.\n\n"
            "## Tomas Echeverria\n\n- Role: theologian\nHe asks who is responsible.\n", encoding="utf-8")
        (d / "joint_statements.md").write_text(
            "# Joint Statements\n\nStatements: 1\n\n## joint_000001\n\n"
            "- Published at: 2026-06-27T05:37:12+00:00\n\n**Public statement**\n\nNora agrees.\n",
            encoding="utf-8")

    def test_sync_en_renames(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"; src.mkdir()
            out = Path(tmp) / "out"; out.mkdir()
            self._fixture(src)
            s.sync(src, out, lang="en")
            conv = (out / "conversations.qmd").read_text(encoding="utf-8")
            self.assertIn("### Amélie Maturana · Round 0", conv)
            self.assertIn("Ask Humberto", conv)
            self.assertNotIn("## turn_", conv)
            prof = (out / "profiles.qmd").read_text(encoding="utf-8")
            self.assertIn("## Nicanor Bolaño", prof)
            self.assertIn("## Humberto Parra", prof)
            self.assertNotIn("Roberto Nothomb", prof)
            self.assertNotIn("Oleo Cebaroa", prof)
            self.assertIn("::: {.panel-tabset}", prof)
            post = out / "statements" / "2026-06-27-joint-000001" / "index.qmd"
            self.assertIn("Amélie agrees", post.read_text(encoding="utf-8"))

    def test_sync_es_titles_and_banner(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"; src.mkdir()
            out = Path(tmp) / "out"; out.mkdir()
            self._fixture(src)
            s.sync(src, out, lang="es", banner="EN ORIGINAL")
            conv = (out / "conversations.qmd").read_text(encoding="utf-8")
            self.assertIn('title: "Conversaciones"', conv)
            self.assertIn("callout-note", conv)
            self.assertIn("EN ORIGINAL", conv)
            self.assertIn("Amélie Maturana", conv)
            post = out / "statements" / "2026-06-27-joint-000001" / "index.qmd"
            self.assertIn('title: "Declaración conjunta — 2026-06-27"',
                          post.read_text(encoding="utf-8"))

    def test_statements_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"; src.mkdir()
            out = Path(tmp) / "out"; out.mkdir()
            self._fixture(src)
            s.sync(src, out, lang="en")
            post = out / "statements" / "2026-06-27-joint-000001" / "index.qmd"
            post.write_text("EDITED BY HAND", encoding="utf-8")
            s.sync(src, out, lang="en")
            self.assertEqual(post.read_text(encoding="utf-8"), "EDITED BY HAND")


if __name__ == "__main__":
    unittest.main()
