import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

# Comprehensive curriculum data with realistic Indonesian course names
# Format: (Kode, Nama, SKS, Semester, Prodi)
COMPREHENSIVE_CURRICULUM = [
    # ==================== INFORMATIKA ====================
    # Semester 1 (24 SKS)
    ("INF101", "Dasar Pemrograman", 3, 1, "Informatika"),
    ("INF102", "Matematika Diskrit", 3, 1, "Informatika"),
    ("INF103", "Pengantar Teknologi Informasi", 3, 1, "Informatika"),
    ("INF104", "Logika Informatika", 3, 1, "Informatika"),
    ("INF105", "Bahasa Inggris I", 2, 1, "Informatika"),
    ("INF106", "Pendidikan Agama", 2, 1, "Informatika"),
    ("INF107", "Pancasila", 2, 1, "Informatika"),
    ("INF108", "Kalkulus I", 3, 1, "Informatika"),
    ("INF109", "Fisika Dasar", 3, 1, "Informatika"),
    
    # Semester 2 (24 SKS)
    ("INF201", "Struktur Data", 4, 2, "Informatika"),
    ("INF202", "Algoritma Pemrograman", 4, 2, "Informatika"),
    ("INF203", "Arsitektur Komputer", 3, 2, "Informatika"),
    ("INF204", "Aljabar Linear", 3, 2, "Informatika"),
    ("INF205", "Kalkulus II", 3, 2, "Informatika"),
    ("INF206", "Bahasa Inggris II", 2, 2, "Informatika"),
    ("INF207", "Kewarganegaraan", 2, 2, "Informatika"),
    ("INF208", "Statistika Dasar", 3, 2, "Informatika"),
    
    # Semester 3 (24 SKS)
    ("INF301", "Pemrograman Berorientasi Objek", 4, 3, "Informatika"),
    ("INF302", "Basis Data", 4, 3, "Informatika"),
    ("INF303", "Sistem Operasi", 3, 3, "Informatika"),
    ("INF304", "Matematika Numerik", 3, 3, "Informatika"),
    ("INF305", "Jaringan Komputer Dasar", 3, 3, "Informatika"),
    ("INF306", "Interaksi Manusia dan Komputer", 3, 3, "Informatika"),
    ("INF307", "Probabilitas dan Statistika", 2, 3, "Informatika"),
    ("INF308", "Etika Profesi", 2, 3, "Informatika"),
    
    # Semester 4 (24 SKS)
    ("INF401", "Pemrograman Web", 4, 4, "Informatika"),
    ("INF402", "Sistem Basis Data Lanjut", 3, 4, "Informatika"),
    ("INF403", "Jaringan Komputer Lanjut", 3, 4, "Informatika"),
    ("INF404", "Analisis dan Desain Algoritma", 3, 4, "Informatika"),
    ("INF405", "Pemrograman Mobile", 4, 4, "Informatika"),
    ("INF406", "Grafika Komputer", 3, 4, "Informatika"),
    ("INF407", "Teori Bahasa dan Automata", 2, 4, "Informatika"),
    ("INF408", "Kewirausahaan", 2, 4, "Informatika"),
    
    # Semester 5 (24 SKS)
    ("INF501", "Rekayasa Perangkat Lunak", 4, 5, "Informatika"),
    ("INF502", "Kecerdasan Buatan", 4, 5, "Informatika"),
    ("INF503", "Sistem Terdistribusi", 3, 5, "Informatika"),
    ("INF504", "Keamanan Informasi", 3, 5, "Informatika"),
    ("INF505", "Pemrograman Framework", 3, 5, "Informatika"),
    ("INF506", "Data Mining", 3, 5, "Informatika"),
    ("INF507", "Manajemen Proyek TI", 2, 5, "Informatika"),
    ("INF508", "Bahasa Indonesia", 2, 5, "Informatika"),
    
    # Semester 6 (24 SKS)
    ("INF601", "Machine Learning", 4, 6, "Informatika"),
    ("INF602", "Cloud Computing", 3, 6, "Informatika"),
    ("INF603", "Internet of Things", 3, 6, "Informatika"),
    ("INF604", "Pengolahan Citra Digital", 3, 6, "Informatika"),
    ("INF605", "Sistem Informasi Enterprise", 3, 6, "Informatika"),
    ("INF606", "Pemrograman Game", 3, 6, "Informatika"),
    ("INF607", "Metodologi Penelitian", 2, 6, "Informatika"),
    ("INF608", "Komputer dan Masyarakat", 3, 6, "Informatika"),
    
    # Semester 7 (24 SKS)
    ("INF701", "Big Data Analytics", 3, 7, "Informatika"),
    ("INF702", "Blockchain Technology", 3, 7, "Informatika"),
    ("INF703", "Cyber Security", 3, 7, "Informatika"),
    ("INF704", "DevOps dan CI/CD", 3, 7, "Informatika"),
    ("INF705", "Artificial Intelligence Lanjut", 3, 7, "Informatika"),
    ("INF706", "Kerja Praktek", 3, 7, "Informatika"),
    ("INF707", "Mata Kuliah Pilihan I", 3, 7, "Informatika"),
    ("INF708", "Mata Kuliah Pilihan II", 3, 7, "Informatika"),
    
    # Semester 8 (6 SKS - Tugas Akhir)
    ("INF801", "Tugas Akhir", 6, 8, "Informatika"),
    
    # ==================== SISTEM INFORMASI ====================
    # Semester 1 (24 SKS)
    ("SI101", "Pengantar Sistem Informasi", 3, 1, "Sistem Informasi"),
    ("SI102", "Dasar Pemrograman", 3, 1, "Sistem Informasi"),
    ("SI103", "Matematika Bisnis", 3, 1, "Sistem Informasi"),
    ("SI104", "Pengantar Manajemen", 3, 1, "Sistem Informasi"),
    ("SI105", "Pengantar Akuntansi", 3, 1, "Sistem Informasi"),
    ("SI106", "Bahasa Inggris I", 2, 1, "Sistem Informasi"),
    ("SI107", "Pendidikan Agama", 2, 1, "Sistem Informasi"),
    ("SI108", "Pancasila", 2, 1, "Sistem Informasi"),
    ("SI109", "Statistika Bisnis", 3, 1, "Sistem Informasi"),
    
    # Semester 2 (24 SKS)
    ("SI201", "Analisis Proses Bisnis", 4, 2, "Sistem Informasi"),
    ("SI202", "Basis Data", 4, 2, "Sistem Informasi"),
    ("SI203", "Pemrograman Berorientasi Objek", 3, 2, "Sistem Informasi"),
    ("SI204", "Sistem Operasi", 3, 2, "Sistem Informasi"),
    ("SI205", "Manajemen Organisasi", 3, 2, "Sistem Informasi"),
    ("SI206", "Akuntansi Manajemen", 3, 2, "Sistem Informasi"),
    ("SI207", "Bahasa Inggris II", 2, 2, "Sistem Informasi"),
    ("SI208", "Kewarganegaraan", 2, 2, "Sistem Informasi"),
    
    # Semester 3 (24 SKS)
    ("SI301", "Manajemen Database", 4, 3, "Sistem Informasi"),
    ("SI302", "Analisis dan Desain Sistem", 4, 3, "Sistem Informasi"),
    ("SI303", "Pemrograman Web", 3, 3, "Sistem Informasi"),
    ("SI304", "Jaringan Komputer", 3, 3, "Sistem Informasi"),
    ("SI305", "Manajemen Pemasaran", 3, 3, "Sistem Informasi"),
    ("SI306", "Sistem Informasi Manajemen", 3, 3, "Sistem Informasi"),
    ("SI307", "Etika Profesi", 2, 3, "Sistem Informasi"),
    ("SI308", "Riset Operasi", 2, 3, "Sistem Informasi"),
    
    # Semester 4 (24 SKS)
    ("SI401", "E-Business", 4, 4, "Sistem Informasi"),
    ("SI402", "Desain UI/UX", 3, 4, "Sistem Informasi"),
    ("SI403", "Pemrograman Mobile", 3, 4, "Sistem Informasi"),
    ("SI404", "Manajemen Rantai Pasok", 3, 4, "Sistem Informasi"),
    ("SI405", "Sistem Informasi Akuntansi", 3, 4, "Sistem Informasi"),
    ("SI406", "Manajemen Keuangan", 3, 4, "Sistem Informasi"),
    ("SI407", "Kewirausahaan", 2, 4, "Sistem Informasi"),
    ("SI408", "Komunikasi Bisnis", 3, 4, "Sistem Informasi"),
    
    # Semester 5 (24 SKS)
    ("SI501", "Manajemen Proyek SI", 4, 5, "Sistem Informasi"),
    ("SI502", "Enterprise Resource Planning", 4, 5, "Sistem Informasi"),
    ("SI503", "Business Intelligence", 3, 5, "Sistem Informasi"),
    ("SI504", "Audit Sistem Informasi", 3, 5, "Sistem Informasi"),
    ("SI505", "Customer Relationship Management", 3, 5, "Sistem Informasi"),
    ("SI506", "E-Commerce", 3, 5, "Sistem Informasi"),
    ("SI507", "Bahasa Indonesia", 2, 5, "Sistem Informasi"),
    ("SI508", "Manajemen Strategi", 2, 5, "Sistem Informasi"),
    
    # Semester 6 (24 SKS)
    ("SI601", "Perencanaan Strategis SI", 4, 6, "Sistem Informasi"),
    ("SI602", "Data Warehouse", 3, 6, "Sistem Informasi"),
    ("SI603", "Tata Kelola TI", 3, 6, "Sistem Informasi"),
    ("SI604", "Keamanan Sistem Informasi", 3, 6, "Sistem Informasi"),
    ("SI605", "Sistem Pendukung Keputusan", 3, 6, "Sistem Informasi"),
    ("SI606", "Digital Marketing", 3, 6, "Sistem Informasi"),
    ("SI607", "Metodologi Penelitian", 2, 6, "Sistem Informasi"),
    ("SI608", "Manajemen Risiko TI", 3, 6, "Sistem Informasi"),
    
    # Semester 7 (24 SKS)
    ("SI701", "Inovasi Sistem Informasi", 3, 7, "Sistem Informasi"),
    ("SI702", "Cloud Computing untuk Bisnis", 3, 7, "Sistem Informasi"),
    ("SI703", "Analytics dan Big Data", 3, 7, "Sistem Informasi"),
    ("SI704", "Sistem Informasi Global", 3, 7, "Sistem Informasi"),
    ("SI705", "Kerja Praktek", 3, 7, "Sistem Informasi"),
    ("SI706", "Mata Kuliah Pilihan I", 3, 7, "Sistem Informasi"),
    ("SI707", "Mata Kuliah Pilihan II", 3, 7, "Sistem Informasi"),
    ("SI708", "Seminar Proposal", 3, 7, "Sistem Informasi"),
    
    # Semester 8 (6 SKS - Tugas Akhir)
    ("SI801", "Tugas Akhir", 6, 8, "Sistem Informasi"),
    
    # ==================== TEKNIK ELEKTRO ====================
    # Semester 1 (24 SKS)
    ("TE101", "Rangkaian Listrik I", 3, 1, "Teknik Elektro"),
    ("TE102", "Fisika Dasar I", 3, 1, "Teknik Elektro"),
    ("TE103", "Kalkulus I", 3, 1, "Teknik Elektro"),
    ("TE104", "Kimia Dasar", 3, 1, "Teknik Elektro"),
    ("TE105", "Gambar Teknik", 2, 1, "Teknik Elektro"),
    ("TE106", "Pengantar Teknik Elektro", 3, 1, "Teknik Elektro"),
    ("TE107", "Bahasa Inggris I", 2, 1, "Teknik Elektro"),
    ("TE108", "Pendidikan Agama", 2, 1, "Teknik Elektro"),
    ("TE109", "Pancasila", 2, 1, "Teknik Elektro"),
    ("TE110", "Praktikum Fisika Dasar", 1, 1, "Teknik Elektro"),
    
    # Semester 2 (24 SKS)
    ("TE201", "Rangkaian Listrik II", 3, 2, "Teknik Elektro"),
    ("TE202", "Elektronika Dasar", 4, 2, "Teknik Elektro"),
    ("TE203", "Fisika Dasar II", 3, 2, "Teknik Elektro"),
    ("TE204", "Kalkulus II", 3, 2, "Teknik Elektro"),
    ("TE205", "Pemrograman Komputer", 3, 2, "Teknik Elektro"),
    ("TE206", "Matematika Teknik I", 3, 2, "Teknik Elektro"),
    ("TE207", "Bahasa Inggris II", 2, 2, "Teknik Elektro"),
    ("TE208", "Kewarganegaraan", 2, 2, "Teknik Elektro"),
    ("TE209", "Praktikum Elektronika Dasar", 1, 2, "Teknik Elektro"),
    
    # Semester 3 (24 SKS)
    ("TE301", "Sistem Digital", 4, 3, "Teknik Elektro"),
    ("TE302", "Sinyal dan Sistem", 3, 3, "Teknik Elektro"),
    ("TE303", "Elektronika Analog", 4, 3, "Teknik Elektro"),
    ("TE304", "Matematika Teknik II", 3, 3, "Teknik Elektro"),
    ("TE305", "Mesin Listrik I", 3, 3, "Teknik Elektro"),
    ("TE306", "Pengukuran Listrik", 3, 3, "Teknik Elektro"),
    ("TE307", "Etika Profesi", 2, 3, "Teknik Elektro"),
    ("TE308", "Praktikum Sistem Digital", 2, 3, "Teknik Elektro"),
    
    # Semester 4 (24 SKS)
    ("TE401", "Medan Elektromagnetik", 3, 4, "Teknik Elektro"),
    ("TE402", "Sistem Kendali", 4, 4, "Teknik Elektro"),
    ("TE403", "Elektronika Daya", 3, 4, "Teknik Elektro"),
    ("TE404", "Mesin Listrik II", 3, 4, "Teknik Elektro"),
    ("TE405", "Mikroprosesor", 4, 4, "Teknik Elektro"),
    ("TE406", "Teknik Telekomunikasi", 3, 4, "Teknik Elektro"),
    ("TE407", "Kewirausahaan", 2, 4, "Teknik Elektro"),
    ("TE408", "Praktikum Mikroprosesor", 2, 4, "Teknik Elektro"),
    
    # Semester 5 (24 SKS)
    ("TE501", "Mikrokontroler", 4, 5, "Teknik Elektro"),
    ("TE502", "Sistem Tenaga Listrik", 3, 5, "Teknik Elektro"),
    ("TE503", "Pengolahan Sinyal Digital", 3, 5, "Teknik Elektro"),
    ("TE504", "Sistem Komunikasi", 3, 5, "Teknik Elektro"),
    ("TE505", "Instrumentasi Industri", 3, 5, "Teknik Elektro"),
    ("TE506", "Sistem Embedded", 3, 5, "Teknik Elektro"),
    ("TE507", "Bahasa Indonesia", 2, 5, "Teknik Elektro"),
    ("TE508", "Praktikum Mikrokontroler", 3, 5, "Teknik Elektro"),
    
    # Semester 6 (24 SKS)
    ("TE601", "Sistem Kendali Digital", 3, 6, "Teknik Elektro"),
    ("TE602", "Proteksi Sistem Tenaga", 3, 6, "Teknik Elektro"),
    ("TE603", "Antena dan Propagasi", 3, 6, "Teknik Elektro"),
    ("TE604", "Robotika", 4, 6, "Teknik Elektro"),
    ("TE605", "PLC dan SCADA", 3, 6, "Teknik Elektro"),
    ("TE606", "Energi Terbarukan", 3, 6, "Teknik Elektro"),
    ("TE607", "Metodologi Penelitian", 2, 6, "Teknik Elektro"),
    ("TE608", "Praktikum Robotika", 3, 6, "Teknik Elektro"),
    
    # Semester 7 (24 SKS)
    ("TE701", "Teknik Tegangan Tinggi", 3, 7, "Teknik Elektro"),
    ("TE702", "Sistem Kontrol Cerdas", 3, 7, "Teknik Elektro"),
    ("TE703", "Internet of Things", 3, 7, "Teknik Elektro"),
    ("TE704", "Smart Grid", 3, 7, "Teknik Elektro"),
    ("TE705", "Kerja Praktek", 3, 7, "Teknik Elektro"),
    ("TE706", "Mata Kuliah Pilihan I", 3, 7, "Teknik Elektro"),
    ("TE707", "Mata Kuliah Pilihan II", 3, 7, "Teknik Elektro"),
    ("TE708", "Seminar Proposal", 3, 7, "Teknik Elektro"),
    
    # Semester 8 (6 SKS - Tugas Akhir)
    ("TE801", "Tugas Akhir", 6, 8, "Teknik Elektro"),
]

