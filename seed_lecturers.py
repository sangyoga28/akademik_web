import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def seed_lecturers():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all courses
    cursor.execute("SELECT kode_matkul, nama_matkul FROM tbMatakuliah")
    courses = cursor.fetchall()
    
    # Get all existing lecturers' assigned courses
    cursor.execute("SELECT matkul_ajar FROM tbDosen")
    existing_assignments = {l['matkul_ajar'] for l in cursor.fetchall()}
    
    # Find courses that don't have a lecturer
    missing_courses = []
    for c in courses:
        if c['nama_matkul'] not in existing_assignments:
            missing_courses.append(c['nama_matkul'])
    
    if not missing_courses:
        print("All courses already have lecturers.")
        conn.close()
        return

    # Find max NIP to continue sequence
    cursor.execute("SELECT nip FROM tbDosen")
    nips = [int(row['nip']) for row in cursor.fetchall() if row['nip'].isdigit()]
    next_nip = max(nips) + 1 if nips else 9001
    
    print(f"Adding lecturers for {len(missing_courses)} courses starting with NIP {next_nip}...")

    added_count = 0
    for course_name in missing_courses:
        nip = str(next_nip)
        name = f"Dosen {course_name}"
        phone = f"08123456{nip[-4:].zfill(4)}"
        
        try:
            # 1. Add to tbDosen
            cursor.execute("INSERT INTO tbDosen (nip, nama, matkul_ajar, telepon) VALUES (?, ?, ?, ?)", 
                           (nip, name, course_name, phone))
            
            # 2. Add to tbUser (Account)
            hashed_pw = generate_password_hash(nip, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO tbUser (username, password_hash, role) VALUES (?, ?, ?)", 
                           (nip, hashed_pw, 'Dosen'))
            
            print(f"Added: {name} (NIP: {nip})")
            next_nip += 1
            added_count += 1
        except Exception as e:
            print(f"Error adding {name}: {e}")
            
    conn.commit()
    conn.close()
    print(f"\nSuccessfully added {added_count} new lecturers and their accounts.")

if __name__ == "__main__":
    seed_lecturers()
