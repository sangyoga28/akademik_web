import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

# DATA KURIKULUM (Sample)
# Format: (Kode, Nama, SKS, Semester, Prodi)
KURIKULUM = [
    # --- TEKNIK INFORMATIKA (FT) ---
    # Sem 1
    ("TI101", "Dasar Pemrograman", 3, 1, "Teknik Informatika"),
    ("TI102", "Matematika Diskrit", 3, 1, "Teknik Informatika"),
    ("TI103", "Pengantar TIK", 2, 1, "Teknik Informatika"),
    ("TI104", "Bahasa Inggris 1", 2, 1, "Teknik Informatika"),
    # Sem 2
    ("TI201", "Algoritma & Struktur Data", 4, 2, "Teknik Informatika"),
    ("TI202", "Aljabar Linear", 3, 2, "Teknik Informatika"),
    ("TI203", "Arsitektur Komputer", 3, 2, "Teknik Informatika"),
    # Sem 3
    ("TI301", "Pemrograman Berorientasi Objek", 4, 3, "Teknik Informatika"),
    ("TI302", "Basis Data 1", 3, 3, "Teknik Informatika"),
    ("TI303", "Sistem Operasi", 3, 3, "Teknik Informatika"),
    # Sem 4
    ("TI401", "Pemrograman Web", 4, 4, "Teknik Informatika"),
    ("TI402", "Jaringan Komputer", 3, 4, "Teknik Informatika"),
    ("TI403", "Basis Data 2", 3, 4, "Teknik Informatika"),
    # Sem 5
    ("TI501", "Kecerdasan Buatan", 3, 5, "Teknik Informatika"),
    ("TI502", "Pengembangan Mobile", 4, 5, "Teknik Informatika"),
    ("TI503", "Rekayasa Perangkat Lunak", 3, 5, "Teknik Informatika"),
    # Sem 6-8 (Lanjutan)
    ("TI601", "Data Mining", 3, 6, "Teknik Informatika"),
    ("TI701", "Keamanan Siber", 3, 7, "Teknik Informatika"),
    ("TI801", "Skripsi", 6, 8, "Teknik Informatika"),

    # --- SISTEM INFORMASI (FT) ---
    ("SI101", "Konsep Sistem Informasi", 3, 1, "Sistem Informasi"),
    ("SI102", "Manajemen & Organisasi", 2, 1, "Sistem Informasi"),
    ("SI201", "Analisis Proses Bisnis", 3, 2, "Sistem Informasi"),
    ("SI301", "Desain UI/UX", 3, 3, "Sistem Informasi"),
    ("SI401", "E-Business", 3, 4, "Sistem Informasi"),
    ("SI501", "Manajemen Proyek SI", 3, 5, "Sistem Informasi"),
    
    # --- MANAJEMEN (FE) ---
    ("MN101", "Pengantar Bisnis", 3, 1, "Manajemen"),
    ("MN102", "Pengantar Akuntansi 1", 3, 1, "Manajemen"),
    ("MN201", "Manajemen Pemasaran", 3, 2, "Manajemen"),
    ("MN301", "Manajemen SDM", 3, 3, "Manajemen"),
    ("MN401", "Manajemen Keuangan", 3, 4, "Manajemen"),
    
    # --- AKUNTANSI (FE) ---
    ("AK101", "Pengantar Akuntansi 1", 3, 1, "Akuntansi"),
    ("AK201", "Akuntansi Biaya", 3, 2, "Akuntansi"),
    ("AK301", "Perpajakan 1", 3, 3, "Akuntansi"),
    ("AK401", "Auditing 1", 3, 4, "Akuntansi"),
]

def seed_curriculum():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    print(f"Seeding database at: {DATABASE_NAME}")

    # 1. Hapus Data Lama (Agar tidak duplikat/campur aduk)
    print("Menghapus data mata kuliah lama...")
    cursor.execute("DELETE FROM tbMatakuliah")
    
    # 2. Insert Data Baru
    print("Memasukkan Kurikulum Baru...")
    count = 0
    for mk in KURIKULUM:
        # Kode, Nama, SKS, Semester, Prodi
        try:
            cursor.execute("""
                INSERT INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi) 
                VALUES (?, ?, ?, ?, ?)
            """, (mk[0], mk[1], mk[2], mk[3], mk[4]))
            count += 1
        except sqlite3.IntegrityError:
            print(f"[SKIP] Kode {mk[0]} sudah ada (konflik PK).")

    conn.commit()
    conn.close()
    print(f"Selesai! {count} mata kuliah berhasil ditambahkan.")

if __name__ == "__main__":
    seed_curriculum()
