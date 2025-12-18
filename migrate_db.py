import sqlite3
import os

import sqlite3
import os

# Gunakan lokasi yang PASTI sama dengan repository.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def migrate():
    if not os.path.exists(DATABASE_NAME):
        print(f"DEBUG: Mencari database di: {DATABASE_NAME}")
        print("PERINGATAN: Database belum ditemukan di path tersebut.")
        
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    print(f"Memulai migrasi pada: {DATABASE_NAME}...")
    
    # Cek colom nilai_angka
    try:
        cursor.execute("ALTER TABLE tbKRS ADD COLUMN nilai_angka REAL")
        print("Kolom 'nilai_angka' berhasil ditambahkan.")
    except sqlite3.OperationalError:
        print("Kolom 'nilai_angka' sudah ada.")

    # Cek colom nilai_huruf
    try:
        cursor.execute("ALTER TABLE tbKRS ADD COLUMN nilai_huruf TEXT")
        print("Kolom 'nilai_huruf' berhasil ditambahkan.")
    except sqlite3.OperationalError:
        print("Kolom 'nilai_huruf' sudah ada.")
        
    conn.commit()
    conn.close()
    print("Migrasi selesai.")

if __name__ == "__main__":
    migrate()
