# Personal Website (Quarto)

This repository contains the source for `https://www.adamsceballos.com`.

## Fast content workflow

Create a new blog post:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\new-post.ps1 -Title "Your post title"
```

Create a new research entry:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\new-research.ps1 -Title "Your paper title"
```

Common optional arguments:
- `-Slug "custom-slug"`
- `-Date "yyyy-MM-dd"`
- Blog only: `-Description "One-line summary"` and `-Language english|spanish`
- Research only: `-Doi "10.xxxx/xxxxx"`

## Deployment

GitHub Pages deployment is automated with `.github/workflows/quarto-pages.yml`.
On pushes to `main` (or `master`), the workflow renders with `quarto render --no-execute` and deploys the `docs/` output.
