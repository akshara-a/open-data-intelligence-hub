@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" py -3.10 -m venv .venv
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Setup complete. Training is NOT started automatically.
echo Add the dataset, then run:
echo python -m src.train
echo python -m src.evaluate
echo python -m src.predict sample_images\example.jpg
echo streamlit run app.py
pause
