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
        kode = mk['kode_matkul'].upper().strip()
        nama = mk['nama_matkul'].lower().strip()
        new_prodi = "Umum"

        # 1. Mapping Berdasarkan KODE (Prefix)
        # Teknik Informatika
        if any(kode.startswith(pre) for pre in ['TI', 'IF', 'ILKOM', 'KOM']):
            new_prodi = "Teknik Informatika"
        # Sistem Informasi
        elif any(kode.startswith(pre) for pre in ['SI', 'MSI']):
            new_prodi = "Sistem Informasi"
        # Teknik Elektro
        elif any(kode.startswith(pre) for pre in ['TE', 'EL']):
            new_prodi = "Teknik Elektro"
        # Teknik Industri
        elif any(kode.startswith(pre) for pre in ['TIN', 'ID', 'IND']):
            new_prodi = "Teknik Industri"
        # Manajemen
        elif any(kode.startswith(pre) for pre in ['MN', 'MJ', 'MAN']):
            new_prodi = "Manajemen"
        # Akuntansi
        elif any(kode.startswith(pre) for pre in ['AK', 'AKT', 'ACC']):
            new_prodi = "Akuntansi"
        # Sastra Inggris
        elif any(kode.startswith(pre) for pre in ['ENG', 'ING', 'SI']):
             if 'inggris' in nama: new_prodi = "Sastra Inggris"
        # Ilmu Hukum
        elif any(kode.startswith(pre) for pre in ['HK', 'IH', 'LAW']):
            new_prodi = "Ilmu Hukum"
            
        # 2. Mapping Berdasarkan NAMA (Fuzzy) - Jika Kode belum spesifik
        if new_prodi == "Umum":
            if any(k in nama for k in ['informatika', 'komputer', 'pemrograman', 'data', 'jaringan']):
                new_prodi = "Teknik Informatika"
            elif any(k in nama for k in ['sistem informasi', 'bisnis', 'analisis']):
                new_prodi = "Sistem Informasi"
            elif any(k in nama for k in ['elektro', 'listrik']):
                new_prodi = "Teknik Elektro"
            elif any(k in nama for k in ['industri', 'pabrik']):
                new_prodi = "Teknik Industri"
            elif any(k in nama for k in ['manajemen', 'bisnis', 'pemasaran', 'sdm']):
                new_prodi = "Manajemen"
            elif any(k in nama for k in ['akuntansi', 'pajak', 'audit', 'fiskal']):
                new_prodi = "Akuntansi"
            elif any(k in nama for k in ['inggris', 'english']):
                new_prodi = "Sastra Inggris"
            elif any(k in nama for k in ['jepang', 'japan']):
                new_prodi = "Sastra Jepang"
            elif any(k in nama for k in ['hukum', 'perdata', 'pidana', 'ih']):
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
