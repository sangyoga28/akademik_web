import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def migrate():
    print(f"Migrating database: {DATABASE_NAME}")
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Check existing columns
        cursor.execute("PRAGMA table_info(tbMatakuliah)")
        columns = [info[1] for info in cursor.fetchall()]
        
        new_columns = {
            'hari': 'TEXT',
            'jam_mulai': 'TEXT',
            'jam_selesai': 'TEXT',
            'ruang': 'TEXT'
        }
        
        for col, dtype in new_columns.items():
            if col not in columns:
                print(f"Adding column {col}...")
                cursor.execute(f"ALTER TABLE tbMatakuliah ADD COLUMN {col} {dtype}")
            else:
                print(f"Column {col} already exists.")
                
        conn.commit()
        print("Migration successful!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate()
