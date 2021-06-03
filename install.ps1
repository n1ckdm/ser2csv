python -m venv .env --prompt ser2csv
./.env/Scripts/Activate.ps1
pip install -r .\requirements.txt
pytest .\ser2csv.py
# python .\ser2csv.py --time-secs 5 delta-t 0.1 COM1