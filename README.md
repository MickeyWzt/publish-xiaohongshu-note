# Publish Xiaohongshu Note

A Codex skill for publishing prepared Xiaohongshu image notes through the user's logged-in Chrome session. It covers duplicate checks, ordered multi-image upload, truthful declarations, final-publish authorization, recovery, and Note Manager verification.

## What the skill protects

- Uses the designated logged-in Chrome session without reading credentials or cookies.
- Checks the complete image package, title, body, tags, and required declarations before upload.
- Treats drafting, uploading, and final publishing as separate authorization levels.
- Verifies the exact note in Note Manager instead of relying on a transient success toast.
- Stops safely on login, CAPTCHA, risk-control, or ambiguous publish outcomes.

## Install

Copy or clone this repository into the Codex skills directory:

```powershell
git clone https://github.com/MickeyWzt/publish-xiaohongshu-note.git "$env:USERPROFILE\.codex\skills\publish-xiaohongshu-note"
```

Then invoke it explicitly in a new task:

```text
Use $publish-xiaohongshu-note to upload this prepared image note in Chrome, stop before publishing, and verify the draft.
```

Final publication still requires explicit authorization in the current request or automation.

## Package layout

```text
publish-xiaohongshu-note/
├── SKILL.md
├── agents/openai.yaml
└── references/publishing-playbook.md
```

Read [the publishing playbook](references/publishing-playbook.md) for the browser-action pattern and recovery matrix.

## Verify the package

Run the standard-library checks before publishing changes:

```powershell
python -m unittest discover -s tests -v
```

The checks validate the required files, Skill frontmatter, agent metadata, and local Markdown links.
