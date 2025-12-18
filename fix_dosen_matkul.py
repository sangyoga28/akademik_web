import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def fix_dosen_matkul():
    if not os.path.exists(DATABASE_NAME):
        print("Database tidak ditemukan.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print(f"Sinkronisasi Matkul Dosen di: {DATABASE_NAME}")

    # Mapping Manual untuk Nama yang Sering Beda/Singkat
    mapping = {
        'Basis Data': 'Basis Data 1',
        'Struktur Data': 'Algoritma & Struktur Data',
        'Pemrograman Mobile': 'Pengembangan Mobile',
        'Kalkulus': 'Matematika Diskrit', # Pendekatan terdekat jika tdk ada kalkulus
        'Keamanan Informasi': 'Keamanan Siber',
        'Statistika': 'Aljabar Linear', # Dummy mapping jika tdk ada statistika
        'Manajemen Proyek': 'Manajemen Proyek SI',
        'Grafika Komputer': 'Desain UI/UX'
    }

    cursor.execute("SELECT nip, nama, matkul_ajar FROM tbDosen")
    dosen_list = cursor.fetchall()

    count = 0
    for d in dosen_list:
        nip = d['nip']
        nama_dosen = d['nama']
        matkul_lama = d['matkul_ajar']
        
        # 1. Cek apakah matkul lama ada di mapping manual
        new_name = mapping.get(matkul_lama)
        
        # 2. Jika tidak ada di mapping, coba cari yang mirip (LIke)
        if not new_name:
            cursor.execute("SELECT nama_matkul FROM tbMatakuliah WHERE nama_matkul LIKE ?", (f'%{matkul_lama}%',))
            match = cursor.fetchone()
            if match:
                new_name = match['nama_matkul']

        if new_name and new_name != matkul_lama:
            cursor.execute("UPDATE tbDosen SET matkul_ajar=? WHERE nip=?", (new_name, nip))
            print(f"[FIX] {nama_dosen} ({nip}): '{matkul_lama}' -> '{new_name}'")
            count += 1
        elif not new_name:
            # Cari matkul pertama yang ada di DB saja sebagai default jika benar-benar tidak ketemu
            cursor.execute("SELECT nama_matkul FROM tbMatakuliah LIMIT 1")
            first_mk = cursor.fetchone()
            if first_mk:
                new_name = first_mk['nama_matkul']
                cursor.execute("UPDATE tbDosen SET matkul_ajar=? WHERE nip=?", (new_name, nip))
                print(f"[DEFAULT] {nama_dosen} ({nip}): '{matkul_lama}' -> '{new_name}' (Tidak ketemu matkul cocok)")
                count += 1

    conn.commit()
    conn.close()
    print("------------------------------------------------")
    print(f"Selesai! {count} data dosen telah disesuaikan mata kuliah ajarnya.")

if __name__ == "__main__":
    fix_dosen_matkul()
