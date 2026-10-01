# Changelog

All notable changes to Volumetric Wing Vapor.

---

## 1.0.0 — First release

Wingtip Vortex's wing vapor, drawn as a soft volumetric cloud with Waterfall's shader.

### Added

* **One cloud per wing, in place of the puffs.** The cloud is fitted to the vapor Wingtip Vortex
  computes each frame: its front lies along where the vapor starts, it takes the wing's sweep and
  taper, its top is rounded, and the two wings' clouds join over the fuselage.
* **Two settings in Wingtip Vortex's window**: the cloud's thickness, and a switch back to the
  puffs. Saved to `PluginData/settings.cfg` in this mod's folder.

### Requirements

* Wingtip Vortex 1.5.0 or later, and Waterfall (developed against 0.10.5).

### Known limitations

* The shader adds light, so the cloud reads best against sky.
* Main wings only: not a strake or canard ahead of them or a tail well behind.
