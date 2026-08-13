# Fullscreen Map Overlay (for EQL)

Makes the **native EQL map** a **fullscreen, see-through overlay** - like the RueUI fullscreen
maps - using EQ's own UI files. No add-ons, no external programs. Live position, zoom and
panning all work as normal because it's still the native map.

This is the **only** map-window tweak in this pack, because EQL's map already does the rest:

> **You do NOT need a "dark background" or "minimap" file.** EQL's native map already has them.
> Right-click the map -> **Display Types** and pick e.g. *Dark Background*, *No Background*
> (transparent), or the *Compact* / *Minimal* (minimap) layouts. Right-click -> **Window ->
> Lock** to lock it in place.

## Install

Easiest: run **`Install.bat`** in the repo root, choose **Install**, and pick the **Overlay**
UI mode (and a skin, or ALL skins).

Manual: copy `Overlay\EQUI_MapViewWnd.xml` into your active `uifiles\<skin>` folder (back up
the existing one first), then `/loadskin <skin>` (or relog).

Use it with the **`Spiken's Maps - Light`** pack - over a see-through/dark map, light lines
show up; dark lines don't.

## Using it

The overlay is a big, see-through map that sits in the **lower-right corner** of your screen.
To hide the controls, **minimize the little "Map" window** - the overlay map stays up.

## Resolution (auto)

The installer sizes the overlay to **200% of your EQ resolution**, read from `eqclient.ini`
(fullscreen `Width/Height` or windowed `WindowedWidth/Height`). EQL positions the map's centre
relative to the render area, so a 2x render area lands the visible map in the lower-right
corner, on-screen - and it scales to **1080p, 1440p, 4K and ultrawide**. If you install
manually, edit the `MVW_MapRenderArea` block's `<CX>`/`<CY>` to twice your screen size.

## Undo

Run the installer again and choose **Revert** (restores your skin's original map), or delete
the `EQUI_MapViewWnd.xml` you copied in / restore the `.bak`.
