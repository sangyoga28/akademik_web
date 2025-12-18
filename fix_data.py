import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def determine_faculty(prodi):
    """Menentukan Fakultas berdasarkan nama Prodi."""
    if not prodi:
        return None
        
    p = prodi.lower().strip()
    
    # Cek yang spesifik dulu
    if p in ['ti', 'si', 'if', 'ilkom']:
        return 'Fakultas Teknik'
    if p in ['mn', 'mj', 'ak', 'akt']:
        return 'Fakultas Ekonomi'
        
    # Cek substring
    if 'teknik' in p or 'sistem informasi' in p or 'informatika' in p or 'komputer' in p or 'elektro' in p:
        return 'Fakultas Teknik'
    elif 'manajemen' in p or 'akuntansi' in p or 'ekonomi' in p or 'bisnis' in p or 'fiskal' in p:
        return 'Fakultas Ekonomi'
    elif 'sastra' in p or 'bahasa' in p or 'inggris' in p or 'jepang' in p:
        return 'Fakultas Sastra'
    elif 'hukum' in p:
        return 'Fakultas Hukum'
    else:
        # Debugging: Print apa yang gagal dimapping
        print(f"[DEBUG] Prodi '{prodi}' masuk kategori Lainnya.")
        return 'Fakultas Lainnya'

def fix_data():
    if not os.path.exists(DATABASE_NAME):
        print("Database tidak ditemukan.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print(f"Memulai perbaikan data di: {DATABASE_NAME}")

    # 1. Ambil semua data mahasiswa
    cursor.execute("SELECT * FROM tbMahasiswa")
    mahasiswa_list = cursor.fetchall()
    
    count_nim = 0
    count_fakultas = 0
    
    # Disable Foreign Keys sementara agar update PK (NIM) lancar
    cursor.execute("PRAGMA foreign_keys=OFF")
    
    for m in mahasiswa_list:
        old_nim = m['nim']
        nama = m['nama']
        prodi = m['prodi']
        
        # --- FIX 1: NIM 10 DIGIT ---
        new_nim = old_nim
        if len(old_nim) < 10:
            if len(old_nim) == 7: # Asumsi format lama 2023001
                new_nim = old_nim[:4] + "000" + old_nim[4:] # Jadi 2023000001
            else:
                new_nim = old_nim.zfill(10) # Pad zero depan
            
            try:
                cursor.execute("UPDATE tbMahasiswa SET nim=? WHERE nim=?", (new_nim, old_nim))
                cursor.execute("UPDATE tbUser SET username=? WHERE username=?", (new_nim, old_nim))
                cursor.execute("UPDATE tbKRS SET nim=? WHERE nim=?", (new_nim, old_nim))
                print(f"[NIM] Fixed {old_nim} -> {new_nim}")
                count_nim += 1
            except Exception as e:
                print(f"[NIM] Gagal update {old_nim}: {e}")
        
        # --- FIX 2: ISI FAKULTAS ---
        # Jika kosong ATAU "Fakultas Lainnya" (karena salah mapping sebelumnya), kita coba fix lagi
        current_fakultas = m['fakultas'] if 'fakultas' in m.keys() else None
        
        if not current_fakultas or current_fakultas == 'Fakultas Lainnya':
            fakultas_baru = determine_faculty(prodi)
            if fakultas_baru:
                cursor.execute("UPDATE tbMahasiswa SET fakultas=? WHERE nim=?", (fakultas_baru, new_nim))
                print(f"[Fakultas] {nama} ({prodi}) -> {fakultas_baru}")
                count_fakultas += 1

    conn.commit()
    conn.close()
    
    print("------------------------------------------------")
    print(f"Selesai! {count_nim} NIM diperbaiki, {count_fakultas} Fakultas diisi.")

if __name__ == "__main__":
    fix_data()
