![](./screenshot.png)
![](./screenshot2.png)

This is an **experimental** fork of @ravignir's 5Hex tileset.

This adds:
- Terrain blending.
- Unit and terrain feature shadows.
- An automatic build system for adding such features onto the existing tileset images.

All the tile and unit art is by @ravignir, licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License!

---

To incorporate the effects and build system into your own tileset:
- Add the `BuildTileset.sh` and `TileTransformer.py` script files to your tileset.
- Move your mod's tileset directory into `src/`.
- Edit the locations, string, and parameters in `BuildTileset.sh` to fit your tileset.
- Run `./BuildTileset.sh`. It will copy the original files from `src/` to `Images/TileSets/`, and apply margins, blending, and shadows onto the copies according to its configuration.
- Set `tileScale` in your tileset's configuration JSON to the expansion/margin factor you used in `BuildTileset.sh`.

Back up your files before doing this!

---

See:
- https://github.com/ravignir/5Hex-Tileset for the 5Hex tileset.
- https://github.com/yairm210/Unciv/pull/5874 for game code support.
- https://github.com/will-ca/Bubbly-Borders-Example if you just want the smooth borders.
