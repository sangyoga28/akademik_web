import sqlite3
import os
import repository as repo
from werkzeug.security import generate_password_hash

def reset_and_seed():
    db_path = repo.DATABASE_NAME
    
    # 1. Hapus DB lama jika ada
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Database lama '{db_path}' telah dihapus.")

    # 2. Inisialisasi Database (Buat Tabel)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    repo.buat_tabel(conn)
    print("Tabel-tabel baru berhasil dibuat.")

    # 3. Seed Admin
    hashed_pw_admin = generate_password_hash('admin123', method='pbkdf2:sha256')
    repo.tambah_user(conn, 'admin', hashed_pw_admin, role='Admin Sistem')
    print("User 'admin' (pass: admin123) ditambahkan.")

    # 4. Seed Mata Kuliah (Comprehensive per Semester & Prodi)
    matkul_template = [
        # Semester 1
        ('INF101', 'Dasar Pemrograman', 3, 1, 'Informatika'),
        ('SI101', 'Pengantar Sistem Informasi', 3, 1, 'Sistem Informasi'),
        ('TE101', 'Rangkaian Listrik I', 3, 1, 'Teknik Elektro'),
        ('KU101', 'Pendidikan Agama', 2, 1, 'Umum'),
        ('KU102', 'Bahasa Inggris', 2, 1, 'Umum'),
        # Semester 2
        ('INF201', 'Struktur Data', 3, 2, 'Informatika'),
        ('SI201', 'Analisis Proses Bisnis', 3, 2, 'Sistem Informasi'),
        ('TE201', 'Elektronika Dasar', 3, 2, 'Teknik Elektro'),
        ('KU201', 'Pancasila & Kewarganegaraan', 2, 2, 'Umum'),
        # Semester 3
        ('INF301', 'Pemrograman Berorientasi Objek', 3, 3, 'Informatika'),
        ('SI301', 'Manajemen Database', 3, 3, 'Sistem Informasi'),
        ('TE301', 'Sistem Digital', 3, 3, 'Teknik Elektro'),
        ('INF302', 'Arsitektur Komputer', 3, 3, 'Informatika'),
        # Semester 4
        ('INF401', 'Pemrograman Web', 3, 4, 'Informatika'),
        ('SI401', 'E-Business', 3, 4, 'Sistem Informasi'),
        ('TE401', 'Medan Elektromagnetik', 3, 4, 'Teknik Elektro'),
        ('INF402', 'Sistem Operasi', 3, 4, 'Informatika'),
        # Semester 5
        ('INF501', 'Jaringan Komputer', 3, 5, 'Informatika'),
        ('SI501', 'Audit Sistem Informasi', 3, 5, 'Sistem Informasi'),
        ('TE501', 'Mikrokontroler', 3, 5, 'Teknik Elektro'),
        ('INF502', 'Kecerdasan Buatan', 3, 5, 'Informatika'),
        # Semester 6
        ('INF601', 'Rekayasa Perangkat Lunak', 3, 6, 'Informatika'),
        ('SI601', 'Perencanaan Strategis SI', 3, 6, 'Sistem Informasi'),
        ('TE601', 'Sistem Kendali', 3, 6, 'Teknik Elektro'),
        ('KU601', 'Metodologi Penelitian', 2, 6, 'Umum'),
        # Semester 7
        ('INF701', 'Keamanan Informasi', 3, 7, 'Informatika'),
        ('SI701', 'Data Warehouse', 3, 7, 'Sistem Informasi'),
        ('TE701', 'Teknik Tegangan Tinggi', 3, 7, 'Teknik Elektro'),
        ('KU701', 'Kerja Praktek', 2, 7, 'Umum'),
        # Semester 8
        ('INF801', 'Tugas Akhir Informatika', 6, 8, 'Informatika'),
        ('SI801', 'Tugas Akhir SI', 6, 8, 'Sistem Informasi'),
        ('TE801', 'Tugas Akhir Elektro', 6, 8, 'Teknik Elektro'),
    ]
    for mk in matkul_template:
        repo.tambah_data_matkul(conn, *mk)
    print(f"{len(matkul_template)} Mata Kuliah ditambahkan.")

    # 5. Seed Dosen (Realistic names, 10-digit NIP)
    dosen_pool = [
        ('1990010101', 'Dr. Ir. Hendra Wijaya, M.T.', '081122334455'),
        ('1990010102', 'Prof. Dr. Ratna Sari, M.Kom.', '081122334456'),
        ('1990010103', 'Dr. Agus Pratama, S.T., M.T.', '081122334457'),
        ('1990010104', 'Drs. Bambang Sudarsono, M.Sc.', '081122334458'),
        ('1990010105', 'Ir. Siti Aminah, M.Eng.', '081122334459'),
        ('1990010106', 'Ph.D. Joko Susilo', '081122334460'),
        ('1990010107', 'Dr. Dewi Lestari, M.Si.', '081122334461'),
        ('1990010108', 'M.Hum. Andi Kurniawan', '081122334462'),
        ('1990010109', 'Dr. Sri Wahyuni', '081122334463'),
        ('1990010110', 'Ir. Budi Raharjo', '081122334464'),
        ('1990010111', 'M.Pd. Lilis Suryani', '081122334465'),
        ('1990010112', 'Dr. Wahyu Utama', '081122334466'),
        ('1990010113', 'M.T. Rizky Ramadhan', '081122334467'),
        ('1990010114', 'Ph.D. Maria Ulfa', '081122334468'),
        ('1990010115', 'Dr. Ahmad Zulkarnain', '081122334469'),
    ]

    all_subjects = [mk[1] for mk in matkul_template]
    
    # We need to assign each subject to ONE and ONLY ONE Nip initially to avoid UNIQUE constraint on Nip 
    # OR we can assign one Nip to multiple subjects if allowed (it is, but we must use one NIP per entry).
    # Wait, the table tbDosen has NIP as PRIMARY KEY. 
    # Current structure: nip TEXT PRIMARY KEY, nama TEXT NOT NULL, matkul_ajar TEXT, telepon TEXT
    # This means one NIP can only teach ONE course in the database record. 
    # To fix this properly, we should probably change the schema or just assign one course per lecturer.
    # User said: "pastikan semua data kuliah memiliki dosen pengajarnya"
    # If one NIP can only teach one course (due to PK), we need more lecturers.
    
    # I will expand the pool to match the number of subjects.
    while len(dosen_pool) < len(all_subjects):
        next_id = len(dosen_pool) + 1
        dosen_pool.append((f'1991{100000 + next_id:06}', f'Dosen {next_id}', f'0899{next_id:06}'))

    for i, subj in enumerate(all_subjects):
        nip, nama, telp = dosen_pool[i]
        repo.tambah_data_dosen(conn, nip, nama, subj, telp)
        # Account creation
        if repo.cari_user_by_username(conn, nip) is None:
            hashed_pw = generate_password_hash(nip, method='pbkdf2:sha256')
            repo.tambah_user(conn, nip, hashed_pw, role='Dosen')

    print(f"{len(all_subjects)} Dosen dipetakan ke {len(all_subjects)} Mata Kuliah.")

    # 6. Seed Mahasiswa (Realistic names, 10-digit NIM)
    mhs_names = [
        ('Ahmad Fauzi', 'Informatika'), ('Budi Santoso', 'Informatika'), ('Citra Lestari', 'Informatika'),
        ('Dedi Irawan', 'Informatika'), ('Eka Putri', 'Informatika'),
        ('Fajar Gunawan', 'Sistem Informasi'), ('Gita Permata', 'Sistem Informasi'), ('Hadi Syahputra', 'Sistem Informasi'),
        ('Indah Jaya', 'Sistem Informasi'), ('Joko Susanto', 'Sistem Informasi'),
        ('Kiki Amelia', 'Teknik Elektro'), ('Lukman Hakim', 'Teknik Elektro'), ('Maya Sari', 'Teknik Elektro'),
        ('Nanda Octavian', 'Teknik Elektro'), ('Oscar Pratama', 'Teknik Elektro')
    ]
    
    fakultas_map = {
        'Informatika': 'Teknik & Ilmu Komputer',
        'Sistem Informasi': 'Teknik & Ilmu Komputer',
        'Teknik Elektro': 'Teknik'
    }

    for i, (name, prodi) in enumerate(mhs_names):
        nim = f"2023{100000 + i + 1:06}"
        alamat = f"Jl. Contoh No. {i+1}, Kota Pelajar"
        fakultas = fakultas_map.get(prodi, 'Lainnya')
        repo.tambah_data_mahasiswa(conn, nim, name, alamat, prodi, fakultas)
        hashed_pw = generate_password_hash(nim, method='pbkdf2:sha256')
        repo.tambah_user(conn, nim, hashed_pw, role='Mahasiswa')
    
    print(f"{len(mhs_names)} Mahasiswa ditambahkan.")

    # 7. Seed Sample KRS & Payment (Ahmad Fauzi - Informatka Sem 1)
    target_nim = "2023100001"
    sample_courses = ['INF101', 'KU101', 'KU102']
    total_sks = 0
    for code in sample_courses:
        repo.tambah_krs(conn, target_nim, code, 1, '2023/2024')
        mk_info = repo.cari_by_kode_matkul(conn, code)
        total_sks += mk_info['sks']
    
    total_bayar = total_sks * 150000
    repo.buat_tagihan(conn, target_nim, 1, '2023/2024', total_sks, total_bayar)
    repo.bayar_tagihan(conn, target_nim, 1, '2023/2024', 'Virtual Account')
    
    print("Sample KRS & Pembayaran ditambahkan.")

    conn.close()
    print("------------------------------------------------")
    print("DATABASE RESET DAN SEEDING SELESAI!")

if __name__ == "__main__":
    reset_and_seed()
