# Changelog

## v1.8

- **Modified skins rebuild from the current UI** — the installer's "Patch-safe Modified skin"
  option now **regenerates** Modified Default / Modified Modern from your live `default` /
  `default_modern` each run (it deletes the old copy first), so **re-running after a game patch
  picks up the new UI files**. They stay classic-style (Gameface stripped) so the overlay renders.

## v1.7

- **Overlay reworked — centered and works at every zoom.** The see-through overlay now sizes the
  map's render area to **1× your screen** (was 2×) with auto-stretch on, so the map renders
  **centered on screen and stays visible at every zoom level, including full zoom-out**. The old 2×
  version pushed the map into the lower-right and blanked out when zoomed all the way out. It also
  **adapts to any window size** and no longer slides around as you move.
- **Installer fixes** — the installer + Modified skins produce the new centered overlay, and
  resolution detection now uses the **larger of your windowed/fullscreen** size, so a stale
  windowed value in `eqclient.ini` can't mis-size it.

## v1.6

- **Patch-safe "Modified" skins** — the installer can now build **Modified Default** / **Modified
  Modern** skins: it copies your `default` / `default_modern` skin under a custom name LaunchPad
  won't overwrite, **strips EQL's Gameface web-UI layer** so the classic map + see-through overlay
  render (the same reason the overlay only worked on Sparxx), and applies the overlay. So the
  overlay now **survives patch day** instead of being wiped — just `/loadskin "Modified Default"`
  (or Modern) in game.
- **Why the overlay never showed on Default/Modern** — those skins carry the `EQLSUI*` Gameface
  files, which route the map through EQL's web UI that a classic `EQUI_MapViewWnd.xml` can't touch.
  Removing those files drops the skin to the classic map, exactly like Sparxx — now documented and
  automated.

## v1.5

- **Resized zones** — 18 of the offset zones EQL didn't just shift but *resized* (Nektulos,
  Freeport, North Karana, Oasis, Lavastorm and others), which a shift can't correct. Those
  now use **EQL's exact geometry**, so your player lands dead-on. Their POI markers ride along
  and can sit a touch off near a zone's edges, but the map itself is accurate.
- **Overlay docs** — clarified that the overlay appears **automatically** (there is no "drag it
  out of the frame" gesture — dragging the map just pans it) and that it needs a **classic-UI
  skin** (e.g. Sparxx); it does **not** work on EQL's Default/Modern web-based UI. The installer
  now says the same.

## v1.4

- **Fixed offset zones** — EQL re-coordinated about 20 zones (Nektulos Forest, Lavastorm,
  North Karana, Commons, Freeport and others), so the classic geometry these packs inherit
  was shifted from where the game plots your character — the map looked "offset" and your
  dot sat off the map. Each pack's map is now shifted onto **EQL's coordinates** (geometry
  and labels moved together, so each pack keeps its own style), and your player lands on the
  map. Applied to all four packs.

## v1.3

- **No-Python installer** — the installer is now a native **Windows PowerShell** script
  (`Install.ps1`, launched by `Install.bat`), so there's nothing extra to install. It still
  copies packs, detects your resolution, sizes the overlay, backs up your UI, and reverts.
  (`install.py` is kept for anyone who prefers Python, but it's no longer required.)
- **Docs** — added a full **manual-install** section (maps + overlay, no installer), documented
  exactly how the overlay behaves (the small Map window is what you drag/minimize; the
  see-through map is anchored to the lower-right), where it installs
  (`uifiles\<skin>\EQUI_MapViewWnd.xml`) and its `EQUI_MapViewWnd.xml.bak` backup, plus a
  resolution table including 21:9 and 32:9 ultrawide.

## v1.2

- **Added EQL's own map labels** — 760 labels across 81 zones (portals, zone-ins, points of
  interest, vendor / NPC names) that the classic community packs never included. They ride the
  toggleable label layer, so they show by default and hide with everything else via layer `1`.
  Especially handy in **Plane of Sky** (island portals + keys), **Plane of Knowledge**, and the
  cities.

## v1.1

- **Toggleable labels** — every zone's spawn labels (named / rare / boss / GuildMaster / NPC
  markers) are now on map **layer 1**, so you can hide them in one click when a zone is busy.
  In the map window: **Layers: Visible → `1`**. Zone lines, landmarks and the footer stay
  always-on. Great for camps like Rathe Mountains where the froglok names cover the map.
- **Fixed geometry for rebuilt zones** — EQL rebuilt some zones, so the classic layouts were
  wrong. Swapped in EQL's own geometry for **Arena**, **Plane of Sky** and **Plane of
  Knowledge** so the maps match what you see in game. (More may follow as they're spotted —
  report any that look wrong.)

## v1.0

- Initial release: **Spiken's Maps**, **Spiken's Maps - Light**, **Spiken's Brewall**,
  **Spiken's Good's Maps**.
- Colour-coded **named / rare / boss** spawn markers plus **GuildMaster / class-trainer**
  markers (data from EQEMU and the EverQuest Legends Wiki), including custom EQL zones such as
  New Sebilis Expedition.
- Fullscreen **see-through overlay** UI, auto-sized to your resolution.
- One-click **`Install.bat`** installer with pack selection and revert.
