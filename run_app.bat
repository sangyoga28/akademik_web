@echo off
REM --- 1. Pastikan lingkungan virtual diaktifkan ---
call venv\Scripts\activate

REM --- 2. Tentukan nama file aplikasi Anda ---
set FLASK_APP=app.py

REM --- 3. Jalankan aplikasi Flask (Mode Development) ---
flask run

REM --- 4. Opsional: Jaga jendela tetap terbuka setelah selesai/error (Hanya untuk debugging) ---
pause