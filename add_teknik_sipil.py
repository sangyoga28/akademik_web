import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

# ==================== TEKNIK SIPIL CURRICULUM ====================
# Format: (Kode, Nama, SKS, Semester, Prodi)
TEKNIK_SIPIL_COURSES = [
    # Semester 1 (24 SKS)
    ("TS101", "Matematika Teknik I", 3, 1, "Teknik Sipil"),
    ("TS102", "Fisika Teknik", 3, 1, "Teknik Sipil"),
    ("TS103", "Kimia Teknik", 3, 1, "Teknik Sipil"),
    ("TS104", "Gambar Teknik Sipil", 2, 1, "Teknik Sipil"),
    ("TS105", "Pengantar Teknik Sipil", 3, 1, "Teknik Sipil"),
    ("TS106", "Mekanika Teknik I", 3, 1, "Teknik Sipil"),
    ("TS107", "Bahasa Inggris Teknik", 2, 1, "Teknik Sipil"),
    ("TS108", "Pendidikan Agama", 2, 1, "Teknik Sipil"),
    ("TS109", "Pancasila", 2, 1, "Teknik Sipil"),
    ("TS110", "Praktikum Fisika", 1, 1, "Teknik Sipil"),
    
    # Semester 2 (24 SKS)
    ("TS201", "Matematika Teknik II", 3, 2, "Teknik Sipil"),
    ("TS202", "Mekanika Teknik II", 4, 2, "Teknik Sipil"),
    ("TS203", "Mekanika Fluida", 3, 2, "Teknik Sipil"),
    ("TS204", "Ilmu Ukur Tanah", 3, 2, "Teknik Sipil"),
    ("TS205", "Teknologi Bahan Konstruksi", 3, 2, "Teknik Sipil"),
    ("TS206", "Statistika dan Probabilitas", 3, 2, "Teknik Sipil"),
    ("TS207", "Kewarganegaraan", 2, 2, "Teknik Sipil"),
    ("TS208", "Praktikum Mekanika Fluida", 2, 2, "Teknik Sipil"),
    ("TS209", "Komputer Teknik Sipil", 1, 2, "Teknik Sipil"),
    
    # Semester 3 (24 SKS)
    ("TS301", "Mekanika Tanah I", 4, 3, "Teknik Sipil"),
    ("TS302", "Struktur Beton I", 4, 3, "Teknik Sipil"),
    ("TS303", "Struktur Baja I", 3, 3, "Teknik Sipil"),
    ("TS304", "Hidrologi", 3, 3, "Teknik Sipil"),
    ("TS305", "Analisis Struktur I", 3, 3, "Teknik Sipil"),
    ("TS306", "Manajemen Konstruksi I", 3, 3, "Teknik Sipil"),
    ("TS307", "Etika Profesi", 2, 3, "Teknik Sipil"),
    ("TS308", "Praktikum Mekanika Tanah", 2, 3, "Teknik Sipil"),
    
    # Semester 4 (24 SKS)
    ("TS401", "Mekanika Tanah II", 3, 4, "Teknik Sipil"),
    ("TS402", "Struktur Beton II", 4, 4, "Teknik Sipil"),
    ("TS403", "Struktur Baja II", 3, 4, "Teknik Sipil"),
    ("TS404", "Hidraulika", 3, 4, "Teknik Sipil"),
    ("TS405", "Analisis Struktur II", 3, 4, "Teknik Sipil"),
    ("TS406", "Rekayasa Jalan Raya", 3, 4, "Teknik Sipil"),
    ("TS407", "Kewirausahaan", 2, 4, "Teknik Sipil"),
    ("TS408", "Praktikum Struktur Beton", 3, 4, "Teknik Sipil"),
    
    # Semester 5 (24 SKS)
    ("TS501", "Rekayasa Pondasi", 4, 5, "Teknik Sipil"),
    ("TS502", "Struktur Bangunan Gedung", 3, 5, "Teknik Sipil"),
    ("TS503", "Rekayasa Lalu Lintas", 3, 5, "Teknik Sipil"),
    ("TS504", "Drainase Perkotaan", 3, 5, "Teknik Sipil"),
    ("TS505", "Manajemen Konstruksi II", 3, 5, "Teknik Sipil"),
    ("TS506", "Estimasi Biaya", 3, 5, "Teknik Sipil"),
    ("TS507", "Bahasa Indonesia", 2, 5, "Teknik Sipil"),
    ("TS508", "Praktikum Rekayasa Pondasi", 3, 5, "Teknik Sipil"),
    
    # Semester 6 (24 SKS)
    ("TS601", "Rekayasa Gempa", 3, 6, "Teknik Sipil"),
    ("TS602", "Jembatan", 4, 6, "Teknik Sipil"),
    ("TS603", "Bangunan Air", 3, 6, "Teknik Sipil"),
    ("TS604", "Perkerasan Jalan", 3, 6, "Teknik Sipil"),
    ("TS605", "Dinamika Struktur", 3, 6, "Teknik Sipil"),
    ("TS606", "Teknologi Beton", 3, 6, "Teknik Sipil"),
    ("TS607", "Metodologi Penelitian", 2, 6, "Teknik Sipil"),
    ("TS608", "Praktikum Jembatan", 3, 6, "Teknik Sipil"),
    
    # Semester 7 (24 SKS)
    ("TS701", "Rekayasa Pantai", 3, 7, "Teknik Sipil"),
    ("TS702", "Manajemen Proyek Konstruksi", 3, 7, "Teknik Sipil"),
    ("TS703", "Sistem Informasi Geografis", 3, 7, "Teknik Sipil"),
    ("TS704", "Bangunan Tahan Gempa", 3, 7, "Teknik Sipil"),
    ("TS705", "Kerja Praktek", 3, 7, "Teknik Sipil"),
    ("TS706", "Mata Kuliah Pilihan I", 3, 7, "Teknik Sipil"),
    ("TS707", "Mata Kuliah Pilihan II", 3, 7, "Teknik Sipil"),
    ("TS708", "Seminar Proposal", 3, 7, "Teknik Sipil"),
    
    # Semester 8 (6 SKS - Tugas Akhir)
    ("TS801", "Tugas Akhir", 6, 8, "Teknik Sipil"),
]

