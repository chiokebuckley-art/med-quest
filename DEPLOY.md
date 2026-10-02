# Deploy Med Quest

Repository: https://github.com/chiokebuckley-art/med-quest
Pages: https://chiokebuckley-art.github.io/med-quest/

The public repository was created October 1, 2026. The connected GitHub account has admin/push access. Source upload and release checks are in progress; browser access is available. The earlier sign-in blocker is resolved.

The workflow `.github/workflows/deploy-pages.yml` installs locked dependencies on Node 22, runs `npm test`, builds with `/med-quest/`, and deploys `dist/` from main. Pull requests run build/test without publishing.

In GitHub repository Settings → Pages → Build and deployment, choose GitHub Actions. After merging a tested release PR, inspect the Actions run and open the public URL. Verify the educational notice, all mission paths, journal persistence, Lab loading, phone layout and console before recording live success in SHIP-NOTES.md.

For later local pushes, authenticate the official GitHub CLI or Git credential helper on this machine:

```sh
gh auth login
git remote -v
git fetch origin
```

Review remote history before integrating local changes. Do not force-push. A connected GitHub API can also upload Git blobs/tree/commit and update a release branch without installing or storing a new credential locally.

To trigger or inspect the deployment using an authenticated CLI:

```sh
gh workflow run deploy-pages.yml --repo chiokebuckley-art/med-quest
gh run list --repo chiokebuckley-art/med-quest --limit 5
gh api repos/chiokebuckley-art/med-quest/pages
```

The release commit, PR, successful Actions run and deployed verification will be linked in SHIP-NOTES.md after they exist.
