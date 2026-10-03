# Quick Start for Windows

1. Extract the ZIP.
2. Open the project folder in VS Code.
3. Open Terminal → PowerShell.
4. Run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python data\generate_dataset.py
python backend\app.py
```

5. Open `http://127.0.0.1:5000`.
6. Complete the 44-question assessment.
7. Open the report and dashboard from the results page.
8. Run `pytest -q` for automated tests.

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and then activate again.
