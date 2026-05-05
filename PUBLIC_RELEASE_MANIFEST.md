# Public Release Manifest

Source commit: `005b950`

This directory is a clean public-release candidate for hackathon judging.
It intentionally excludes thesis deliverables, defense materials, project control notes, and generated local artifacts.

## Included Roots

- `README.md`
- `.gitattributes`
- `.gitignore`
- `scripts/generate_hackathon_assets.py`
- `scripts/generate_storage_audit_manifest.py`
- `scripts/hackathon_readiness_check.py`
- `scripts/external_dependency_check.py`
- `scripts/privygate_cli.py`
- `scripts/run_core_demo.py`
- `scripts/update_submission_links.py`
- `.github`
- `app`
- `contracts`
- `docs/engineering`
- `docs/hackathon`
- `experiments`
- `storage`
- `src`
- `tests`

## Excluded Private Roots

- `deliverables`
- `docs/project`
- `docs/thesis`
- `references`
- `data/generated`

## Before Publishing

1. Run `python scripts/hackathon_readiness_check.py` inside this export.
2. If publishing the hosted web demo, enable GitHub Pages with the included `.github/workflows/pages.yml` workflow.
3. Replace final GitHub, video, X, contract, and Explorer links.
4. Run strict readiness after replacing links.
5. Publish this export to a clean public repository or orphan public branch, not the private thesis repository history.
