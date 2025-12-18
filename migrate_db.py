import sqlite3
import os

# Daftar kemungkinan lokasi database
POSSIBLE_PATHS = ["akademik.db", "../akademik.db", "instance/akademik.db"]

def migrate():
    db_path = None
    for p in POSSIBLE_PATHS:
        if os.path.exists(p):
            db_path = p
            print(f"Database ditemukan di: {os.path.abspath(p)}")
            break
            
    if db_path is None:
        print("PERINGATAN: File 'akademik.db' tidak ditemukan di folder ini maupun folder induk.")
        print("Database baru akan dibuat di 'akademik.db' saat aplikasi berjalan.")
        print("Jika aplikasi Anda sudah ada datanya, pastikan Anda berada di folder yang benar.")
        # Kita tetap coba jalankan di 'akademik.db' lokal agar tidak error, tapi ini mungkin database baru/kosong
        db_path = "akademik.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Memulai migrasi pada: {db_path}...")
    
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
