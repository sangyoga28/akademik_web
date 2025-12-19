import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def debug():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("--- tbKRS linked with Payment (Top 20) ---")
    query = """
        SELECT k.nim, k.kode_matkul, k.semester, k.tahun_ajaran, p.status as status_bayar
        FROM tbKRS k
        LEFT JOIN tbPembayaran p ON k.nim = p.nim AND k.semester = p.semester AND k.tahun_ajaran = p.tahun_ajaran
        LIMIT 20
    """
    cursor.execute(query)
    for row in cursor.fetchall():
        print(dict(row))
        
    print("\n--- Summary of Years/Semesters in tbKRS ---")
    cursor.execute("SELECT DISTINCT semester, tahun_ajaran FROM tbKRS")
    for row in cursor.fetchall():
        print(dict(row))

    conn.close()

if __name__ == "__main__":
    debug()