# Realistic Indonesian lecturer names with academic titles
LECTURER_NAMES = [
    "Dr. Ir. Budi Santoso, M.T.",
    "Prof. Dr. Siti Nurhaliza, M.Kom.",
    "Dr. Ahmad Fauzi, S.T., M.T.",
    "Drs. Bambang Wijaya, M.Sc.",
    "Ir. Dewi Lestari, M.Eng.",
    "Dr. Hendra Gunawan, M.Kom.",
    "Prof. Dr. Ratna Sari, M.Si.",
    "Dr. Joko Widodo, S.T., M.T.",
    "Ir. Maya Puspita, M.T.",
    "Dr. Agus Salim, M.Kom.",
    "Dra. Sri Wahyuni, M.Pd.",
    "Dr. Eko Prasetyo, S.T., M.T.",
    "Ir. Lilis Suryani, M.Eng.",
    "Dr. Wahyu Hidayat, M.Kom.",
    "Prof. Dr. Ani Widiastuti, M.T.",
    "Dr. Rizky Ramadhan, S.T., M.T.",
    "Ir. Indah Permata, M.Sc.",
    "Dr. Fajar Nugroho, M.Kom.",
    "Drs. Lukman Hakim, M.Si.",
    "Dr. Citra Dewi, S.T., M.T.",
    "Ir. Dedi Kurniawan, M.Eng.",
    "Dr. Eka Putri, M.Kom.",
    "Prof. Dr. Gita Maharani, M.T.",
    "Dr. Hadi Susanto, S.T., M.T.",
    "Ir. Kiki Amelia, M.Sc.",
    "Dr. Nanda Pratama, M.Kom.",
    "Dra. Oscar Wijayanti, M.Pd.",
    "Dr. Putra Mahendra, S.T., M.T.",
    "Ir. Rina Kusuma, M.Eng.",
    "Dr. Surya Dharma, M.Kom.",
    "Prof. Dr. Tari Wulandari, M.T.",
    "Dr. Umar Bakri, S.T., M.T.",
    "Ir. Vina Melati, M.Sc.",
    "Dr. Wawan Setiawan, M.Kom.",
    "Drs. Yanto Suryanto, M.Si.",
    "Dr. Zainal Arifin, S.T., M.T.",
    "Ir. Ayu Lestari, M.Eng.",
    "Dr. Bayu Firmansyah, M.Kom.",
    "Prof. Dr. Candra Kirana, M.T.",
    "Dr. Dimas Pradipta, S.T., M.T.",
    "Ir. Elsa Maharani, M.Sc.",
    "Dr. Farhan Maulana, M.Kom.",
    "Dra. Gina Puspita, M.Pd.",
    "Dr. Haris Setiawan, S.T., M.T.",
    "Ir. Intan Permatasari, M.Eng.",
    "Dr. Jaya Kusuma, M.Kom.",
    "Prof. Dr. Kartika Sari, M.T.",
    "Dr. Lutfi Rahman, S.T., M.T.",
    "Ir. Mega Wulandari, M.Sc.",
    "Dr. Noval Hidayat, M.Kom.",
    "Drs. Okta Wijaya, M.Si.",
    "Dr. Pandu Winata, S.T., M.T.",
    "Ir. Qori Amalia, M.Eng.",
    "Dr. Reza Pahlevi, M.Kom.",
    "Prof. Dr. Sari Indah, M.T.",
    "Dr. Taufik Hidayat, S.T., M.T.",
    "Ir. Umi Kalsum, M.Sc.",
    "Dr. Vicky Prasetya, M.Kom.",
    "Dra. Wulan Dari, M.Pd.",
    "Dr. Yoga Aditya, S.T., M.T.",
    "Ir. Zara Amira, M.Eng.",
    "Dr. Adi Nugroho, M.Kom.",
    "Prof. Dr. Bella Safitri, M.T.",
    "Dr. Cahyo Wibowo, S.T., M.T.",
    "Ir. Diana Putri, M.Sc.",
    "Dr. Eko Wijayanto, M.Kom.",
    "Drs. Faisal Ahmad, M.Si.",
    "Dr. Galih Pratama, S.T., M.T.",
    "Ir. Hana Safira, M.Eng.",
    "Dr. Irfan Hakim, M.Kom.",
    "Prof. Dr. Julia Rahmawati, M.T.",
    "Dr. Kurnia Sandi, S.T., M.T.",
    "Ir. Linda Wijaya, M.Sc.",
    "Dr. Maulana Ibrahim, M.Kom.",
    "Dra. Nina Kartika, M.Pd.",
    "Dr. Oki Firmansyah, S.T., M.T.",
    "Ir. Putri Maharani, M.Eng.",
    "Dr. Qomar Zaman, M.Kom.",
    "Prof. Dr. Rani Puspita, M.T.",
    "Dr. Sigit Purnomo, S.T., M.T.",
    "Ir. Tina Melinda, M.Sc.",
    "Dr. Udin Saepudin, M.Kom.",
    "Drs. Vino Andika, M.Si.",
    "Dr. Widi Astuti, S.T., M.T.",
    "Ir. Yuni Safitri, M.Eng.",
    "Dr. Zaki Mubarak, M.Kom.",
    "Prof. Dr. Anggun Pramesti, M.T.",
    "Dr. Bima Sakti, S.T., M.T.",
    "Ir. Cinta Lestari, M.Sc.",
    "Dr. Doni Prasetyo, M.Kom.",
    "Dra. Erna Wati, M.Pd.",
    "Dr. Firman Syahputra, S.T., M.T.",
    "Ir. Gita Anggraini, M.Eng.",
    "Dr. Heru Santoso, M.Kom.",
    "Prof. Dr. Ika Purnama, M.T.",
    "Dr. Jefri Kurniawan, S.T., M.T.",
    "Ir. Kartini Dewi, M.Sc.",
    "Dr. Luthfi Hakim, M.Kom.",
    "Drs. Maman Sulaeman, M.Si.",
    "Dr. Novi Andriani, S.T., M.T.",
    "Ir. Olivia Putri, M.Eng.",
    "Dr. Pandu Mahardika, M.Kom.",
]

