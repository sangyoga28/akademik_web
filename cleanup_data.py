import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def cleanup_data():
    if not os.path.exists(DATABASE_NAME):
        print("Database tidak ditemukan.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print(f"Memulai PEMBERSIHAN data di: {DATABASE_NAME}")

    # 1. Cari Mahasiswa dengan NIM != 10 digit (termasuk yang 3 digit) ATAU Fakultas Kosong
    query = "SELECT nim, nama FROM tbMahasiswa WHERE length(trim(nim)) != 10 OR fakultas IS NULL OR fakultas = ''"
    cursor.execute(query)
    bad_data = cursor.fetchall()

    if not bad_data:
        print("Tidak ditemukan data mahasiswa dengan NIM < 10 digit (seperti NIM 3 angka) atau Fakultas kosong.")
        conn.close()
        return

    print(f"Ditemukan {len(bad_data)} data mahasiswa invalid yang akan dihapus (termasuk NIM 3 angka).")
    
    # Konfirmasi (langsung eksekusi sesuai request user)
    count = 0
    cursor.execute("PRAGMA foreign_keys=OFF")

    for m in bad_data:
        nim = m['nim']
        nama = m['nama']
        print(f"MENGHAPUS DATA LEGACY: {nim} - {nama}")
        
        try:
            # Hapus dari semua tabel terkait
            cursor.execute("DELETE FROM tbMahasiswa WHERE nim=?", (nim,))
            cursor.execute("DELETE FROM tbUser WHERE username=?", (nim,))
            cursor.execute("DELETE FROM tbKRS WHERE nim=?", (nim,))
            cursor.execute("DELETE FROM tbPembayaran WHERE nim=?", (nim,))
            
            count += 1
        except Exception as e:
            print(f"Gagal hapus {nim}: {e}")

    conn.commit()
    conn.close()
    print("------------------------------------------------")
    print(f"Selesai! {count} data mahasiswa (dan akun loginnya) telah dihapus.")

if __name__ == "__main__":
    cleanup_data()
