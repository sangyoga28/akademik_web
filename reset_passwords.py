import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def reset_all_passwords():
    if not os.path.exists(DATABASE_NAME):
        print("Database tidak ditemukan.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print(f"Force Reset Password Student ke default (NIM) di: {DATABASE_NAME}")

    # 1. Ambil semua mahasiswa active
    cursor.execute("SELECT nim, nama FROM tbMahasiswa")
    mahasiswa = cursor.fetchall()
    
    count = 0
    for m in mahasiswa:
        nim = m['nim']
        nama = m['nama']
        
        # Buat hash password baru (Password = NIM)
        new_hash = generate_password_hash(nim, method='pbkdf2:sha256')
        
        # Cek apakah user sudah ada
        cursor.execute("SELECT * FROM tbUser WHERE username=?", (nim,))
        user = cursor.fetchone()
        
        if user:
            # Update password existing
            try:
                cursor.execute("UPDATE tbUser SET password_hash=? WHERE username=?", (new_hash, nim))
                print(f"[RESET] Password {nama} ({nim}) -> Reset ke NIM.")
                count += 1
            except Exception as e:
                print(f"Gagal update {nim}: {e}")
        else:
            # Create user baru jika belum ada (misal korban cleanup berlebihan)
            try:
                cursor.execute("INSERT INTO tbUser (username, password_hash, role) VALUES (?, ?, 'Mahasiswa')", 
                               (nim, new_hash))
                print(f"[CREATE] User {nama} ({nim}) dibuatkan akun baru.")
                count += 1
            except Exception as e:
                print(f"Gagal create user {nim}: {e}")

    conn.commit()
    conn.close()
    print("------------------------------------------------")
    print(f"Selesai! {count} Akun mahasiswa telah di-reset passwordnya menjadi NIM masing-masing.")

if __name__ == "__main__":
    reset_all_passwords()
