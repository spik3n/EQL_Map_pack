<#
    Spiken's EQL Map Pack - installer (no Python required).

    Uses only Windows PowerShell (built into Windows 7+). Pick your map pack(s)
    and optionally the see-through overlay, point it at your EverQuest Legends
    folder, and everything is copied in ready to use. Your existing files are
    backed up (EQUI_MapViewWnd.xml.bak) so you can revert.

    Run it by double-clicking Install.bat, or:  right-click Install.ps1 > Run with PowerShell
#>

$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path

$Packs = @(
    @{ Name = "Spiken's Maps";         Desc = "Spiken's own - clean geometry + named / rare / boss + GuildMaster markers" }
    @{ Name = "Spiken's Maps - Light"; Desc = "Same, light-gray lines - for a dark background / the overlay" }
    @{ Name = "Spiken's Brewall";      Desc = "Brewall's style, updated for EQL" }
    @{ Name = "Spiken's Good's Maps";  Desc = "Good's style, updated for EQL" }
)

function Read-Menu {
    param([string]$Title, [string[]]$Options, [switch]$AllowAll)
    Write-Host ""
    Write-Host $Title -ForegroundColor Cyan
    for ($i = 0; $i -lt $Options.Count; $i++) { Write-Host ("  {0}. {1}" -f ($i + 1), $Options[$i]) }
    if ($AllowAll) { Write-Host ("  {0}. ALL of the above" -f ($Options.Count + 1)) }
    $max = $Options.Count + $(if ($AllowAll) { 1 } else { 0 })
    while ($true) {
        $pick = (Read-Host ("Choose [1-{0}]" -f $max)).Trim()
        $n = 0
        if ([int]::TryParse($pick, [ref]$n)) {
            if ($n -ge 1 -and $n -le $Options.Count) { return @($n - 1) }
            if ($AllowAll -and $n -eq ($Options.Count + 1)) { return @(0..($Options.Count - 1)) }
        }
        Write-Host "Please enter a number from the list." -ForegroundColor Yellow
    }
}

function Get-EqFolder {
    # Try a folder-picker dialog; fall back to typing the path.
    try {
        Add-Type -AssemblyName System.Windows.Forms
        $dlg = New-Object System.Windows.Forms.FolderBrowserDialog
        $dlg.Description = "Select your EverQuest Legends folder (the one with eqgame.exe)"
        if ($dlg.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) { return $dlg.SelectedPath }
    } catch { }
    return (Read-Host "Paste the path to your EverQuest Legends folder").Trim('"', ' ')
}

function Resolve-Root {
    param([string]$Folder)
    $Folder = [System.IO.Path]::GetFullPath($Folder)
    $leaf = (Split-Path $Folder -Leaf).ToLower()
    if ($leaf -eq 'maps' -or $leaf -eq 'uifiles') { $Folder = Split-Path $Folder -Parent }
    if (-not (Test-Path (Join-Path $Folder 'eqgame.exe'))) {
        Write-Host ("  ! Warning: no eqgame.exe in {0} - continuing anyway." -f $Folder) -ForegroundColor Yellow
    }
    return $Folder
}

function Get-EqResolution {
    # Read the client's render size from eqclient.ini: fullscreen Width/Height,
    # or windowed WindowedWidth/Height. Returns @(w,h) or $null.
    param([string]$Root)
    $ini = Join-Path $Root 'eqclient.ini'
    if (-not (Test-Path $ini)) { return $null }
    $v = @{}
    foreach ($line in Get-Content $ini) {
        if ($line -match '^\s*([^=;]+?)\s*=\s*(.*)$') { $v[$matches[1].Trim().ToLower()] = $matches[2].Trim() }
    }
    $windowed = @('0', 'false', 'no', '') -contains ("" + $v['fullscreen'])
    $w = 0; $h = 0
    if ($windowed) { [void][int]::TryParse($v['windowedwidth'], [ref]$w); [void][int]::TryParse($v['windowedheight'], [ref]$h) }
    if (-not ($w -gt 0 -and $h -gt 0)) { [void][int]::TryParse($v['width'], [ref]$w); [void][int]::TryParse($v['height'], [ref]$h) }
    if ($w -gt 0 -and $h -gt 0) { return @($w, $h) }
    return $null
}

function Choose-Skins {
    param([string]$Root)
    $uidir = Join-Path $Root 'uifiles'
    $skins = @(Get-ChildItem -Path $uidir -Directory -ErrorAction SilentlyContinue | ForEach-Object { $_.Name })
    $skins = @($skins | Sort-Object @{ Expression = { $_ -like 'default*' } }, @{ Expression = { $_ } })
    Write-Host ""
    Write-Host "Which UI skin do you use? (the overlay's map file goes here)" -ForegroundColor Cyan
    for ($i = 0; $i -lt $skins.Count; $i++) { Write-Host ("  {0}. {1}" -f ($i + 1), $skins[$i]) }
    $allOpt = $skins.Count + 1
    Write-Host ("  {0}. ALL skins (install into every skin)" -f $allOpt)
    while ($true) {
        $pick = (Read-Host ("Choose [1-{0}]" -f $allOpt)).Trim()
        $n = 0
        if ([int]::TryParse($pick, [ref]$n)) {
            if ($n -ge 1 -and $n -le $skins.Count) { return @($skins[$n - 1]) }
            if ($n -eq $allOpt) { return $skins }
        }
        Write-Host "Please enter a number from the list." -ForegroundColor Yellow
    }
}

