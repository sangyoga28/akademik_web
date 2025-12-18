import sys
import os

# 1. Tentukan path folder proyek Anda
# Di PythonAnywhere, path ini biasanya: /home/USERNAME/MYSITE
# USERNAME = nama user PythonAnywhere Anda
# MYSITE   = nama folder project yang Anda upload
path = '/home/yourusername/mysite'  # <-- GANTI INI NANTI DI SERVER

if path not in sys.path:
    sys.path.append(path)

# 2. Impor objek aplikasi Flask Anda
# Pastikan file app.py ada di folder yang sama dengan wsgi.py ini
from app import app as application

# *Catatan: Variabel 'application' adalah konvensi yang digunakan oleh server WSGI.*