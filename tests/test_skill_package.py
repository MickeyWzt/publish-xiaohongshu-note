import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


class SkillPackageTests(unittest.TestCase):
    def test_required_package_files_exist(self):
        required = [
            ROOT / "SKILL.md",
            ROOT / "agents" / "openai.yaml",
            ROOT / "references" / "publishing-playbook.md",
        ]

        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertEqual(missing, [], f"Missing required package files: {missing}")

    def test_skill_frontmatter_identifies_package(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = content.split("---", 2)

        self.assertGreaterEqual(len(frontmatter), 3, "SKILL.md needs YAML frontmatter")
        self.assertRegex(
            frontmatter[1], r"(?m)^name:\s*publish-xiaohongshu-note\s*$"
        )
        self.assertRegex(frontmatter[1], r"(?m)^description:\s*\S.+$")

    def test_agent_metadata_references_skill(self):
        content = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertRegex(content, r'(?m)^\s*display_name:\s*"\S.+"\s*$')
        self.assertRegex(content, r'(?m)^\s*short_description:\s*"\S.+"\s*$')
        self.assertRegex(
            content,
            r'(?m)^\s*default_prompt:\s*"[^"\n]*\$publish-xiaohongshu-note[^"\n]*"\s*$',
        )

    def test_relative_markdown_links_resolve(self):
        broken = []

        for markdown in ROOT.rglob("*.md"):
            if ".git" in markdown.parts:
                continue
            content = markdown.read_text(encoding="utf-8")
            for match in LINK_PATTERN.finditer(content):
                target = match.group(1).strip().strip("<>")
                target = target.split(maxsplit=1)[0]
                parsed = urlparse(target)
                if parsed.scheme or target.startswith("#"):
                    continue
                path_text = unquote(parsed.path)
                if not path_text:
                    continue
                resolved = markdown.parent / path_text
                if not resolved.exists():
                    broken.append(f"{markdown.relative_to(ROOT)} -> {target}")

        self.assertEqual(broken, [], f"Broken relative Markdown links: {broken}")


if __name__ == "__main__":
    unittest.main()
