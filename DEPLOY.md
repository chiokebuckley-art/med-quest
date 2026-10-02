# Deploy Med Quest

Repository: https://github.com/chiokebuckley-art/med-quest
Pages: https://chiokebuckley-art.github.io/med-quest/

Published and verified October 1, 2026 (America/Chicago). GitHub Actions is configured as the Pages source. The release PR and kidney correction are merged, with successful build/test and Pages deployment. See SHIP-NOTES.md for the verified runtime revision and live evidence.

The workflow `.github/workflows/deploy-pages.yml` installs locked dependencies on Node 22, runs `npm test`, builds with `/med-quest/`, and deploys `dist/` from main. Pull requests run build/test without publishing.

For a replacement repository, choose GitHub Actions in Settings → Pages → Build and deployment. This repository is already configured. After merging a tested release PR, inspect the Actions run and open the public URL. Verify the educational notice, all mission paths, journal persistence, Lab loading, phone layout and console before recording live success in SHIP-NOTES.md.

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

The release commit, merged PRs, successful deployment and live verification are linked in SHIP-NOTES.md.
