# Human surface asset provenance

The game code, mission artwork, internal anatomy, garment design and generated surface normal/roughness textures are original Med Quest work. The detailed human surface is adapted from MakeHuman's hm08 base mesh and core asset data, which are CC0. This replaces the earlier procedural mannequin; the entire character is no longer described as original geometry.

Core sources:

- https://github.com/makehumancommunity/makehuman/blob/a8bc2d54ff0ac92e78ff71431b1023eda42bf482/makehuman/data/3dobjs/base.obj
- https://github.com/makehumancommunity/mpfb2/tree/afb9f530a7c2741dedb8df0ebae2e0b183caec21/src/mpfb/data
- https://static.makehumancommunity.org/assets/assetpacks/makehuman_system_assets.html
- System pack: https://files.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip (Last-Modified: 2024-04-14; ETag 10bbb7ea-6160e7c0d7996)

Copied graphical data in `scripts/vendor/makehuman/`: hm08 `base.obj`, adult shape targets, default skin weights, and `young_darkskinned_male_diffuse.png` with its material metadata. The core material explicitly states its CC0 release. Original copyright holders: Data Collection AB, Joel Palmius and Jonas Hauquier. Full upstream license notices are retained alongside these assets.

https://static.makehumancommunity.org/about/license.html confirms the separate CC0 graphical-asset licensing. MakeHuman application code is AGPL and MPFB application code is GPL; no application code from either project is copied or executed here. The Med Quest adaptation and export scripts are authored for this game.

Adaptations: Black adult volunteer using the CC0 African adult shape target and natural dark skin albedo, scaled to 1.75 m, weighted arm/leg posing into the exhibit stance, subdivided surface, fitted opaque teal shorts, modeled eyes/scalp, embedded skin albedo, generated pore normal and roughness maps, chest-only breathing morph, Meshopt compression. The educational internal anatomy remains simplified and is not a clinical atlas.

## Rebuild

Run the installed Blender in background mode with `--python scripts/build_anatomy.py`, then `node scripts/optimize-anatomy.mjs`, `npm test`, and `npm run build`. The editable, texture-packed Blender file is `docs/MQ-human-anatomy.blend`. Neither rebuilding nor running the game requires contacting MakeHuman.

## Generated museum artwork

The home hero and ten system lesson images were generated for Med Quest using the built-in image generation tool. Exact prompts and output filenames are recorded in ART-PROMPTS.json. They are illustrative educational simplifications, not clinical reference photographs. WebP conversion changes only resolution/compression. No competitor artwork or logos were used.

## Browser runtime libraries

Three.js is MIT-licensed by the three.js authors. The Meshopt decoder is MIT-licensed by Arseny Kapoulkine. Full notices ship with the production site at `assets/licenses/THREE-LICENSE.txt` and `assets/licenses/MESHOPTIMIZER-LICENSE.txt`. The locked npm dependencies retain their own license files for source development.

The lab motion update retains native CC0 MakeHuman joint influences in the skin mesh as `_MQ_ARM_WEIGHTS`. The runtime applies elbow and shoulder movement to the surface and a matching body-space pose to the internal layers and circulation demonstration.
