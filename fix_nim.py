import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def fix_nim():
    if not os.path.exists(DATABASE_NAME):
        print("Database tidak ditemukan.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print(f"Memperbaiki NIM di database: {DATABASE_NAME}")

    # 1. Ambil semua mahasiswa
    cursor.execute("SELECT nim FROM tbMahasiswa")
    mahasiswa = cursor.fetchall()
    
    count = 0
    for m in mahasiswa:
        old_nim = m['nim']
        
        # Cek jika panjang < 10
        if len(old_nim) < 10:
            # Pad dengan '0' di tengah atau di depan? 
            # Biasanya NIM itu ada kode tahun, prodi, urut. 
            # Asumsi simpel: Pad dengan 0 di belakang tahun (jika format tahun di depan)
            # Atau paling aman: Pad '0' di depan sampai 10 digit (untuk sekadar memenuhi syarat)
            # TAPI, user mungkin mau format spesifik.
            # Mari kita coba padding standar: 2023001 -> 2023000001 (sisipkan 0 setelah 4 digit pertama)
            
            if len(old_nim) == 7: 
                # Asumsi format lama: 2023001 (4 digit tahun + 3 digit urut)
                # Format baru: 2023100001 (4 digit tahun + 1 digit kode + 5 digit urut)
                # Kita ubah jadi: 2023 + 00 + 001 ? 
                # Mari kita pakai padding sederhana 0 di tengah.
                new_nim = old_nim[:4] + "000" + old_nim[4:]
            else:
                # Fallback: Pad zero di depan agar 10 digit
                new_nim = old_nim.zfill(10)
            
            print(f"Fixing: {old_nim} -> {new_nim}")
            
            try:
                # Update tbMahasiswa
                # Hati-hati constraint PK, harus hapus insert atau update cascade jika SQLite support
                # Karena update PK di SQLite agak tricky kalau ada Foreign Key (tbKRS, tbUser) disable FK check dulu
                cursor.execute("PRAGMA foreign_keys=OFF")
                
                cursor.execute("UPDATE tbMahasiswa SET nim=? WHERE nim=?", (new_nim, old_nim))
                cursor.execute("UPDATE tbUser SET username=? WHERE username=?", (new_nim, old_nim))
                # Update KRS juga
                cursor.execute("UPDATE tbKRS SET nim=? WHERE nim=?", (new_nim, old_nim))
                
                count += 1
            except Exception as e:
                print(f"Gagal update {old_nim}: {e}")

    conn.commit()
    conn.close()
    print(f"Selesai! {count} NIM berhasil diperbarui menjadi 10 digit.")

if __name__ == "__main__":
    fix_nim()