# Realistic Indonesian lecturer names for Teknik Sipil
TEKNIK_SIPIL_LECTURERS = [
    "Dr. Ir. Bambang Suhendro, M.T.",
    "Prof. Dr. Ir. Wiryanto Dewobroto, M.Sc.",
    "Dr. Ir. Harianto Hardjasaputra, M.Eng.",
    "Ir. Asriwiyanti Desiani, M.T.",
    "Dr. Ir. Paulus Pramono Rahardjo, M.Sc.",
    "Prof. Dr. Ir. Iswandi Imran, M.Sc.",
    "Dr. Ir. Yanuar Haryanto, M.T.",
    "Ir. Endah Wahyuni, M.Sc.",
    "Dr. Ir. Tavio Tavio, M.T.",
    "Prof. Dr. Ir. Djoko Legono, M.Eng.",
    "Dr. Ir. Iman Satyarno, M.Eng.",
    "Ir. Niken Silmi Surjandari, M.T.",
    "Dr. Ir. Budi Suswanto, M.T.",
    "Prof. Dr. Ir. Radianta Triatmadja, M.Sc.",
    "Dr. Ir. Ary Setyawan, M.Sc.",
    "Ir. Leksmono Suryo Putranto, M.T.",
    "Dr. Ir. Faimun Faimun, M.T.",
    "Prof. Dr. Ir. Sarwidi Sarwidi, M.Eng.",
    "Dr. Ir. Data Iranata, M.T.",
    "Ir. Nur Iriawan Gatot, M.Sc.",
    "Dr. Ir. Edy Purwanto, M.T.",
    "Prof. Dr. Ir. Bambang Triatmodjo, M.Sc.",
    "Dr. Ir. Mochamad Solikin, M.T.",
    "Ir. Dwi Prasetya Utomo, M.Eng.",
    "Dr. Ir. Januarti Jaya Ekaputri, M.T.",
    "Prof. Dr. Ir. Priyo Suprobo, M.Sc.",
    "Dr. Ir. Umboro Lasminto, M.Sc.",
    "Ir. Cahyono Bintang Nurcahyo, M.T.",
    "Dr. Ir. Tri Joko Wahyu Adi, M.T.",
    "Prof. Dr. Ir. Djwantoro Hardjito, M.Eng.",
    "Dr. Ir. Nadjadji Anwar, M.Sc.",
    "Ir. Ria Asih Aryani Soemitro, M.T.",
    "Dr. Ir. Ervina Ahyudanari, M.T.",
    "Prof. Dr. Ir. Hitapriya Suprayitno, M.T.",
    "Dr. Ir. Wasis Wardoyo, M.Sc.",
    "Ir. Farida Rachmawati, M.T.",
    "Dr. Ir. Christiono Utomo, M.T.",
    "Prof. Dr. Ir. I Putu Artama Wiguna, M.T.",
    "Dr. Ir. Retno Indryani, M.Sc.",
    "Ir. Supani Supani, M.T.",
    "Dr. Ir. Yusroniya Eka Putri, M.T.",
    "Prof. Dr. Ir. Amien Widodo, M.Sc.",
    "Dr. Ir. Mas Agus Mardyanto, M.Eng.",
    "Ir. Theresia MCA Retno Wulan, M.T.",
    "Dr. Ir. Ridho Bayuaji, M.T.",
    "Prof. Dr. Ir. Triwulan Triwulan, M.T.",
    "Dr. Ir. Dian Rahmawati, M.T.",
    "Ir. Putu Artama Wiguna, M.Sc.",
    "Dr. Ir. Hera Widyastuti, M.T.",
    "Prof. Dr. Ir. Eko Budi Djatmiko, M.Sc.",
]

