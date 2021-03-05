set workdir=%~dp0
cd %workdir%
SET PYTHONPATH=.
python auto_remove/main.py
