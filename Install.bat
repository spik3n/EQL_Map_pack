@echo off
REM Spiken's EQL Map Pack installer.
REM Uses Windows PowerShell (built into Windows) - no Python required.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install.ps1"
if errorlevel 1 pause
