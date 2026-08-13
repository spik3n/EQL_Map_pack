# Spiken's EQL Map Pack

In-game map packs for **EverQuest: Legends (EQL)**, in three styles, plus an optional
see-through overlay UI and a one-click installer.

Every pack is **updated for EQL**: the geometry matches the current EQL client, and the
~20 custom / instanced Legends zones the community packs never had (e.g. `lakenerius`,
`arena2`, the Plane-of-Hate revamp interiors) are included.

> **Quick install:** download a release, run **`Install.bat`**, pick a pack + (optional)
> UI mode, and point it at your EQL folder. Details below.

---

## The packs at a glance

| Pack | Style | POIs |
|------|-------|------|
| **Spiken's Maps** | Clean geometry, our own style | Zone lines, landmarks, vendors **+ named / rare / boss spawn markers** |
| **Spiken's Maps - Light** | Same, light-gray lines | Same as above (for dark-background / overlay use) |
| **Spiken's Brewall** | Brewall's look | Brewall's original POIs |
| **Spiken's Good's Maps** | Good's look | Good's original POIs |

Pick whichever you like — they install side by side, and you switch between them from the
map window's **top-left dropdown** in game.

---

## Spiken's Maps

Our own pack. Clean, EQL-accurate line work (see Credits) with a rich, colour-coded points
-of-interest layer built specifically for EQL.

![Spiken's Maps](Screenshots/spikens.png)

**What's on it**

- **Zone connections** — every `to <zone>` line, in **purple**
- **Vendors / NPCs** — merchants, bankers, bartenders, etc., in **black**
- **Landmarks** — spires, druid rings, tradeskill spots, etc., in **white**
- **Spawn markers** for the mobs you actually care about:

| Colour | Meaning |
|--------|---------|
| 🔴 **Red** | Raid bosses |
| 🟠 **Orange** | Epic 1.0 quest mobs |
| 🟡 **Yellow** | Named / rare spawns |
| 🔵 **Cyan** | GuildMasters / class trainers |

**How the spawn data is sourced** — spawn locations come from **EQEMU** POI data (the open
EverQuest emulator database), which EQL's classic-era content closely matches. Only genuine
named/rare/boss spawns are shown (generic trash and static guards/summoned NPCs are filtered
out), one marker per mob, and overlapping labels at a shared camp are spread apart so they
stay readable.

For the **custom EQL zones** that don't exist on classic databases (e.g. New Sebilis Expedition)
and for **GuildMaster / class-trainer** locations, POIs are sourced from the community-run
[EverQuest Legends Wiki](https://eqlwiki.com/).

![New Sebilis Expedition — GuildMasters, boss and merchants](Screenshots/spikens_newsibilisexpedition.png)

*New Sebilis Expedition: GuildMasters (cyan), the boss (red) and class spell/tradeskill merchants (black), placed from the EQL Wiki.*

### Spiken's Maps - Light

Identical to Spiken's Maps but with **light-gray lines** instead of dark, so they show up
over a **dark background** or a **transparent overlay**. Use this variant with any of the
dark/overlay UI modes below.

![Spiken's Maps - Light](Screenshots/spikens_light.png)

The Light pack carries the **same POIs** as the standard pack — here's New Sebilis Expedition
in light style (GuildMasters, boss and merchants all present):

![New Sebilis Expedition — Light](Screenshots/spikens_newsibilisexpedition_light.png)

---

## Spiken's Brewall

Brewall's map set, updated for EQL and with the missing custom Legends zones filled in.
Brewall's own colour scheme and POI layers are preserved.

![Spiken's Brewall](Screenshots/Brewall.png)

---

## Spiken's Good's Maps

Good's map set, updated for EQL and with the missing custom Legends zones filled in. Good's
own labelling and colours are preserved.

![Spiken's Good's Maps](Screenshots/goods.png)

---

## Fullscreen overlay (optional)

EQL's **native map already has dark / transparent backgrounds and compact "minimap"
layouts** built in - just right-click the map → **Display Types** (and **Window → Lock** to
lock it). So the only extra piece here is a **fullscreen, see-through overlay** (RueUI-style),
in `UI Overlay\Overlay\` - it makes the native map fill the screen so you can play with the
map over the world.

- Install it via **`Install.bat`** (pick the **Overlay** UI mode), or copy
  `UI Overlay\Overlay\EQUI_MapViewWnd.xml` into your `uifiles\<skin>` folder.
- Use it with **Spiken's Maps - Light** (light lines show over the world).
- The map sits **see-through in the lower-right corner**; **minimize** the little "Map" window to hide the controls (the map stays).
- The installer **sizes it to 200% of your screen** (reads `eqclient.ini` — fits 1080p / 1440p / 4K / ultrawide).
- Undo any time with the installer's **Revert** option.

[![Spiken's Overlay](Screenshots/spikens_overlay.gif)](Screenshots/spikens_overlay_full.gif)

*(click the gif for a larger version)*

---

## Install

### Easy way (installer)

1. Download and extract a release.
2. Run **`Install.bat`**.
3. Choose **Install**, pick a map pack (or ALL), then optionally a UI mode.
4. Browse to your EverQuest Legends folder (the one with `eqgame.exe`).

Packs install to `EverQuest Legends\maps\<pack>\` (your existing maps are untouched — pick
the pack from the in-game map dropdown). A UI mode installs into a skin you choose (or **ALL
skins**), backing up the skin's original map first.

To undo a UI mode later, run the installer again and choose **Revert**.

### Manual way

- **Maps:** copy a pack folder (or just its `.txt` files) into `EverQuest Legends\maps`.
- **UI mode:** copy `UI Overlay\<mode>\EQUI_MapViewWnd.xml` into your active
  `uifiles\<skin>` folder, then `/loadskin <skin>` (or relog).

> **Patch days:** EQL's patcher rewrites the `maps` folder on patch days (not every launch).
> After an EQL patch, re-run the installer to restore your maps.

---

## Credits

- **Brewall's Maps** — basis for *Spiken's Brewall*. Original maps & POIs by Brewall. <https://www.eqmaps.info/>
- **Good's Maps** — basis for *Spiken's Good's Maps*, and the clean geometry used by *Spiken's Maps*. Original maps & POIs by Goodurden. <https://www.eqmaps.info/good-eq-maps/>
- **EQEMU** — spawn-location / POI data used for Spiken's Maps' named/rare/boss markers. <https://www.eqemu.org/>
- **EverQuest Legends Wiki** — POIs for custom EQL zones (e.g. New Sebilis Expedition) and GuildMaster / class-trainer locations. <https://eqlwiki.com/>
- EQL zone geometry generation, POI layer & packaging by **Spiken**.

All credit for the original cartography goes to Brewall and Goodurden; these packs
redistribute their work updated for EverQuest: Legends.
