import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def migrate_structure():
    if not os.path.exists(DATABASE_NAME):
        print("Database belum ada. Jalankan aplikasi dulu.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    print(f"Migrating database at: {DATABASE_NAME}")

    # 1. Tambah kolom 'fakultas' di tbMahasiswa
    try:
        cursor.execute("ALTER TABLE tbMahasiswa ADD COLUMN fakultas TEXT")
        print("[OK] Kolom 'fakultas' ditambahkan ke tbMahasiswa.")
    except sqlite3.OperationalError:
        print("[SKIP] Kolom 'fakultas' sudah ada.")

    # 2. Tambah kolom 'prodi' di tbMatakuliah
    try:
        cursor.execute("ALTER TABLE tbMatakuliah ADD COLUMN prodi TEXT")
        print("[OK] Kolom 'prodi' ditambahkan ke tbMatakuliah.")
    except sqlite3.OperationalError:
        print("[SKIP] Kolom 'prodi' sudah ada.")

    conn.commit()
    conn.close()
    print("Migrasi Struktur Selesai.")

if __name__ == "__main__":
    migrate_structure()
