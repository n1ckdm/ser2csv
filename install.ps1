python -m venv .env --prompt ser2csv
./.env/Scripts/Activate.ps1
pip install -r .\requirements.txt
python .\ser2csv.py COM1 --time-secs 5 delta-t 0.1