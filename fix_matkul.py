import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def fix_matkul_prodi():
    if not os.path.exists(DATABASE_NAME):
        print("Database tidak ditemukan.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print(f"Sinkronisasi Prodi Mata Kuliah di: {DATABASE_NAME}")

    # 1. Ambil semua matkul yang prodi-nya kosong atau NULL
    query = "SELECT kode_matkul, nama_matkul FROM tbMatakuliah WHERE prodi IS NULL OR prodi = '' OR prodi = 'Lainnya'"
    cursor.execute(query)
    matkul_list = cursor.fetchall()

    if not matkul_list:
        print("Semua mata kuliah sudah memiliki data Prodi.")
        conn.close()
        return

    print(f"Ditemukan {len(matkul_list)} mata kuliah yang perlu sinkronisasi.")
    
    count = 0
    for mk in matkul_list:
        kode = mk['kode_matkul'].upper()
        nama = mk['nama_matkul'].lower()
        new_prodi = "Umum"

        # Mapping berdasarkan Awalan Kode (Prefix)
        if kode.startswith('TI'):
            new_prodi = "Teknik Informatika"
        elif kode.startswith('SI'):
            new_prodi = "Sistem Informasi"
        elif kode.startswith('TE'):
            new_prodi = "Teknik Elektro"
        elif kode.startswith('TIN') or kode.startswith('ID'):
            new_prodi = "Teknik Industri"
        elif kode.startswith('MN'):
            new_prodi = "Manajemen"
        elif kode.startswith('AK'):
            new_prodi = "Akuntansi"
        elif kode.startswith('ENG') or 'inggris' in nama:
            new_prodi = "Sastra Inggris"
        elif kode.startswith('JPN') or 'jepang' in nama:
            new_prodi = "Sastra Jepang"
        elif kode.startswith('HK') or kode.startswith('IH') or 'hukum' in nama:
            new_prodi = "Ilmu Hukum"
        
        # Update ke database
        cursor.execute("UPDATE tbMatakuliah SET prodi=? WHERE kode_matkul=?", (new_prodi, mk['kode_matkul']))
        print(f"[FIX] {mk['kode_matkul']} ({mk['nama_matkul']}) -> {new_prodi}")
        count += 1

    conn.commit()
    conn.close()
    print("------------------------------------------------")
    print(f"Selesai! {count} mata kuliah telah disesuaikan Prodi-nya.")

if __name__ == "__main__":
    fix_matkul_prodi()
