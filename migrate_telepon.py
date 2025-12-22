import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def migrate():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    try:
        print("Menambahkan kolom 'telepon' ke tbMahasiswa...")
        cursor.execute("ALTER TABLE tbMahasiswa ADD COLUMN telepon TEXT;")
        conn.commit()
        print("Migrasi berhasil!")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Kolom 'telepon' sudah ada.")
        else:
            print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
