<div align="center">

# Volumetric Wing Vapor

An add-on for [KSP Wingtip Vortex](https://github.com/PogKai/ksp-wingtip-vortex): its wing vapor, drawn as a soft volumetric cloud.

<br>

[![Release](https://img.shields.io/github/v/release/PogKai/ksp-volumetric-wing-vapor?style=flat-square&label=release&color=2b7bb9)](https://github.com/PogKai/ksp-volumetric-wing-vapor/releases/latest)
[![KSP](https://img.shields.io/badge/KSP-1.12.x-4c9a4c?style=flat-square)](#install)
[![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey?style=flat-square)](license.md)

**[Download](https://github.com/PogKai/ksp-volumetric-wing-vapor/releases/latest)**
&nbsp;·&nbsp; [Wingtip Vortex](https://github.com/PogKai/ksp-wingtip-vortex)
&nbsp;·&nbsp; [Changelog](CHANGELOG.md)

</div>

<br>

## What it does

Wingtip Vortex works out where the air over the wings condenses and draws it as particle puffs. With this add-on installed, that same vapor is drawn as one soft cloud over each wing, using [Waterfall](https://github.com/post-kerbin-mining-corporation/Waterfall)'s volumetric shader.

| | |
|---|---|
| **One cloud per wing** | Fitted to the vapor each frame: it starts along the wing's leading edge and takes the wing's sweep and taper |
| **Joined over the fuselage** | When both wings are condensing, the two clouds meet in one |
| **Same vapor** | When and where it forms is still Wingtip Vortex's doing. This mod only changes how it is drawn |

<br>

## Install

1. Install [Wingtip Vortex](https://github.com/PogKai/ksp-wingtip-vortex/releases/latest) 1.5.0 or later, and [Waterfall](https://github.com/post-kerbin-mining-corporation/Waterfall)
2. Download the zip from the [latest release](https://github.com/PogKai/ksp-volumetric-wing-vapor/releases/latest)
3. Copy the `VolumetricWingVapor` folder (inside the zip's `GameData`) into your KSP `GameData/`
4. Fly

KSP 1.12.x · needs Wingtip Vortex and Waterfall · to upgrade, replace the folder · to remove, delete it.

<br>

## Settings

Wingtip Vortex's settings window (the vortex button on the app launcher, or **Alt+V**) gains two rows under the wing vapor's when this add-on is installed:

* **Volumetric cloud (Waterfall)**: switch it off to go back to the puffs, and on again for the cloud
* **Thickness**: how far the cloud stands off the wing, 0 to 200%

The wing vapor's own switch and intensity apply to the cloud too. The two settings are saved to `PluginData/settings.cfg` in this mod's folder.

<br>

## Good to know

* **Without Wingtip Vortex**, KSP does not load this mod
* **Without Waterfall**, the vapor stays as Wingtip Vortex's puffs, and the settings window says so. Developed against Waterfall 0.10.5
* The shader adds light, so the cloud reads best against sky and can look like a glow against dark terrain
* It covers the main wings only, not a strake or canard ahead of them or a tail well behind
* Like the puffs, it is drawn on the craft you fly only

<br>

## Learn more

| | |
|---|---|
| [How it works](docs/how-it-works.md) | How the cloud is fitted to the vapor |
| [Wing vapor](https://github.com/PogKai/ksp-wingtip-vortex/blob/main/docs/wing-vapor.md) | Wingtip Vortex's notes on when vapor forms, and its limits |
| [Changelog](CHANGELOG.md) | Every release |

<br>

## Source and building

The source is in [`Source/`](Source), and every release zip carries a copy of it next to the DLL.

`VolumetricWingVapor.csproj` reads two paths from a `local.props` file next to it, which is not tracked:

```xml
<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <KSPDIR>C:\path\to\Kerbal Space Program</KSPDIR>
    <VortexDll>C:\path\to\WingtipVortex.dll</VortexDll>
  </PropertyGroup>
</Project>
```

`python tools/package.py` builds the DLL and writes the release zip to `dist/`.

<br>

## License

[CC BY-NC-SA 4.0](license.md): free to use and share, never to sell. You can:

| | |
|---|---|
| **Use it** | In your own game, videos, streams and screenshots |
| **Change it** | Fork it, modify it, fix it, build on it |
| **Share it** | Redistribute it, or bundle it in a free modpack |
| **Reuse the code** | Put any part of it in your own free mods and projects |

As long as you:

* **Credit PogKai** and link back to this repository
* **Don't sell it**, or anything built from it, or put it behind a paywall
* **Use the same license** for anything you share that's built from it

Waterfall is not included. Its shader, model and texture are loaded from your own Waterfall install.

<br>

## Free, always

Every version of this mod is free. I have never charged for it and never will. If you paid for it anywhere, that money didn't go to me. Get it from the [official releases](https://github.com/PogKai/ksp-volumetric-wing-vapor/releases).

<br>

## AI disclosure

This mod was built with help from Claude, Anthropic's AI assistant.

| | |
|---|---|
| **With Claude** | Research support, baseline code, and debugging |
| **Me (PogKai)** | The ideas and the direction of the project, my own research, core integration into KSP, and all in-game testing |

<br>

<div align="center">

CC BY-NC-SA 4.0 · by PogKai

</div>
