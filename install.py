"""
Spiken's EQL Map Pack - installer.

Pick a map pack and (optionally) a map-window UI mode, browse to your EverQuest
Legends folder, and everything is copied in ready to use.

  - Map packs install as subfolders of \\maps (pick them from the map's top-left
    dropdown in game). Your existing maps are untouched.
  - A UI mode installs a modified EQUI_MapViewWnd.xml into a skin you choose
    (the existing one is backed up first).
"""
import os
import re
import sys
import glob
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

PACKS = [
    ("Spiken's Maps",           "Spiken's own - clean geometry + named/rare/boss markers"),
    ("Spiken's Maps - Light",   "Same as above, light lines - for the Spiken Overlay UI or EQL's dark/no background"),
    ("Spiken's Brewall",        "Brewall style, updated for EQL"),
    ("Spiken's Good's Maps",    "Good's style, updated for EQL"),
]

def prompt(title, options, allow_all=False):
    print("\n" + title)
    for i, (_, label) in enumerate(options, 1):
        print(f"  {i}. {label}")
    if allow_all:
        print(f"  {len(options) + 1}. ALL of the above")
    while True:
        pick = input(f"Choose [1-{len(options) + (1 if allow_all else 0)}]: ").strip()
        if pick.isdigit():
            n = int(pick)
            if 1 <= n <= len(options):
                return [options[n - 1][0]]
            if allow_all and n == len(options) + 1:
                return [o[0] for o in options]
        print("Please enter a number from the list.")


def browse_folder():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        path = filedialog.askdirectory(title="Select your EverQuest Legends folder (has eqgame.exe)")
        root.destroy()
        if path:
            return path
    except Exception:
        pass
    return input("Paste the path to your EverQuest Legends folder: ").strip('" ')


def resolve_root(folder):
    folder = os.path.abspath(folder)
    if os.path.basename(folder).lower() in ("maps", "uifiles"):
        folder = os.path.dirname(folder)
    if not os.path.isfile(os.path.join(folder, "eqgame.exe")):
        print(f"  ! Warning: no eqgame.exe in {folder} - continuing anyway.")
    return folder


def choose_skin(root):
    uidir = os.path.join(root, "uifiles")
    skins = [os.path.basename(d) for d in glob.glob(os.path.join(uidir, "*")) if os.path.isdir(d)]
    # put likely-custom skins first
    skins.sort(key=lambda s: (s.startswith("default"), s.lower()))
    print("\nWhich UI skin do you use? (the map UI file goes here)")
    for i, s in enumerate(skins, 1):
        print(f"  {i}. {s}")
    all_opt = len(skins) + 1
    print(f"  {all_opt}. ALL skins (install into every skin, so it works whichever you load)")
    while True:
        pick = input(f"Choose [1-{all_opt}]: ").strip()
        if pick.isdigit():
            n = int(pick)
            if 1 <= n <= len(skins):
                return [skins[n - 1]]
            if n == all_opt:
                return skins
        print("Please enter a number from the list.")


def eq_resolution(root):
    """Read EQL's actual render size from eqclient.ini so the overlay fits any screen
    (1080p / 1440p / 4K / ultrawide). Uses the fullscreen or windowed size depending on
    which mode the client is set to. Returns (w, h) or None."""
    vals = {}
    try:
        with open(os.path.join(root, "eqclient.ini"), encoding="latin-1", errors="ignore") as f:
            for line in f:
                if "=" in line:
                    k, _, v = line.partition("=")
                    vals[k.strip().lower()] = v.strip()
    except OSError:
        return None

    def geti(key):
        try:
            return int(vals.get(key, ""))
        except ValueError:
            return None

    # Use the LARGER of windowed / fullscreen so a stale small windowed value can't shrink
    # the overlay (AutoStretch adapts to the real window regardless).
    ww, wh = geti("windowedwidth") or 0, geti("windowedheight") or 0
    fw, fh = geti("width") or 0, geti("height") or 0
    w, h = max(ww, fw), max(wh, fh)
    return (w, h) if (w > 0 and h > 0) else None


