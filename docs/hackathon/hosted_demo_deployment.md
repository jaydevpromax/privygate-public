# Hosted Demo Deployment

Last updated: 2026-05-05

Purpose: publish the dependency-free PrivyGate static web demo through GitHub Pages from the public repository.

## Target

Static demo source:

`app/web/`

Expected GitHub Pages URL after deployment:

`https://jaydevpromax.github.io/privygate-public/`

Do not add this hosted URL to submission pages until it opens correctly in a private browser window.

## What Is Already Prepared

- GitHub Actions workflow: `.github/workflows/pages.yml`
- Static demo files: `app/web/index.html`, `app/web/styles.css`, `app/web/app.js`
- Relative asset paths, so the page works under the repository Pages path.
- No build step and no secrets required.

## Deployment Steps

1. Regenerate the public release package:

```powershell
python .\scripts\prepare_public_release.py --output .\data\generated\public_release_pages --force
```

2. Copy or push the generated public release contents to `jaydevpromax/privygate-public`.

3. In the public GitHub repository, open:

```text
Settings -> Pages
```

4. Set the Pages source to GitHub Actions if it is not already selected.

5. Open the Actions tab and run:

```text
Deploy Web Demo to GitHub Pages
```

You can also trigger it by pushing changes to `main` that touch `app/web/**` or `.github/workflows/pages.yml`.

6. After the workflow succeeds, open:

```text
https://jaydevpromax.github.io/privygate-public/
```

7. Check these states:

- Alice shows `ACCEPT`.
- Bob shows `REJECT`.
- Alice after revocation shows `REJECT`.
- 0G Chain evidence and 0G Storage evidence are visible.
- The page works in a private browser window.

## Update Public Links After Verification

Only after the hosted demo URL works, update:

- GitHub repository README demo section.
- HackQuest project page, if edits are still allowed.
- X profile or pinned post, if useful.
- `deliverables/competition_submission_archive_2026-05-05/submission_links.md`, by creating a new dated archive or an addendum rather than rewriting the frozen snapshot.

## Safety Notes

- The workflow deploys only `app/web`.
- No wallet key, `.env`, contract artifact, dependency directory, thesis document, or internal project note is deployed by GitHub Pages.
- Keep `contracts/.env` local only.