# Student names for Teknik Sipil (5 students per semester, total 40 students)
TEKNIK_SIPIL_STUDENTS = [
    # Semester 1 (Angkatan 2024)
    ("Andi Setiawan", 1), ("Budi Prasetyo", 1), ("Citra Dewi", 1), 
    ("Dedi Kurniawan", 1), ("Eka Putri Lestari", 1),
    # Semester 2 (Angkatan 2023 Semester 2)
    ("Fajar Ramadhan", 2), ("Gita Permata Sari", 2), ("Hendra Gunawan", 2),
    ("Indah Wulandari", 2), ("Joko Susilo", 2),
    # Semester 3 (Angkatan 2023 Semester 3)
    ("Kartika Sari", 3), ("Lukman Hakim", 3), ("Maya Anggraini", 3),
    ("Nanda Pratama", 3), ("Oscar Wijaya", 3),
    # Semester 4 (Angkatan 2022 Semester 4)
    ("Putri Maharani", 4), ("Qomar Zaman", 4), ("Rizky Firmansyah", 4),
    ("Siti Nurhaliza", 4), ("Taufik Hidayat", 4),
    # Semester 5 (Angkatan 2022 Semester 5)
    ("Umar Bakri", 5), ("Vina Melati", 5), ("Wawan Setiawan", 5),
    ("Yanti Suryani", 5), ("Zainal Arifin", 5),
    # Semester 6 (Angkatan 2021 Semester 6)
    ("Agus Salim", 6), ("Bella Safitri", 6), ("Cahyo Wibowo", 6),
    ("Diana Putri", 6), ("Eko Wijayanto", 6),
    # Semester 7 (Angkatan 2021 Semester 7)
    ("Faisal Ahmad", 7), ("Galih Pratama", 7), ("Hana Safira", 7),
    ("Irfan Hakim", 7), ("Julia Rahmawati", 7),
    # Semester 8 (Angkatan 2020 Semester 8)
    ("Kurnia Sandi", 8), ("Linda Wijaya", 8), ("Maulana Ibrahim", 8),
    ("Nina Kartika", 8), ("Oki Firmansyah", 8),
]