$Latin1 = [System.Text.Encoding]::GetEncoding('iso-8859-1')

function Apply-Overlay {
    param([string]$Root, [string[]]$Skins, $Size)
    $src = Join-Path $Here 'UI Overlay\Overlay\EQUI_MapViewWnd.xml'
    $content = [System.IO.File]::ReadAllText($src, $Latin1)
    if ($Size) {
        $w = [int]$Size[0] * 2; $h = [int]$Size[1] * 2   # overlay = 200% of the screen (fills the lower-right)
        $content = [regex]::Replace($content, '(?s)(<Screen item="MVW_MapRenderArea">.*?<Size>\s*<CX>)\d+(</CX>\s*<CY>)\d+(</CY>)', ('${1}' + $w + '${2}' + $h + '${3}'))
    }
    foreach ($skin in $Skins) {
        $dst = Join-Path $Root ("uifiles\{0}\EQUI_MapViewWnd.xml" -f $skin)
        if ((Test-Path $dst) -and -not (Test-Path ($dst + '.bak'))) { Copy-Item $dst ($dst + '.bak') }
        [System.IO.File]::WriteAllText($dst, $content, $Latin1)
        Write-Host ("  + Overlay -> uifiles\{0}" -f $skin) -ForegroundColor Green
    }
}

function Revert-Ui {
    param([string]$Root, [string[]]$Skins)
    $default = Join-Path $Root 'uifiles\default\EQUI_MapViewWnd.xml'
    foreach ($skin in $Skins) {
        $dst = Join-Path $Root ("uifiles\{0}\EQUI_MapViewWnd.xml" -f $skin)
        $bak = $dst + '.bak'
        if (Test-Path $bak) {
            Copy-Item $bak $dst -Force; Remove-Item $bak -Force
            Write-Host ("  ~ {0}: restored the skin's original map (from backup)" -f $skin) -ForegroundColor Green
        } elseif ($skin -ne 'default' -and (Test-Path $default)) {
            Copy-Item $default $dst -Force
            Write-Host ("  ~ {0}: no backup - restored the game-default map" -f $skin) -ForegroundColor Green
        } else {
            Write-Host ("  ~ {0}: nothing to revert" -f $skin) -ForegroundColor Yellow
        }
    }
}

# ---- main ----
Write-Host "Spiken's EQL Map Pack installer (no Python needed)" -ForegroundColor Cyan
$root = Resolve-Root (Get-EqFolder)
Write-Host ("EverQuest Legends folder: {0}" -f $root)

$action = (Read-Menu "What do you want to do?" @(
        "Install a map pack and / or the see-through overlay",
        "Revert the map window to default (undo the overlay)"
    ))[0]

if ($action -eq 1) {
    $skins = Choose-Skins $root
    Revert-Ui $root $skins
    Write-Host ""
    Write-Host "Done. In game: /loadskin <yourskin> (or relog) to apply." -ForegroundColor Cyan
    Read-Host "Press Enter to close"
    return
}

$mapsDir = Join-Path $root 'maps'
New-Item -ItemType Directory -Force -Path $mapsDir | Out-Null

$sel = Read-Menu "Which map pack(s)?" ($Packs | ForEach-Object { "{0} - {1}" -f $_.Name, $_.Desc }) -AllowAll
if ($sel.Count -gt 1) {
    Write-Host ""
    Write-Host "  Note: ALL packs install side by side; pick which to view from the map's top-left dropdown in game."
}
foreach ($i in $sel) {
    $name = $Packs[$i].Name
    $srcDir = Join-Path $Here $name
    if (-not (Test-Path $srcDir)) { Write-Host ("  ! Missing pack folder: {0} - skipped." -f $name) -ForegroundColor Yellow; continue }
    $dstDir = Join-Path $mapsDir $name
    New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
    $n = 0
    Get-ChildItem (Join-Path $srcDir '*.txt') | ForEach-Object { Copy-Item $_.FullName $dstDir -Force; $n++ }
    Write-Host ("  + {0}: {1} maps -> maps\{0}" -f $name, $n) -ForegroundColor Green
}

Write-Host ""
$ans = (Read-Host "Also install the see-through overlay? [y/N]").Trim().ToLower()
if ($ans.StartsWith('y')) {
    Write-Host ""
    Write-Host "  * The overlay makes the native map a big see-through map in the lower-right of the screen."
    Write-Host "    Minimize the little 'Map' window to hide the controls - the overlay map stays."
    Write-Host "    Use it with the 'Spiken's Maps - Light' pack so lines show over the world."
    $size = Get-EqResolution $root
    if ($size) {
        Write-Host ("`n    Detected your EQ resolution: {0}x{1} - sizing the overlay to 200% ({2}x{3})." -f $size[0], $size[1], ($size[0] * 2), ($size[1] * 2)) -ForegroundColor Green
    } else {
        Write-Host "`n    (Couldn't read eqclient.ini - overlay stays at its default size; edit <CX>/<CY> if needed.)" -ForegroundColor Yellow
    }
    $skins = Choose-Skins $root
    Apply-Overlay $root $skins $size
    Write-Host "    In game: /loadskin <yourskin> (or relog) to apply."
}

Write-Host ""
Write-Host "Done. In game, open the Map and pick your pack from the top-left dropdown." -ForegroundColor Cyan
Read-Host "Press Enter to close"
