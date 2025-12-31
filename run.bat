@echo off
cd /d "%~dp0"

call artvenv\Scripts\activate.bat

if not exist logs mkdir logs

start "" /B pythonw -m src.watcher
