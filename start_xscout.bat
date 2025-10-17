@echo off
echo Starting XScout Bot...
cd /d "c:\Users\hp\Desktop\XScout"
start /B pythonw.exe xscout.py
echo XScout started in background!
timeout /t 3
