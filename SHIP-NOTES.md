# Med Quest release notes

Release: 1.1.0 · October 1, 2026

Public repository: https://github.com/chiokebuckley-art/med-quest
Public target: https://chiokebuckley-art.github.io/med-quest/
Local production preview: http://127.0.0.1:5190/med-quest/

Status: the public repository is created. Full source transfer, pull request checks and Pages deployment are in progress. Public success is not yet claimed. This file will record the actual deployed revision and workflow after verification.

## Delivered game

All ten system missions are playable, including the original skin, bone and breathing missions with their specified order gates. Seven additional systems have distinct diagrams and interactions: muscle comfort, blood clot helpers, heart-loop connection, digestion tracing, kidney token sorting, brain/help decisions and immune defense matches. Each ends with observation and a saved journal. There are no unfinished system operation screens.

Emergency has three playable decision stories: breathing trouble, a head bump and a dangerous roadside scene. Children practice recognizing danger and obtaining adult/professional help. Emergency never claims to teach real injury treatment or qualify a player for clinical care.

Arcade unlocks per saved Learn discovery and retains practice stars. Free Lab includes six anatomy layers, selectable parts, keyboard labels, camera controls, human skin texture and detailed hands/feet/face, fitted shorts, grounded breathing, heart/lung motion and contained vessel flow. The editable Blender source, CC0 upstream graphical assets, adaptation scripts and licenses are included.

Eleven finished museum illustrations, generated with the built-in image tool, are integrated into the hero and all system lessons. The original optional Astra placeholder paths remain available for replacement; no cinematic WebM clips are supplied. Interactive motion is implemented in the body explorer. Anatomy is educationally simplified.

## Verified locally

- 21 automated tests pass: core thresholds/order/snap gates, persistence recovery and rollback, human geometry/textures/morph decoding, all seven additional system missions and all three Emergency stories.
- Production build passes with the correct `/med-quest/` base. The JavaScript runtime is approximately 191 kB gzipped; Vite reports a large uncompressed chunk warning.
- Browser journeys complete all ten systems and all three Emergency stories. Thirteen journals and all ten system discoveries survive refresh; Emergency records do not inflate system progress.
- Skin rejects stitch-first, empty journals are rejected, and the breathing journal requires adult/help language. Exact cleaning, swab and cast thresholds remain intact.
- Arcade starts locked before a Learn discovery. A completed heart replay awards three stars, which survive refresh.
- New muscle support was placed with a physical drag; original bandage, bone and stitch gestures were verified in earlier checks of the unchanged core boards. Keyboard alternatives complete all mission paths.
- All six human layers, part facts, rotation/zoom/reset and reduced-motion behavior were previously verified with the same model and Lab implementation.

Desktop hero and 390x780 home, lesson, Emergency and kidney sorting views show no horizontal overflow. Updated production checks show no browser errors/warnings. Deployed-build checks will be recorded after launch. `AGENT-RUNBOOK.md` tracks the remaining gates.

## Release package

`med-quest-release.zip` beside the local repository will contain the full source, lockfile, production dist, editable human source, tests, artwork and deployment notes. Installed dependencies and Git internals are omitted. The final ZIP is regenerated after public verification.

Med Quest is a game for learning. Not real medical care. For real injuries, tell a grown-up / get clinical care.