def add_teknik_sipil_program():
    """
    Menambahkan program studi Teknik Sipil lengkap dengan:
    - Mata kuliah (24 SKS per semester untuk semester 1-7)
    - Dosen untuk setiap mata kuliah
    - Mahasiswa untuk setiap semester
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 70)
    print("ADDING TEKNIK SIPIL PROGRAM")
    print("=" * 70)
    
    # 1. Add Courses
    print("\n[1] Adding Teknik Sipil Courses...")
    cursor.execute("SELECT kode_matkul FROM tbMatakuliah")
    existing_courses = {row['kode_matkul'] for row in cursor.fetchall()}
    
    added_courses = 0
    for course in TEKNIK_SIPIL_COURSES:
        kode, nama, sks, semester, prodi = course
        if kode not in existing_courses:
            try:
                cursor.execute("""
                    INSERT INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi)
                    VALUES (?, ?, ?, ?, ?)
                """, (kode, nama, sks, semester, prodi))
                print(f"  [+] {kode} - {nama} ({sks} SKS, Sem {semester})")
                added_courses += 1
            except Exception as e:
                print(f"  [-] Error adding {kode}: {e}")
        else:
            print(f"  [=] Exists: {kode}")
    
    conn.commit()
    print(f"\n  Total courses added: {added_courses}")
    
    # 2. Add Lecturers
    print("\n[2] Assigning Lecturers to Courses...")
    cursor.execute("SELECT nip FROM tbDosen ORDER BY nip DESC LIMIT 1")
    last_nip = cursor.fetchone()
    if last_nip and last_nip['nip'].isdigit():
        next_nip = int(last_nip['nip']) + 1
    else:
        next_nip = 1991100200
    
    cursor.execute("SELECT matkul_ajar FROM tbDosen")
    assigned_courses = {row['matkul_ajar'] for row in cursor.fetchall()}
    
    added_lecturers = 0
    lecturer_index = 0
    
    for course in TEKNIK_SIPIL_COURSES:
        course_name = course[1]  # nama matkul
        
        if course_name in assigned_courses:
            print(f"  [=] Lecturer exists for: {course_name}")
            continue
        
        if lecturer_index < len(TEKNIK_SIPIL_LECTURERS):
            lecturer_name = TEKNIK_SIPIL_LECTURERS[lecturer_index]
            lecturer_index += 1
        else:
            lecturer_name = f"Dr. Ir. Dosen TS {lecturer_index}, M.T."
            lecturer_index += 1
        
        nip = str(next_nip)
        phone = f"08{next_nip % 10000000000:010d}"
        
        try:
            cursor.execute("""
                INSERT INTO tbDosen (nip, nama, matkul_ajar, telepon)
                VALUES (?, ?, ?, ?)
            """, (nip, lecturer_name, course_name, phone))
            
            hashed_pw = generate_password_hash(nip, method='pbkdf2:sha256')
            cursor.execute("""
                INSERT INTO tbUser (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (nip, hashed_pw, 'Dosen'))
            
            print(f"  [+] {lecturer_name} -> {course_name} (NIP: {nip})")
            added_lecturers += 1
            next_nip += 1
        except Exception as e:
            print(f"  [-] Error: {e}")
            next_nip += 1
    
    conn.commit()
    print(f"\n  Total lecturers added: {added_lecturers}")
    
    # 3. Add Students
    print("\n[3] Adding Teknik Sipil Students...")
    cursor.execute("SELECT nim FROM tbMahasiswa ORDER BY nim DESC LIMIT 1")
    last_nim = cursor.fetchone()
    if last_nim and last_nim['nim'].isdigit():
        next_nim = int(last_nim['nim']) + 1
    else:
        next_nim = 2020100001
    
    added_students = 0
    for student_name, semester in TEKNIK_SIPIL_STUDENTS:
        nim = str(next_nim)
        alamat = f"Jl. Teknik Sipil No. {added_students + 1}, Kota Pelajar"
        fakultas = "Teknik"
        
        try:
            cursor.execute("""
                INSERT INTO tbMahasiswa (nim, nama, alamat, prodi, fakultas)
                VALUES (?, ?, ?, ?, ?)
            """, (nim, student_name, alamat, "Teknik Sipil", fakultas))
            
            hashed_pw = generate_password_hash(nim, method='pbkdf2:sha256')
            cursor.execute("""
                INSERT INTO tbUser (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (nim, hashed_pw, 'Mahasiswa'))
            
            print(f"  [+] {student_name} (NIM: {nim}, Semester {semester})")
            added_students += 1
            next_nim += 1
        except Exception as e:
            print(f"  [-] Error: {e}")
            next_nim += 1
    
    conn.commit()
    print(f"\n  Total students added: {added_students}")
    
    # 4. Verify SKS Distribution
    print("\n[4] Verifying SKS Distribution for Teknik Sipil...")
    print("-" * 70)
    cursor.execute("""
        SELECT semester, COUNT(*) as jumlah_matkul, SUM(sks) as total_sks
        FROM tbMatakuliah
        WHERE prodi = 'Teknik Sipil'
        GROUP BY semester
        ORDER BY semester
    """)
    
    for row in cursor.fetchall():
        status = "[OK]" if row['total_sks'] >= 24 else "[!!]"
        print(f"  {status} Teknik Sipil Semester {row['semester']}: {row['jumlah_matkul']:2} courses, {row['total_sks']:2} SKS")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("TEKNIK SIPIL PROGRAM ADDED SUCCESSFULLY!")
    print("=" * 70)
    print(f"[+] {added_courses} courses added")
    print(f"[+] {added_lecturers} lecturers added")
    print(f"[+] {added_students} students added")
    print(f"[+] All users have accounts (password = NIM/NIP)")
    print("=" * 70)

if __name__ == "__main__":
    add_teknik_sipil_program()