def _fit_overlay(content, size):
    """Size the screen-anchored render area to 1x the screen. With AutoStretch=true the map
    stays centered and works at every zoom level, and adapts to any window size."""
    if not size:
        return content
    w, h = int(size[0]), int(size[1])

    def repl(m):
        b = re.sub(r"(<CX>)\d+(</CX>)", rf"\g<1>{w}\g<2>", m.group(0))
        b = re.sub(r"(<CY>)\d+(</CY>)", rf"\g<1>{h}\g<2>", b)
        return b

    return re.sub(r'<Screen item="MVW_MapRenderArea">.*?</Screen>', repl, content, count=1, flags=re.S)


def apply_ui(root, ui, skins, size=None):
    src_xml = os.path.join(HERE, "UI Overlay", ui, "EQUI_MapViewWnd.xml")
    content = open(src_xml, encoding="latin-1").read()
    if ui == "Overlay":
        content = _fit_overlay(content, size)
    for skin in skins:
        dst_xml = os.path.join(root, "uifiles", skin, "EQUI_MapViewWnd.xml")
        # back up the skin's ORIGINAL map file once, so 'revert' can restore it
        if os.path.isfile(dst_xml) and not os.path.isfile(dst_xml + ".bak"):
            shutil.copy2(dst_xml, dst_xml + ".bak")
        with open(dst_xml, "w", encoding="latin-1") as f:
            f.write(content)
        print(f"  + UI '{ui}' -> uifiles\\{skin}")


def make_modified_skin(root, base, new_name):
    """Make (or REUSE) a patch-safe classic-UI copy of default / default_modern under a custom name
    LaunchPad won't overwrite. If the skin already exists it is LEFT IN PLACE and the caller just
    applies the overlay into it - so a skin already carrying the Sparxx ring (or anything else)
    keeps it. Only a brand-new skin is copied from the base and Gameface-stripped so the classic
    map + overlay render. To pull in a game patch's UI, delete the skin folder and re-run.
    Returns new_name, or None if the base skin is missing."""
    uidir = os.path.join(root, "uifiles")
    src = os.path.join(uidir, base)
    dst = os.path.join(uidir, new_name)
    if os.path.isdir(dst):
        print(f"  '{new_name}' already exists - adding to it (keeping any other changes).")
        return new_name
    if not os.path.isdir(src):
        print(f"  ! '{base}' skin not found - can't create '{new_name}'.")
        return None
    print(f"  Copying '{base}' -> '{new_name}' (patch-safe classic-UI skin)...")
    shutil.copytree(src, dst)
    stripped = glob.glob(os.path.join(dst, "EQLSUI*.xml"))
    for f in stripped:
        os.remove(f)
    if stripped:
        print(f"    stripped {len(stripped)} Gameface (EQLSUI) files -> classic UI, so the overlay renders.")
    return new_name


def revert_ui(root, skins):
    default_xml = os.path.join(root, "uifiles", "default", "EQUI_MapViewWnd.xml")
    for skin in skins:
        dst_xml = os.path.join(root, "uifiles", skin, "EQUI_MapViewWnd.xml")
        bak = dst_xml + ".bak"
        if os.path.isfile(bak):
            shutil.copy2(bak, dst_xml)
            os.remove(bak)
            print(f"  ~ {skin}: restored the skin's original map (from backup)")
        elif skin != "default" and os.path.isfile(default_xml):
            shutil.copy2(default_xml, dst_xml)
            print(f"  ~ {skin}: no backup found - restored the game-default map")
        else:
            print(f"  ~ {skin}: nothing to revert")


