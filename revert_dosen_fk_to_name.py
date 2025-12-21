import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def revert_and_fill():
    conn = sqlite3.connect(DATABASE_NAME)
    # conn.row_factory = sqlite3.Row # Don't use Row factory for UPDATE cursor safety sometimes
    cursor = conn.cursor()
    
    print("REVERTING DOSEN FK TO NAMES & ENSURING COVERAGE...")
    
    # 1. REVERT CODES TO NAMES
    print("[1/2] Converting Dosen FK (Code -> Name)...")
    cursor.execute("SELECT nip, matkul_ajar FROM tbDosen")
    all_dosen = cursor.fetchall()
    
    updated_count = 0
    for nip, matkul_ref in all_dosen:
        # Check if this ref exists as a CODE in tbMatakuliah
        cursor.execute("SELECT nama_matkul FROM tbMatakuliah WHERE kode_matkul = ?", (matkul_ref,))
        result = cursor.fetchone()
        
        if result:
            nama_matkul = result[0]
            # Update to Name
            cursor.execute("UPDATE tbDosen SET matkul_ajar = ? WHERE nip = ?", (nama_matkul, nip))
            updated_count += 1
            # print(f"  Converted {matkul_ref} -> {nama_matkul} for NIP {nip}")
            
    print(f"      Converted {updated_count} records to Name format.")
    
    # 2. ENSURE EVERY MATKUL HAS A DOSEN (Based on NAME matching)
    print("\n[2/2] Checking Coverage (Every Matkul must have a Dosen)...")
    
    cursor.execute("SELECT kode_matkul, nama_matkul FROM tbMatakuliah")
    all_matkul = cursor.fetchall()
    
    # Get all taught courses (Names)
    cursor.execute("SELECT DISTINCT matkul_ajar FROM tbDosen")
    taught_courses = {row[0] for row in cursor.fetchall()}
    
    # Find next available NIP
    cursor.execute("SELECT nip FROM tbDosen ORDER BY nip DESC LIMIT 1")
    last_nip_row = cursor.fetchone()
    next_nip = int(last_nip_row[0]) + 1 if last_nip_row and last_nip_row[0].isdigit() else 1999900000
    
    added_dosen = 0
    
    for kode, nama in all_matkul:
        if nama not in taught_courses:
            # Add Dosen for this course
            print(f"  [MISSING] {kode} - {nama}. Adding Lecturer...")
            
            lecturer_name = f"Dosen Pengampu {kode}"
            nip = str(next_nip)
            phone = f"081{next_nip}"
            
            cursor.execute("INSERT INTO tbDosen (nip, nama, matkul_ajar, telepon) VALUES (?, ?, ?, ?)", 
                           (nip, lecturer_name, nama, phone))
            
            # Add User
            pw_hash = generate_password_hash(nip)
            cursor.execute("INSERT INTO tbUser (username, password_hash, role) VALUES (?, ?, ?)",
                           (nip, pw_hash, 'Dosen'))
                           
            next_nip += 1
            added_dosen += 1
            taught_courses.add(nama) # Mark as covered
            
    print(f"      Added {added_dosen} new lecturers to ensure 100% coverage.")
    
    conn.commit()
    conn.close()
    print("\nDone. Data structure is now NAME-based and fully covered.")

if __name__ == "__main__":
    revert_and_fill()
