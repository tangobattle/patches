# Tango patch repository

This is the repository Tango loads patches from.

Each patch version is a single `.tangopatch` file — a package holding
its metadata, its patches, its save templates and its README. Tango
downloads one only when it needs it: you install it, someone you're
about to play uses it, or a replay was recorded with it. Nobody
downloads the whole repository.

## Submitting a patch

Build a package with the `tango-patch` tool and commit it to a
directory named after your patch:

```
bn6_allstars/
├── bn6_allstars-1.0.0.tangopatch
└── bn6_allstars-1.1.0.tangopatch
```

Installing the tool:

```sh
cargo install --git https://github.com/tangobattle/tango-patch --features cli
```

### Building your package

Lay out a directory like this and run `tango-patch pack`:

```
my-patch/
├── manifest.toml
├── README.md                 # optional, shown in Tango
├── roms/BR6E_00.bps          # at least one required
├── roms/BR5E_00.bps
├── saves/BR6E_00.sav         # optional, a starting save
└── saves/BR6E_00.gregar.sav  # optional, a named one
```

```sh
tango-patch pack my-patch/ -o bn6_allstars/
```

The output is named `<name>-<version>.tangopatch` from the manifest, so
you don't choose the filename. `tango-patch validate` checks a package
(or a source directory) without building anything, and `tango-patch
info` prints what a package contains.

Packing is deterministic: the same inputs always produce byte-identical
output, so rebuilding a package you didn't change produces no diff.

### `roms/`

One BPS patch per ROM you support, named `<GAMECODE>_<REVISION>.bps`.
For Mega Man Battle Network 6: Cybeast Falzar that's `BR6E_00.bps` —
`BR6E` is the game code and `00` is the revision (usually `00`).

Which games your patch supports is read from these files. Nothing in
`manifest.toml` names a game, so the two can't disagree.

### `saves/`

Optional starting saves, offered in Tango when creating a new save.
`BR6E_00.sav` is the default one; `BR6E_00.<name>.sav` is a named one
(`<name>` may use letters, digits, `_` and `-`). A save template needs
a matching `roms/` entry.

### `manifest.toml`

```toml
format = 1
name = "bn6_allstars"
version = "1.1.0"
title = "BN6 All-Stars + BBN6"
authors = ["Your Name <your@email.address>"]
license = "MIT"
source = "https://github.com/luckytyphlosion/bn6-all-stars"
netplay = "group:bn6allstars"
```

- **`name`** — the directory name, unique in this repository. Letters,
  digits, `_` and `-`, starting with a letter or digit.
- **`version`** — [semver](https://semver.org/), without a `v` prefix.
- **`title`** — what Tango shows in its patch list.
- **`authors`** — optional, `Your Name <your@email.address>`.
- **`license`** — optional [SPDX identifier](https://spdx.dev/licenses/).
  Absent means `UNLICENSED`.
- **`source`** — optional URL to the patch's source.
- **`netplay`** — see below. Absent means `"isolated"`.

An unrecognized key is an error rather than something quietly ignored,
so a typo can't leave your patch subtly misconfigured.

#### `netplay`

Who this version of your patch can play against. Exactly one of:

| value | meaning |
|---|---|
| `"isolated"` | only the identical patch at the identical version (the default) |
| `"vanilla"` | the unpatched game, and any other `vanilla` patch for it |
| `"group:NAME"` | anything else declaring the same group |

**`"isolated"`** is the default because it's the safe one: two players
running gameplay code that differs at all will desync, and failing to
match is much better than desyncing mid-match. If your patch changes
anything about how the game plays, leave it alone.

**`"vanilla"`** is for patches that change *nothing* about gameplay —
translations, music, cosmetics. Someone using it can play someone with
no patch at all.

**`"group:NAME"`** is how you opt into playing something else: pick a
name and share it. Use it to let versions of your patch play each other
(don't change the group when you release a version that stays
compatible with the last), or to keep separate patches — a JP and an EN
release of the same mod, say — in lockstep. Group names use the same
characters as patch names.

You never write a game or family name here. Compatibility is scoped to
the ROM being played automatically, so a group called `bn6` is not the
same as `"vanilla"` on BN6, and a package that patches both BN4 and BN6
ROMs can't accidentally match a BN4 player against a BN6 one.

#### `[rom_overrides]`

Optional, for translation patches: replacement text the patched ROM
can't supply itself.

```toml
[rom_overrides]
language = "en-US"
charset = [" ", "0", "1", "..."]
chips = [{ name = "Cannon", description = "Fires a shot." }]
navicust_parts = [{ name = "HP+100" }]
styles = [{ name = "Normal" }]
patch_card56s = [{ name = "..." }]
patch_card56_effects = [{ name_template = [{ t = "Attack +" }, { p = 1 }] }]
```

Each list is indexed by in-game id, so entry 0 overrides id 0. `p = 1`
in an effect template inserts that effect's parameter.

## Releasing a new version

Build a new package and commit it alongside the old ones. Don't touch
the ones already there.

**Once a patch version is published, it may not be deleted** unless it
contains sensitive information — replays record the patch they were
recorded with, and Tango downloads that exact version to play them
back. A version you delete is a replay nobody can watch again.

## What CI does

On push to `main`, GitHub Actions validates every package, generates
`index.json` and the README sidecars from them, and publishes the
directory to GitHub Pages. Those generated files aren't committed —
that's what keeps two patch submissions from conflicting with each
other.

`index.json` is the only file Tango polls. It lists every package with
its size, hash and netplay compatibility, so the app can show you the
whole repository, and check whether you can play someone, without
downloading any patches.