def seed_comprehensive_data():
    """
    Menambahkan data mata kuliah dan dosen secara komprehensif.
    Setiap semester di setiap prodi akan memiliki minimal 24 SKS.
    Setiap mata kuliah akan memiliki dosen pengajar.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 70)
    print("SEEDING COMPREHENSIVE ACADEMIC DATA")
    print("=" * 70)
    
    # 1. Get existing courses to avoid duplicates
    cursor.execute("SELECT kode_matkul FROM tbMatakuliah")
    existing_courses = {row['kode_matkul'] for row in cursor.fetchall()}
    
    # 2. Add new courses
    print("\n[1] Adding Course Data...")
    added_courses = 0
    for course in COMPREHENSIVE_CURRICULUM:
        kode, nama, sks, semester, prodi = course
        if kode not in existing_courses:
            try:
                cursor.execute("""
                    INSERT INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi)
                    VALUES (?, ?, ?, ?, ?)
                """, (kode, nama, sks, semester, prodi))
                added_courses += 1
                print(f"  [+] Added: {kode} - {nama} ({sks} SKS, Sem {semester}, {prodi})")
            except sqlite3.IntegrityError as e:
                print(f"  [-] Skip: {kode} - {e}")
        else:
            print(f"  [=] Exists: {kode}")
    
    conn.commit()
    print(f"\n  Total courses added: {added_courses}")
    
    # 3. Get all courses and assign lecturers
    print("\n[2] Assigning Lecturers to Courses...")
    cursor.execute("SELECT kode_matkul, nama_matkul FROM tbMatakuliah ORDER BY kode_matkul")
    all_courses = cursor.fetchall()
    
    # Get existing lecturer assignments
    cursor.execute("SELECT matkul_ajar FROM tbDosen")
    assigned_courses = {row['matkul_ajar'] for row in cursor.fetchall()}
    
    # Find the next available NIP
    cursor.execute("SELECT nip FROM tbDosen ORDER BY nip DESC LIMIT 1")
    last_nip = cursor.fetchone()
    if last_nip and last_nip['nip'].isdigit():
        next_nip = int(last_nip['nip']) + 1
    else:
        next_nip = 1990010201  # Starting NIP
    
    added_lecturers = 0
    lecturer_index = 0
    
    for course in all_courses:
        course_name = course['nama_matkul']
        
        # Skip if already assigned
        if course_name in assigned_courses:
            print(f"  [=] Lecturer exists for: {course_name}")
            continue
        
        # Assign a lecturer
        if lecturer_index < len(LECTURER_NAMES):
            lecturer_name = LECTURER_NAMES[lecturer_index]
            lecturer_index += 1
        else:
            # Generate additional lecturer if we run out of names
            lecturer_name = f"Dr. Dosen {lecturer_index}, M.T."
            lecturer_index += 1
        
        nip = str(next_nip)
        phone = f"08{next_nip % 10000000000:010d}"
        
        try:
            # Add to tbDosen
            cursor.execute("""
                INSERT INTO tbDosen (nip, nama, matkul_ajar, telepon)
                VALUES (?, ?, ?, ?)
            """, (nip, lecturer_name, course_name, phone))
            
            # Add to tbUser (create account)
            hashed_pw = generate_password_hash(nip, method='pbkdf2:sha256')
            cursor.execute("""
                INSERT INTO tbUser (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (nip, hashed_pw, 'Dosen'))
            
            print(f"  [+] Added: {lecturer_name} -> {course_name} (NIP: {nip})")
            added_lecturers += 1
            next_nip += 1
            
        except sqlite3.IntegrityError as e:
            print(f"  [-] Error adding lecturer for {course_name}: {e}")
            next_nip += 1
    
    conn.commit()
    print(f"\n  Total lecturers added: {added_lecturers}")
    
    # 4. Verify SKS distribution
    print("\n[3] Verifying SKS Distribution...")
    print("-" * 70)
    cursor.execute("""
        SELECT prodi, semester, COUNT(*) as jumlah_matkul, SUM(sks) as total_sks
        FROM tbMatakuliah
        GROUP BY prodi, semester
        ORDER BY prodi, semester
    """)
    
    for row in cursor.fetchall():
        status = "[OK]" if row['total_sks'] >= 24 else "[!!]"
        print(f"  {status} {row['prodi']:25} Sem {row['semester']}: {row['jumlah_matkul']:2} courses, {row['total_sks']:2} SKS")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("SEEDING COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"[+] {added_courses} courses added")
    print(f"[+] {added_lecturers} lecturers added")
    print(f"[+] All lecturers have user accounts (password = NIP)")
    print("=" * 70)

if __name__ == "__main__":
    seed_comprehensive_data()
