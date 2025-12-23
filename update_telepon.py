import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def update_phone_numbers():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Cari mahasiswa yang teleponnya kosong
        cursor.execute("SELECT nim, nama FROM tbMahasiswa WHERE telepon IS NULL OR telepon = ''")
        mahasiswa_list = cursor.fetchall()
        
        if not mahasiswa_list:
            print("Semua data mahasiswa sudah memiliki nomor telepon.")
            return

        print(f"Ditemukan {len(mahasiswa_list)} mahasiswa tanpa nomor telepon. Memperbarui...")
        
        count = 0
        for mhs in mahasiswa_list:
            nim = mhs['nim']
            # Generate dummy phone number based on NIM to make it unique but consistent
            # Usually start with 08 or 62
            dummy_phone = f"0812{nim[-8:]}" if len(nim) >= 8 else f"081299{nim}"
            
            cursor.execute("UPDATE tbMahasiswa SET telepon = ? WHERE nim = ?", (dummy_phone, nim))
            count += 1
            print(f"Updated: {mhs['nama']} ({nim}) -> {dummy_phone}")
            
        conn.commit()
        print(f"Berhasil memperbarui {count} data.")
        conn.close()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    update_phone_numbers()
