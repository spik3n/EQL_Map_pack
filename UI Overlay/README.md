# See-through Map Overlay (for EQL)

Turns the **native EQL map** into a big **transparent map centered on your screen** while you
play — using EQ's own UI file (`Overlay\EQUI_MapViewWnd.xml`). No add-ons, no external programs;
live position, zoom and panning all work because it's still the native map.

> You do **not** need a separate "dark background" or "minimap" file — EQL's native map already
> has those (right-click the map → **Display Types**). This overlay is the one extra piece.

> ⚠️ **Needs a classic-UI skin.** EQL's **Default / Modern** UI uses a web-based (Gameface) map this
> file can't control. The installer's **"Patch-safe Modified skin"** option handles this: it makes a
> classic-UI copy of your `default` / `default_modern` skin (**Modified Default / Modified Modern**)
> where the overlay works and which survives LaunchPad patches. A **Sparxx** classic skin also works.
> Either way it's **automatic**: once installed and `/loadskin`ed, the see-through map appears
> **centered on screen** by itself — there is **no "drag it out of the frame" gesture** (dragging
> the map body just pans it; only the small "Map" control window moves/minimizes).

## How it works (read this)

- The overlay sizes the map's render area to your **screen resolution** with auto-stretch on, so the
  transparent map is **centered on screen and works at every zoom level** (including full zoom-out).
  It's anchored to the screen, so you don't drag the overlay itself.
- The normal little **"Map" window** (search box, layer buttons, zoom, etc.) is still there and
  still works. You **move it by its title bar** and **minimize** it with the normal EQ window
  controls. **Minimizing the small Map window hides the controls but leaves the see-through
  overlay map up.** (That drag/minimize behavior is the EQL client's, not this file's.)
- Use it with the **`Spiken's Maps - Light`** pack — light lines show over the dark world; dark
  lines don't.

## Install

**Easiest:** run **`Install.bat`** in the repo root (no Python needed — it's PowerShell), choose
**Install**, answer *yes* to the overlay, and pick a skin (or ALL skins).

**Manual:**
1. In `EverQuest Legends\uifiles\<your skin>\`, back up `EQUI_MapViewWnd.xml` as
   `EQUI_MapViewWnd.xml.bak`.
2. Copy `Overlay\EQUI_MapViewWnd.xml` into that same `uifiles\<your skin>\` folder.
3. Set the render size (below), then `/loadskin <your skin>` (or relog).

## Resolution — set `<CX>`/`<CY>` to your screen size

The installer reads your resolution from `eqclient.ini` and sets this automatically. Installing by
hand, edit the `MVW_MapRenderArea` block's `<CX>`/`<CY>` to **your game resolution** (e.g. `3440` ×
`1440`) and leave `<AutoStretch>true</AutoStretch>` — it centers and adapts to your window from
there, so the exact number isn't critical.

## Undo

Run the installer and choose **Revert**, or delete the copied `EQUI_MapViewWnd.xml` and rename
`EQUI_MapViewWnd.xml.bak` back to `EQUI_MapViewWnd.xml`.
