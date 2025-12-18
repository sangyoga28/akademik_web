import sqlite3
import os

DATABASE_NAME = "akademik.db"

def migrate():
    if not os.path.exists(DATABASE_NAME):
        print(f"Database {DATABASE_NAME} tidak ditemukan. Jalankan aplikasi sekali utk membuat DB.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    print("Memeriksa kolom nilai di tbKRS...")
    
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
