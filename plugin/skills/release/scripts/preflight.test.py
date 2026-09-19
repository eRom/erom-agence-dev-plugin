"""Suite de comportement de preflight.py : lance le script voisin sur des cas construits.

Chaque cas écrit un plugin.json et un marketplace.json temporaires, pointe HOME vers un
dossier jetable, et n'asserte que le code de sortie et les chemins nommés en sortie.
Usage : uv run --no-project python preflight.test.py
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("preflight.py")


def run(descriptions, *, release="erom-research", plugin_version="1.0.0",
        market_version="1.0.0", home_dirs=(), home_files=()):
    """Construit un home et une marketplace, lance le préflight, rend (code, sortie)."""
    tmp = Path(tempfile.mkdtemp())
    home = tmp / "home"
    home.mkdir()
    for d in home_dirs:
        (home / d).mkdir(parents=True, exist_ok=True)
    for f in home_files:
        (home / f).parent.mkdir(parents=True, exist_ok=True)
        (home / f).write_text("x")
    plugins = [{"name": name, "source": "./x", "version": market_version, "description": desc}
               for name, desc in descriptions.items()]
    market = tmp / "marketplace.json"
    market.write_text(json.dumps({"name": "m", "owner": {"name": "o"}, "plugins": plugins}))
    manifest = tmp / "plugin.json"
    manifest.write_text(json.dumps({"name": release, "version": plugin_version}))
    r = subprocess.run([sys.executable, str(SCRIPT), str(manifest), str(market)],
                       capture_output=True, text=True, env={**os.environ, "HOME": str(home)})
    return r.returncode, r.stdout + r.stderr


class MustFire(unittest.TestCase):
    def test_renamed_store_dir(self):
        code, out = run({"erom-research": "Rapports dans ~/.claude/erom-plugin-artefacts/researchs/ (frontmatter)."},
                        home_dirs=[".claude/erom-store/researchs"])
        self.assertEqual(code, 3)
        self.assertIn("erom-plugin-artefacts/researchs/", out)

    def test_dead_path_in_neighbour_entry(self):
        # L'incident réel : la release d'erom-insight laisse passer l'entrée voisine.
        code, out = run({"erom-insight": "Rien.", "erom-research": "Voir ~/.claude/erom-plugins/researchs/."},
                        release="erom-insight")
        self.assertEqual(code, 3)
        self.assertIn("erom-research", out)

    def test_template_with_dead_prefix(self):
        code, _ = run({"erom-research": "Écrit ~/.claude/old-store/insights/<owner>-<repo>-<YYYY-MM-DD>.md"})
        self.assertEqual(code, 3)

    def test_sentence_final_dot_on_dead_dir(self):
        code, _ = run({"erom-research": "Sauvé dans ~/.claude/erom-plugins/insights/."})
        self.assertEqual(code, 3)

    def test_two_dead_paths_both_named(self):
        code, out = run({"a": "Voir ~/.claude/gone-a/", "b": "Voir ~/.claude/gone-b/x.md"}, release="a")
        self.assertEqual(code, 3)
        self.assertIn("gone-a", out)
        self.assertIn("gone-b", out)

    def test_missing_script_file(self):
        code, _ = run({"erom-research": "Garde ~/.claude/scripts/guard-tools.sh"}, home_dirs=[".claude/scripts"])
        self.assertEqual(code, 3)

    def test_dead_path_still_reported_on_divergence(self):
        # La divergence garde son code 1, mais le chemin mort reste affiché.
        code, out = run({"erom-research": "Voir ~/.claude/gone/"}, plugin_version="1.1.0")
        self.assertEqual(code, 1)
        self.assertIn("~/.claude/gone", out)


class MustStaySilent(unittest.TestCase):
    def test_existing_dir_with_final_dot(self):
        code, _ = run({"erom-insight": "Rapport dans ~/.claude/erom-store/insights/."},
                      release="erom-insight", home_dirs=[".claude/erom-store/insights"])
        self.assertEqual(code, 0)

    def test_template_with_live_prefix(self):
        code, _ = run({"erom-insight": "Écrit ~/.claude/erom-store/insights/<owner>-<repo>-<YYYY-MM-DD>.md"},
                      release="erom-insight", home_dirs=[".claude/erom-store/insights"])
        self.assertEqual(code, 0)

    def test_no_home_path(self):
        code, _ = run({"erom-research": "Quatre moteurs de deep research."})
        self.assertEqual(code, 0)

    def test_bare_tilde(self):
        code, _ = run({"erom-research": "Installe tout sous ~ ou ~/ selon le cas."})
        self.assertEqual(code, 0)

    def test_glob_with_live_prefix(self):
        code, _ = run({"erom-research": "Lit ~/.claude/projects/*/*.jsonl"}, home_dirs=[".claude/projects"])
        self.assertEqual(code, 0)

    def test_existing_file(self):
        code, _ = run({"erom-research": "Garde ~/.claude/scripts/guard-tools.sh"},
                      home_files=[".claude/scripts/guard-tools.sh"])
        self.assertEqual(code, 0)

    def test_divergence_code_unchanged(self):
        code, _ = run({"erom-research": "Rien."}, plugin_version="1.1.0")
        self.assertEqual(code, 1)

    def test_first_publication_code_unchanged(self):
        code, _ = run({"autre": "Rien."}, release="erom-research")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
