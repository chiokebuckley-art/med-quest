# Med Quest / Body Ops Academy

An original, elementary-friendly browser game about how the body works. All ten body systems have playable guided missions, lesson cards and museum illustrations. Three Emergency stories practice recognizing danger and getting help. Free Lab explores six interactive anatomy layers on a textured, breathing human model.

## Play

Play online: https://chiokebuckley-art.github.io/med-quest/

For local development, install Node.js 22 or newer:

```sh
npm ci
npm run dev
```

Open http://127.0.0.1:5173/med-quest/. The release preview uses http://127.0.0.1:5190/med-quest/.

```sh
npm test
npm run build
npm run preview
```

The production build uses `/med-quest/`. See DEPLOY.md and SHIP-NOTES.md for deployment and verification status.

## Playable curriculum

| System | Mission | Main interaction |
|---|---|---|
| Skin | Patch the Cut on the Arm | Clean blue gel, swab, ordered dots, bandage snap |
| Bones | Set the Bone | X-ray, align, splint, cast coverage |
| Muscles | Calm the Strain | Comfort zones, simulation pause, healthy range, support snap |
| Blood | Help the Clot Team | Steady diagram pad, support token, platelet observation |
| Heart | Steady the Pump Path | Connect a loop, follow pulse cues, choose everyday habits |
| Lungs | Clear the Airway | Pose match, soft diagram clog, calm counts, adult-help respect |
| Digestion | Explore the Food Path | Trace organs, guide model tokens, choose safe habits |
| Kidneys | Clean the Filter | Sort useful and waste model tokens, trace the urine path |
| Brain | Rest the Signal Hub | Stop play, report a head bump, get adult/professional help |
| Immune | Call the Defense Team | Handwashing zones, barrier patch, defense-cell matches |

Every mission follows Notice → Predict → Act → Observe → Journal, with ordered tool gates, gentle redo, pretend vitals and two required journal answers. Emergency includes breathing trouble, a head bump and an unsafe roadside accident. Its decisions emphasize safe distance and help, not clinical procedures. Emergency records are separate from the ten system discoveries.

Arcade unlocks after saving the corresponding Learn journal and awards one to three practice stars. Free Lab offers Skin, Muscle, Bone, Organs, Pipes and Signals; clickable parts and keyboard labels; rotation, zoom and front reset; jointed arm bending, chest breathing, heartbeat and visible red blood cells in closed body-and-lung circulation; and three pretend fair-test comparisons. Bend arm, Hold bend and Breathe change the demonstration. Pause motion freezes it, Slow flow slows cells, and Follow cells opens a close-up. Blood is always red; blue vessels distinguish return routes. Cells are enlarged and speeds and vessel paths are simplified for learning. Reduced-motion preferences start the demonstration paused.

## Controls and saved progress

Touch or mouse can tap diagram zones, wipe guide spots, connect ordered dots and drag snap pieces. Select the tool first. Every precision gesture has a labeled keyboard alternative. Tab and Enter/Space work throughout. Learn has no deadline; three-second observation demonstrations are simulation pauses, never treatment or healing durations. Pip and soft sounds are optional. Reduced motion follows the device preference.

Journals, discoveries, Arcade stars, settings and last mode persist in localStorage under `medquest.v1.progress`. Failed storage reports an error and rolls back the saved entry and unlock. Progress stays in the current browser/device. There are no accounts, ads, multiplayer, or real patient records.

## Artwork and source

Vite, JavaScript modules, original SVG mission boards and Three.js power the game. The recovered curriculum lives in `content/`; detailed chapter logic is in `src/game/chapters.js`. Content JSON is ASCII-safe. Hard refresh returns to the educational notice and preserves saved progress.

Free Lab loads the self-contained Meshopt-compressed `public/assets/models/MQ_human_anatomy.glb`. Its surface is adapted from MakeHuman's CC0 human base and adult shape data, with natural skin albedo, pore normal/roughness maps, modeled face, five fingers, toes, fitted opaque shorts and a grounded chest-breathing morph. The editable, texture-packed source is `docs/MQ-human-anatomy.blend`. Rebuild with Blender and `scripts/build_anatomy.py`, then `npm run optimize:anatomy`. Upstream asset sources, licenses, hashes and adaptations are retained in `scripts/vendor/makehuman/` and `docs/THIRD-PARTY-ASSETS.md`.

The main academy guide is a photorealistic Black adult, shown on the home and systems screens. Ten anatomy illustrations now appear directly on the system cards as well as in the lessons. Free Lab uses a Black adult shape and natural dark skin texture. The original hero is retained as a source variant; the new hero is recorded alongside the ten anatomy illustrations. Built-in image generation prompts and output filenames are recorded in `docs/ART-PROMPTS.json`. They illustrate simplified concepts and are not a clinical atlas. The original optional Astra PNG slots remain replacement placeholders; cinematic WebM exports are optional and not supplied. Breathing, heart and contained-flow motion run interactively instead. External web fonts have system-font fallbacks.

## Safety notice

Med Quest is a game for learning. Not real medical care. For real injuries, tell a grown-up / get clinical care.

The diagrams, tools, O2 numbers and outcomes are fictional learning mechanics. Blue gel and closed cartoon lines keep operation boards calm. No medical dosing, diagnosis, real injury assessment or return-to-play clearance is provided. See `docs/MEDICAL-EDUCATION-SOURCES.md` for the help-seeking boundaries used in the Emergency and head-bump stories.

## Grown-up reflection guide

Use the source curriculum rubric as a conversation guide: an Explorer names a body part and completes the FIX steps with Pip; a Trainee explains why two tools are chosen and compares a fair test; a Junior Ops learner teaches the idea to a stuffed animal and writes three sentences. The game saves discoveries and practice stars; these labels are reflection prompts, not medical qualifications or automatically assessed ranks.

The realism rendering revision adds broad studio reflections, gentler skin highlights, fine short curl geometry and a face close-up. The current human remains a digital MakeHuman character. The photographic quality target and replacement requirements are recorded in `docs/REALISM-ASSET-BRIEF.md`; artistic realism is not established by automated test results.

The Skin lesson now uses a photorealistic generated Black adult forearm and hand, with practice markers and bandage placement aligned to the forearm. See `docs/SKIN-BOARD-ART.json` for the prompt and `docs/SKIN-LESSON-CHECKS.json` for verification.

## Living anatomy update

All ten mission boards use detailed anatomy artwork. The bone lesson switches from the Black adult forearm to a detailed bone view; the defense lesson uses the human hand for washing and an immune-cell exhibit for the cell sequence. The Free Lab opens with ten animated close-ups, with independent pause, slow motion and restart controls. The existing rotatable 3D body remains below these views. Animation is illustrative: enlarged cells and motion overlays are not physiological measurements.

Verification: 27 automated checks; ten mission previews; ten lab views at desktop and 390px; physical bone-fragment and hand-patch drags; airway hit target; pause, slow motion and clean browser console. See `docs/LIVING-ANATOMY-CHECKS.json`.

The Skin lesson now clears a continuous gel smear as you wipe, shows swab sheen, and places four tied thread stitches directly on the realistic arm. Small stitch guides replace the numbered circles; keyboard controls remain available. See `docs/SKIN-SURFACE-CHECKS.json`.
