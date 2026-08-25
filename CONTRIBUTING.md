# Contributing to Agent Memory Governance

Thank you for your interest in improving this project. This repository is a **governance guide / Skill**, not a fixed tool, so contributions should extend or clarify the principles without turning them into a mandatory workflow.

## How to Contribute

1. **Open an issue first** for substantial changes (new platform guide, changes to core principles, new deployment patterns).
2. **Fork the repository** and create a feature branch.
3. **Make focused changes** — one logical change per PR.
4. **Run the tests** before submitting:
   ```bash
   python -m unittest discover -s tests -v
   ```
5. **Regenerate diagrams** if you change the repository structure:
   ```bash
   python tools/generate_diagrams.py
   ```
6. **Open a pull request** with a clear description and link to the related issue.

## What We Welcome

- Bug fixes in scripts
- Clarifications or corrections to the governance principles
- New platform integration guides under `references/`
- Additional tests
- Translations (prefer separate files, e.g. `README.zh.md`)

## What We Avoid

- Turning the Skill into a hard-coded workflow or command set
- Adding runtime dependencies to `scripts/memory_health.py` (it must remain stdlib-only)
- Auto-executing deletes, archives, or memory rewrites in example code
- Including personal data, private memory contents, or secrets in any file or commit

## Commit Message Style

Use conventional-commit prefixes:

- `feat:` — new principle, guide, or capability
- `fix:` — bug fix
- `docs:` — documentation changes
- `chore:` — tooling, CI, formatting
- `test:` — test additions or fixes

## Bilingual Conventions

This project is bilingual (English / 中文). When editing:

- Keep English and Chinese paragraphs or bullet points adjacent.
- Do not translate file names or code identifiers.
- Preserve the same meaning in both languages; do not add extra details in only one language.

## Code of Conduct

Be respectful, assume good intent, and focus on making long-running agents safer and more transparent for everyone.
