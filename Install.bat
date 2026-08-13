@echo off
REM Runs the Spiken's EQL Map Pack installer with a console window.
python "%~dp0install.py"
if errorlevel 1 pause
