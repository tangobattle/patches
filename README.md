# tango patch repository

This is the repository from which Tango is able to load patches from.

## Submitting a patch

Each patch is placed in its own directory in this repository, with a uniquely identifying name for it. A patch must contain a valid `info.toml` file, as well as versioned patch files (`.bps` only).

### `info.toml`

`info.toml` contains metadata about your patch. You must have this file to identify your patch.

#### The `[patch]` section

The first (and only) section in `info.toml` is `[patch]`.

##### The `title` field

The human-readable title of your patch. This will be displayed to users in the UI.

##### The `authors` field

The list of authors for your patch, formatted as `Your Name <your@email.address>`.

##### The `source` field

The URL to the source of the patch.

##### The `license` field

The license for the patch as an [SPDX license identifier](https://spdx.dev/licenses/). If this is not present, the license is assumed to be `UNLICENSED`.

##### The `for_rom` field

The ROM that this patch applies to. Tango matches patches based on the ROM title, which usually looks something like `MEGAMAN6_FXXBR6E` (this is the ROM title AND the ROM ID).

#### The `[versions]` section

The versions section contains metadata for each version of your patch. The versions must follow [Semantic Versioning](https://semver.org/).

Tango interprets the version as follows:

-   A **major version change (X.y.z)** assumes everything has changed significantly. If a replay was created on an older major version of the patch, Tango will **refuse** playing it with the newer version.

-   A **minor version change (x.Y.z)** assumes the changes will not adversely impact save state loading: there may be transient issues with e.g. VRAM but they are cosmetic only. Tango will **avoid** playing replays created on older minor versions with newer minor versions, but this is not a hard requirement if Tango cannot find an exactly matching patch.

-   A **patch version change (x.y.Z)** assumes the changes will not impact save state loading at all, including VRAM. Tango will **prefer** playing replays created on older patch versions with newer patch versions.

Version sections are of the format `[versions.'x.y.z']` (note the single quotes!).

##### The `netplay_compatibility` field

A string which, if other patches also have set to the same value, allows netplay between them: e.g. all patches with a `netplay_compatibility` of `bn6` may netplay with each other.

### Your patch directory

You must place your patch in your directory versioned with [Semantic Versioning](https://semver.org/), prefixed with `v`. For example, if you are releasing version 1.0.1 of your patch, you must label the directory as `v1.0.1`. Within the directory, you must place patches for each ROM you support. For instance, if you intend to support Mega Man Battle Network 6: Cybeast Falzar, you must name the patch `MEGAMAN6_FXXBR6E_00.bps`: `MEGAMAN6_FXXBR6E` is the game ID and `00` is the revision (this is usually `00`).

You may also include a plaintext file named README that will be displayed in the patch information in the Tango launcher.

**Once a patch version is submitted, you may not delete it unless it contains sensitive information.** This is such to ensure replays on older versions may always be played.