def main():
    print(__doc__)
    root = resolve_root(browse_folder())

    action = prompt("What do you want to do?", [
        ("install", "Install a map pack and/or a map-window UI mode"),
        ("revert",  "Revert the map window to default (undo Dark / Overlay / Minimap)"),
    ])[0]

    if action == "revert":
        print("\nReverting removes the Dark / Overlay / Minimap map window and restores the")
        print("skin's original map (or the game default if there's no backup).")
        skins = choose_skin(root)
        revert_ui(root, skins)
        print("\nDone. In game: /loadskin <yourskin> (or relog) to apply.")
        return

    maps_dir = os.path.join(root, "maps")
    os.makedirs(maps_dir, exist_ok=True)

    packs = prompt("Which map pack(s)?", PACKS, allow_all=True)
    if len(packs) > 1:
        print("\n  Note: ALL packs install side by side; pick which to view from the map's")
        print("  top-left dropdown in game.")

    # copy packs
    for p in packs:
        src = os.path.join(HERE, p)
        if not os.path.isdir(src):
            print(f"  ! Missing pack folder: {p} - skipped."); continue
        dst = os.path.join(maps_dir, p)
        os.makedirs(dst, exist_ok=True)
        n = 0
        for f in glob.glob(os.path.join(src, "*.txt")):
            shutil.copy2(f, dst); n += 1
        print(f"  + {p}: {n} maps -> maps\\{p}")

    def show_overlay_size(size):
        if size:
            print(f"\n    Detected your EQ resolution: {size[0]}x{size[1]} - sizing the overlay to match")
            print("    (centered see-through map, works at every zoom).")
        else:
            print("\n    (Couldn't read eqclient.ini - overlay stays at its default size; edit <CX>/<CY>.)")

    ui_choice = prompt("Install the see-through overlay?", [
        ("patchsafe", "Patch-safe 'Modified' skin(s) - RECOMMENDED (survives LaunchPad patches, overlay works)"),
        ("existing",  "Overlay into an existing skin (e.g. a Sparxx classic skin)"),
        ("none",      "No thanks - maps only"),
    ])[0]

    if ui_choice == "patchsafe":
        print("\n  Patch-safe skins are classic-UI copies of your default / default_modern skin under a")
        print("  custom name LaunchPad won't overwrite. The Gameface web-UI layer is stripped so the")
        print("  classic map + overlay render (like Sparxx), and it survives patches.")
        pair_map = {"default": "Modified_Default", "default_modern": "Modified_Modern"}
        bases = prompt("Which patch-safe skin(s)?", [
            ("default",        "Modified_Default  (from your 'default' skin)"),
            ("default_modern", "Modified_Modern   (from your 'default_modern' skin)"),
        ], allow_all=True)
        size = eq_resolution(root)
        show_overlay_size(size)
        print()
        made = []
        for base in bases:
            skin = make_modified_skin(root, base, pair_map[base])
            if skin:
                apply_ui(root, "Overlay", [skin], size=size)
                made.append(skin)
        if made:
            print("\n  Use the 'Spiken's Maps - Light' pack so lines show over the dark world.")
            for m in made:
                print(f'  Load the skin:  /loadskin {m}   (or relog)')

    elif ui_choice == "existing":
        print("\n  * The Overlay makes the native map a big, see-through map centered on screen,")
        print("    working at every zoom level. Minimize the little 'Map' window to hide the")
        print("    controls - the overlay map stays. Use the 'Spiken's Maps - Light' pack.")
        print("    - IMPORTANT: needs a CLASSIC-UI skin (e.g. a Sparxx skin); it will NOT show on")
        print("      EQL's Default/Modern (Gameface) UI - use option 1 for a patch-safe classic skin.")
        size = eq_resolution(root)
        show_overlay_size(size)
        skins = choose_skin(root)
        apply_ui(root, "Overlay", skins, size=size)
        print("    In game: /loadskin <yourskin> (or relog) to apply.")

    print("\nDone. In game, open the Map and pick your pack from the top-left dropdown.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
    input("\nPress Enter to close...")
