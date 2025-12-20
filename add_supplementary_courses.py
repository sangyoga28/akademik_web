import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

# Additional courses to reach 24 SKS for semesters that are below
SUPPLEMENTARY_COURSES = [
    # Informatika - add 1 SKS to semesters 2, 3, 4, 5, 6
    ("INF209", "Praktikum Pemrograman", 1, 2, "Informatika"),
    ("INF309", "Praktikum Basis Data", 2, 3, "Informatika"),
    ("INF409", "Praktikum Web Development", 1, 4, "Informatika"),
    ("INF509", "Praktikum AI", 2, 5, "Informatika"),
    ("INF609", "Praktikum Machine Learning", 1, 6, "Informatika"),
    
    # Sistem Informasi - add 1 SKS to semesters 2, 3, 4, 5, 6
    ("SI209", "Praktikum Database", 1, 2, "Sistem Informasi"),
    ("SI309", "Praktikum Analisis Sistem", 1, 3, "Sistem Informasi"),
    ("SI409", "Praktikum E-Business", 1, 4, "Sistem Informasi"),
    ("SI509", "Praktikum ERP", 1, 5, "Sistem Informasi"),
    ("SI609", "Praktikum Business Intelligence", 1, 6, "Sistem Informasi"),
    
    # Teknik Elektro - add 1 SKS to semesters 3, 5
    ("TE309", "Praktikum Elektronika Analog", 1, 3, "Teknik Elektro"),
    ("TE509", "Praktikum Sistem Tenaga", 1, 5, "Teknik Elektro"),
]

ADDITIONAL_LECTURERS = [
    "Dr. Andi Wijaya, M.T.",
    "Ir. Bella Kusuma, M.Eng.",
    "Dr. Chandra Putra, M.Kom.",
    "Dra. Diah Ayu, M.Pd.",
    "Dr. Edi Santoso, S.T., M.T.",
    "Ir. Fitri Handayani, M.Sc.",
    "Dr. Guntur Prakoso, M.Kom.",
    "Prof. Dr. Hesti Wulandari, M.T.",
    "Dr. Indra Kusuma, S.T., M.T.",
    "Ir. Jasmine Putri, M.Eng.",
    "Dr. Krisna Mahardika, M.Kom.",
    "Drs. Lestari Wijaya, M.Si.",
]

def add_supplementary_courses():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 70)
    print("ADDING SUPPLEMENTARY COURSES")
    print("=" * 70)
    
    # Get existing courses
    cursor.execute("SELECT kode_matkul FROM tbMatakuliah")
    existing_courses = {row['kode_matkul'] for row in cursor.fetchall()}
    
    # Find next available NIP
    cursor.execute("SELECT nip FROM tbDosen ORDER BY nip DESC LIMIT 1")
    last_nip = cursor.fetchone()
    if last_nip and last_nip['nip'].isdigit():
        next_nip = int(last_nip['nip']) + 1
    else:
        next_nip = 1991100161
    
    added_courses = 0
    lecturer_index = 0
    
    for course in SUPPLEMENTARY_COURSES:
        kode, nama, sks, semester, prodi = course
        
        if kode in existing_courses:
            print(f"  [=] Exists: {kode}")
            continue
        
        try:
            # Add course
            cursor.execute("""
                INSERT INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi)
                VALUES (?, ?, ?, ?, ?)
            """, (kode, nama, sks, semester, prodi))
            print(f"  [+] Added course: {kode} - {nama} ({sks} SKS, Sem {semester}, {prodi})")
            
            # Add lecturer
            if lecturer_index < len(ADDITIONAL_LECTURERS):
                lecturer_name = ADDITIONAL_LECTURERS[lecturer_index]
                lecturer_index += 1
            else:
                lecturer_name = f"Dr. Dosen {lecturer_index + 200}, M.T."
                lecturer_index += 1
            
            nip = str(next_nip)
            phone = f"08{next_nip % 10000000000:010d}"
            
            cursor.execute("""
                INSERT INTO tbDosen (nip, nama, matkul_ajar, telepon)
                VALUES (?, ?, ?, ?)
            """, (nip, lecturer_name, nama, phone))
            
            hashed_pw = generate_password_hash(nip, method='pbkdf2:sha256')
            cursor.execute("""
                INSERT INTO tbUser (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (nip, hashed_pw, 'Dosen'))
            
            print(f"      Lecturer: {lecturer_name} (NIP: {nip})")
            added_courses += 1
            next_nip += 1
            
        except Exception as e:
            print(f"  [-] Error: {e}")
    
    conn.commit()
    
    # Verify final SKS distribution
    print("\n" + "=" * 70)
    print("FINAL SKS DISTRIBUTION")
    print("=" * 70)
    
    cursor.execute("""
        SELECT prodi, semester, COUNT(*) as jumlah_matkul, SUM(sks) as total_sks
        FROM tbMatakuliah
        WHERE prodi IN ('Informatika', 'Sistem Informasi', 'Teknik Elektro')
        GROUP BY prodi, semester
        ORDER BY prodi, semester
    """)
    
    for row in cursor.fetchall():
        status = "[OK]" if row['total_sks'] >= 24 else "[!!]"
        print(f"  {status} {row['prodi']:25} Sem {row['semester']}: {row['jumlah_matkul']:2} courses, {row['total_sks']:2} SKS")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print(f"[+] {added_courses} supplementary courses added")
    print("=" * 70)

if __name__ == "__main__":
    add_supplementary_courses()
