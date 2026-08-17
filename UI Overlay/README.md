# See-through Map Overlay (for EQL)

Turns the **native EQL map** into a big **transparent map that sits in the lower-right of your
screen** while you play — using EQ's own UI file (`Overlay\EQUI_MapViewWnd.xml`). No add-ons, no
external programs; live position, zoom and panning all work because it's still the native map.

> You do **not** need a separate "dark background" or "minimap" file — EQL's native map already
> has those (right-click the map → **Display Types**). This overlay is the one extra piece.

## How it works (read this)

- The overlay resizes the map's render area to **200% of your screen resolution**. That oversized,
  transparent render area is the **see-through map you see in the lower-right corner**. It's
  anchored to the screen (that's what fills the corner), so you don't drag the overlay itself.
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

## Resolution — set `<CX>`/`<CY>` to 2× your screen

The installer reads your resolution from `eqclient.ini` and sets this automatically. Installing
by hand, edit the `MVW_MapRenderArea` block's `<CX>`/`<CY>` to **twice** your game resolution:

| Game resolution | Overlay `<CX>` × `<CY>` (2×) |
|---|---|
| 1920 × 1080 | 3840 × 2160 |
| 2560 × 1440 | 5120 × 2880 |
| 3440 × 1440 (21:9 ultrawide) | 6880 × 2880 |
| 3840 × 2160 (4K) | 7680 × 4320 |
| 5120 × 1440 (32:9 super-ultrawide) | 10240 × 2880 |

## Undo

Run the installer and choose **Revert**, or delete the copied `EQUI_MapViewWnd.xml` and rename
`EQUI_MapViewWnd.xml.bak` back to `EQUI_MapViewWnd.xml`.
