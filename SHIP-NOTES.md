# Med Quest release notes

Release: 1.1.0 · October 1, 2026

Public repository: https://github.com/chiokebuckley-art/med-quest
Play online: https://chiokebuckley-art.github.io/med-quest/
Local production preview: http://127.0.0.1:5190/med-quest/

Status: shipped and verified on public HTTPS GitHub Pages.

Runtime revision: `a002350a186b37889a43799536924a24376bd493`.

- Full release PR: https://github.com/chiokebuckley-art/med-quest/pull/1 (merged; checks passed).
- Kidney wording correction: https://github.com/chiokebuckley-art/med-quest/pull/2 (merged; checks passed).
- Successful build and Pages deployment: https://github.com/chiokebuckley-art/med-quest/actions/runs/36947138331.
- Live journey evidence: `docs/LIVE-BROWSER-CHECKS.json` and four `docs/live-*.png` screenshots.
- Every one of the 63 production files returned HTTP 200 and matched the local build SHA-256: `docs/LIVE-ASSET-CHECKS.json`.

Documentation-only release commits do not change the verified runtime.

## Delivered game

All ten system missions are playable, including the original skin, bone and breathing missions with their specified order gates. Seven additional systems have distinct diagrams and interactions: muscle comfort, blood clot helpers, heart-loop connection, digestion tracing, kidney token sorting, brain/help decisions and immune defense matches. Each ends with observation and a saved journal. There are no unfinished system operation screens.

Emergency has three playable decision stories: breathing trouble, a head bump and a dangerous roadside scene. Children practice recognizing danger and obtaining adult/professional help. Emergency never claims to teach real injury treatment or qualify a player for clinical care.

Arcade unlocks per saved Learn discovery and retains practice stars. Free Lab includes six anatomy layers, selectable parts, keyboard labels, camera controls, human skin texture and detailed hands/feet/face, fitted shorts, grounded breathing, heart/lung motion and contained vessel flow. The editable Blender source, CC0 upstream graphical assets, adaptation scripts and licenses are included.

Eleven finished museum illustrations, generated with the built-in image tool, are integrated into the hero and all system lessons. The original optional Astra placeholder paths remain available for replacement; no cinematic WebM clips are supplied. Interactive motion is implemented in the body explorer. Anatomy is educationally simplified.

## Verified locally and live

- 21 automated tests pass: core thresholds/order/snap gates, persistence recovery and rollback, human geometry/textures/morph decoding, all seven additional system missions and all three Emergency stories.
- Production build passes with the correct `/med-quest/` base. The JavaScript runtime is approximately 191 kB gzipped; Vite reports a large uncompressed chunk warning.
- Browser journeys complete all ten systems and all three Emergency stories. Thirteen journals and all ten system discoveries survive refresh; Emergency records do not inflate system progress.
- Skin rejects stitch-first, empty journals are rejected, and the breathing journal requires adult/help language. Exact cleaning, swab and cast thresholds remain intact.
- Arcade starts locked before a Learn discovery. A completed heart replay awards three stars, which survive refresh.
- New muscle support was placed with a physical drag; original bandage, bone and stitch gestures were verified in earlier checks of the unchanged core boards. Keyboard alternatives complete all mission paths.
- All six human layers, part facts, rotation/zoom/reset and reduced-motion behavior were previously verified with the same model and Lab implementation.

Desktop hero and 390x780 home, lesson, Emergency and kidney sorting views show no horizontal overflow. Updated production checks show no browser errors/warnings. The same public build passed the live acceptance journeys, all six layers and phone checks. `AGENT-RUNBOOK.md` records the completed release gates.

## Release package

`med-quest-release.zip` beside the local repository contains the full source, lockfile, production dist, editable human source, tests, artwork and deployment notes. Installed dependencies and Git internals are omitted. The package is generated after public verification; its SHA-256 and archive checks are recorded in the adjacent `med-quest-release-checks.json`.

## Release boundaries

GOAL.md's v1 success checklist is fulfilled; the seven planned placeholder missions and permitted Emergency stub were expanded into playable lessons. Broader PDF roadmap features remain optional future work: timed Emergency idle drains, sequential Free Lab piece locks, automated trainee-rank assessment, cinematic clips and additional audio variants. This release keeps Free Lab open and Emergency pause-friendly, uses saved Learn progress to unlock Arcade, and offers optional soft step/success sounds. It does not claim those roadmap features are shipped.

Generated illustrations and simplified inner anatomy are museum-style educational representations. This is a completed browser-game release, not a clinical simulation or photorealistic cinematic package.

Med Quest is a game for learning. Not real medical care. For real injuries, tell a grown-up / get clinical care.
