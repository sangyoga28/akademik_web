import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE_NAME = "akademik.db"

def verify_and_fix():
    if not os.path.exists(DATABASE_NAME):
        print(f"Error: {DATABASE_NAME} not found.")
        return

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("Checking tbUser...", flush=True)
    
    # 1. Ensure Admin exists
    cursor.execute("SELECT * FROM tbUser WHERE username = 'admin'")
    admin = cursor.fetchone()
    
    if not admin:
        print("Admin user missing. Creating admin...", flush=True)
        hashed_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
        cursor.execute("INSERT INTO tbUser (username, password_hash, role) VALUES (?, ?, ?)", 
                       ('admin', hashed_pw, 'Admin Sistem'))
        print("Admin user created (admin / admin123)", flush=True)
    else:
        print(f"Admin found: {admin['username']}", flush=True)

    # 2. Check if students have accounts
    cursor.execute("SELECT nim FROM tbMahasiswa")
    students = cursor.fetchall()
    print(f"Found {len(students)} students. Checking accounts...", flush=True)
    
    count_created = 0
    for s in students:
        nim = s[0]
        cursor.execute("SELECT 1 FROM tbUser WHERE username = ?", (nim,))
        if not cursor.fetchone():
            hashed_pw = generate_password_hash(nim, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO tbUser (username, password_hash, role) VALUES (?, ?, ?)", 
                           (nim, hashed_pw, 'Mahasiswa'))
            count_created += 1
            if count_created % 10 == 0:
                print(f"  Created {count_created} student accounts...", flush=True)
    
    if count_created > 0:
        print(f"Total created {count_created} missing student accounts.", flush=True)

    # 3. Check if lecturers have accounts
    cursor.execute("SELECT nip FROM tbDosen")
    dosen = cursor.fetchall()
    print(f"Found {len(dosen)} lecturers. Checking accounts...", flush=True)
    
    count_created = 0
    for d in dosen:
        nip = d[0]
        cursor.execute("SELECT 1 FROM tbUser WHERE username = ?", (nip,))
        if not cursor.fetchone():
            hashed_pw = generate_password_hash(nip, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO tbUser (username, password_hash, role) VALUES (?, ?, ?)", 
                           (nip, hashed_pw, 'Dosen'))
            count_created += 1
            if count_created % 10 == 0:
                print(f"  Created {count_created} lecturer accounts...", flush=True)
            
    if count_created > 0:
        print(f"Total created {count_created} missing lecturer accounts.", flush=True)

    conn.commit()
    conn.close()
    print("Verification and fixes completed.")

if __name__ == "__main__":
    verify_and_fix()
