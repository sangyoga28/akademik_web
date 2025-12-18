import sqlite3
from werkzeug.security import generate_password_hash

DATABASE_NAME = "akademik.db"

def sync_users():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("--- Memulai Sinkronisasi User ---")
    
    # 1. Sync Mahasiswa
    cursor.execute("SELECT * FROM tbMahasiswa")
    mahasiswa_list = cursor.fetchall()
    count_mhs = 0
    
    for m in mahasiswa_list:
        nim = m['nim']
        # Cek apakah sudah ada di tbUser
        cursor.execute("SELECT * FROM tbUser WHERE username=?", (nim,))
        if not cursor.fetchone():
            # Buat akun baru
            # Default Password = NIM
            pw_hash = generate_password_hash(nim, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO tbUser (username, password_hash, role) VALUES (?, ?, ?)", 
                           (nim, pw_hash, 'Mahasiswa'))
            print(f"[OK] Akun Mahasiswa dibuat untuk NIM: {nim}")
            count_mhs += 1
            
    # 2. Sync Dosen
    cursor.execute("SELECT * FROM tbDosen")
    dosen_list = cursor.fetchall()
    count_dosen = 0
    
    for d in dosen_list:
        nip = d['nip']
        # Cek apakah sudah ada di tbUser
        cursor.execute("SELECT * FROM tbUser WHERE username=?", (nip,))
        if not cursor.fetchone():
            # Buat akun baru
            # Default Password = NIP
            pw_hash = generate_password_hash(nip, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO tbUser (username, password_hash, role) VALUES (?, ?, ?)", 
                           (nip, pw_hash, 'Dosen'))
            print(f"[OK] Akun Dosen dibuat untuk NIP: {nip}")
            count_dosen += 1
            
    conn.commit()
    conn.close()
    
    print("---------------------------------")
    print(f"Selesai! Dibuat {count_mhs} akun Mahasiswa dan {count_dosen} akun Dosen baru.")
    print("Sekarang user tersebut bisa login dengan Username & Password = NIM/NIP mereka.")

if __name__ == "__main__":
    sync_users()
