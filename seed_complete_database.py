"""
COMPLETE DATABASE SEEDING SCRIPT
Membuat database akademik lengkap dengan 4 fakultas:
1. Fakultas Teknik (existing - akan dilengkapi)
2. Fakultas Ekonomi (new)
3. Fakultas Sastra (new)
4. Fakultas Hukum (new)

Total: 9 Prodi, ~550 Mata Kuliah, ~370 Dosen, ~90 Mahasiswa
"""

import sqlite3
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

# ===== DATA MASTER =====

# Nama dosen Indonesia yang realistis
NAMA_DOSEN_PRIA = [
    "Ahmad", "Budi", "Candra", "Dedi", "Eko", "Fajar", "Gunawan", "Hadi", 
    "Indra", "Joko", "Krisna", "Lukman", "Made", "Nanda", "Oki", "Putra",
    "Rizki", "Surya", "Toni", "Umar", "Vino", "Wawan", "Yudi", "Zaki"
]

NAMA_DOSEN_WANITA = [
    "Ani", "Bella", "Citra", "Dewi", "Eka", "Fitri", "Gita", "Hesti",
    "Indah", "Julia", "Kartika", "Lina", "Maya", "Novi", "Olivia", "Putri",
    "Rina", "Sari", "Tuti", "Umi", "Vina", "Wulan", "Yanti", "Zahra"
]

GELAR_DEPAN = ["Dr.", "Prof. Dr.", "Ir.", "Drs.", "Dra."]
GELAR_BELAKANG = ["M.Kom.", "M.T.", "M.Sc.", "M.Si.", "M.M.", "M.Ak.", "M.Hum.", "M.H.", "S.H.", "S.E.", "S.T.", "S.Kom."]

def generate_nama_dosen():
    """Generate nama dosen yang realistis"""
    is_pria = random.choice([True, False])
    nama_depan = random.choice(NAMA_DOSEN_PRIA if is_pria else NAMA_DOSEN_WANITA)
    nama_belakang = random.choice(NAMA_DOSEN_PRIA + NAMA_DOSEN_WANITA)
    
    gelar_depan = random.choice(GELAR_DEPAN) if random.random() > 0.5 else ""
    gelar_belakang = ", ".join(random.sample(GELAR_BELAKANG, random.randint(1, 2)))
    
    if gelar_depan:
        return f"{gelar_depan} {nama_depan} {nama_belakang}, {gelar_belakang}"
    else:
        return f"{nama_depan} {nama_belakang}, {gelar_belakang}"

def generate_nip(tahun=2020):
    """Generate NIP 10 digit: YYYYNNNNNN"""
    nomor = random.randint(100000, 999999)
    return f"{tahun}{nomor:06d}"

def generate_nim(tahun=2023, prodi_code="01"):
    """Generate NIM 10 digit: YYYYPPNNNN"""
    nomor = random.randint(1000, 9999)
    return f"{tahun}{prodi_code}{nomor:04d}"

# ===== KURIKULUM FAKULTAS EKONOMI =====

MATKUL_MANAJEMEN = {
    1: [
        ("MNJ101", "Pengantar Manajemen", 3),
        ("MNJ102", "Pengantar Bisnis", 3),
        ("MNJ103", "Matematika Bisnis", 3),
        ("MNJ104", "Pengantar Ekonomi Mikro", 3),
        ("MNJ105", "Pengantar Ekonomi Makro", 3),
        ("MNJ106", "Bahasa Inggris Bisnis I", 2),
        ("MNJ107", "Kewarganegaraan", 2),
        ("MNJ108", "Pendidikan Agama", 2),
        ("MNJ109", "Bahasa Indonesia", 2),
    ],
    2: [
        ("MNJ201", "Manajemen Keuangan I", 3),
        ("MNJ202", "Manajemen Pemasaran I", 3),
        ("MNJ203", "Manajemen Operasional", 3),
        ("MNJ204", "Manajemen Sumber Daya Manusia I", 3),
        ("MNJ205", "Statistika Bisnis", 3),
        ("MNJ206", "Akuntansi Manajemen", 3),
        ("MNJ207", "Bahasa Inggris Bisnis II", 2),
        ("MNJ208", "Etika Bisnis", 2),
    ],
    3: [
        ("MNJ301", "Manajemen Strategis", 3),
        ("MNJ302", "Manajemen Keuangan II", 3),
        ("MNJ303", "Manajemen Pemasaran II", 3),
        ("MNJ304", "Manajemen Sumber Daya Manusia II", 3),
        ("MNJ305", "Riset Operasi", 3),
        ("MNJ306", "Sistem Informasi Manajemen", 3),
        ("MNJ307", "Hukum Bisnis", 3),
        ("MNJ308", "Kewirausahaan I", 3),
    ],
    4: [
        ("MNJ401", "Manajemen Produksi", 3),
        ("MNJ402", "Manajemen Risiko", 3),
        ("MNJ403", "Perilaku Konsumen", 3),
        ("MNJ404", "Manajemen Rantai Pasok", 3),
        ("MNJ405", "Analisis Laporan Keuangan", 3),
        ("MNJ406", "Manajemen Perubahan", 3),
        ("MNJ407", "Kewirausahaan II", 3),
        ("MNJ408", "Metodologi Penelitian", 3),
    ],
    5: [
        ("MNJ501", "Manajemen Investasi", 3),
        ("MNJ502", "Manajemen Kualitas", 3),
        ("MNJ503", "Manajemen Proyek", 3),
        ("MNJ504", "Pemasaran Digital", 3),
        ("MNJ505", "Manajemen Internasional", 3),
        ("MNJ506", "Kepemimpinan", 3),
        ("MNJ507", "Negosiasi Bisnis", 3),
        ("MNJ508", "Studi Kelayakan Bisnis", 3),
    ],
    6: [
        ("MNJ601", "Manajemen Retail", 3),
        ("MNJ602", "Manajemen Jasa", 3),
        ("MNJ603", "E-Business", 3),
        ("MNJ604", "Manajemen Inovasi", 3),
        ("MNJ605", "Corporate Social Responsibility", 3),
        ("MNJ606", "Manajemen Pengetahuan", 3),
        ("MNJ607", "Seminar Manajemen", 2),
        ("MNJ608", "Praktikum Manajemen", 4),
    ],
    7: [
        ("MNJ701", "Manajemen Strategis Lanjutan", 3),
        ("MNJ702", "Bisnis Internasional", 3),
        ("MNJ703", "Manajemen Perbankan", 3),
        ("MNJ704", "Manajemen Asuransi", 3),
        ("MNJ705", "Analisis Bisnis", 3),
        ("MNJ706", "Magang", 4),
        ("MNJ707", "Kuliah Kerja Nyata", 3),
        ("MNJ708", "Proposal Skripsi", 2),
    ],
    8: [
        ("MNJ801", "Skripsi", 6),
    ]
}

MATKUL_AKUNTANSI = {
    1: [
        ("AKT101", "Pengantar Akuntansi I", 3),
        ("AKT102", "Pengantar Bisnis", 3),
        ("AKT103", "Matematika Bisnis", 3),
        ("AKT104", "Pengantar Ekonomi Mikro", 3),
        ("AKT105", "Pengantar Ekonomi Makro", 3),
        ("AKT106", "Bahasa Inggris Bisnis I", 2),
        ("AKT107", "Kewarganegaraan", 2),
        ("AKT108", "Pendidikan Agama", 2),
        ("AKT109", "Bahasa Indonesia", 2),
    ],
    2: [
        ("AKT201", "Pengantar Akuntansi II", 3),
        ("AKT202", "Akuntansi Keuangan Menengah I", 3),
        ("AKT203", "Akuntansi Biaya", 3),
        ("AKT204", "Sistem Informasi Akuntansi", 3),
        ("AKT205", "Statistika Bisnis", 3),
        ("AKT206", "Manajemen Keuangan", 3),
        ("AKT207", "Bahasa Inggris Bisnis II", 2),
        ("AKT208", "Hukum Bisnis", 2),
    ],
    3: [
        ("AKT301", "Akuntansi Keuangan Menengah II", 3),
        ("AKT302", "Akuntansi Manajemen", 3),
        ("AKT303", "Perpajakan I", 3),
        ("AKT304", "Auditing I", 3),
        ("AKT305", "Akuntansi Sektor Publik", 3),
        ("AKT306", "Teori Akuntansi", 3),
        ("AKT307", "Akuntansi Perbankan", 3),
        ("AKT308", "Etika Profesi Akuntansi", 3),
    ],
    4: [
        ("AKT401", "Akuntansi Keuangan Lanjutan I", 3),
        ("AKT402", "Perpajakan II", 3),
        ("AKT403", "Auditing II", 3),
        ("AKT404", "Akuntansi Internasional", 3),
        ("AKT405", "Pengauditan Sistem Informasi", 3),
        ("AKT406", "Akuntansi Syariah", 3),
        ("AKT407", "Analisis Laporan Keuangan", 3),
        ("AKT408", "Metodologi Penelitian", 3),
    ],
    5: [
        ("AKT501", "Akuntansi Keuangan Lanjutan II", 3),
        ("AKT502", "Akuntansi Forensik", 3),
        ("AKT503", "Sistem Pengendalian Manajemen", 3),
        ("AKT504", "Akuntansi Lingkungan", 3),
        ("AKT505", "Akuntansi Pemerintahan", 3),
        ("AKT506", "Perencanaan Audit", 3),
        ("AKT507", "Akuntansi Keperilakuan", 3),
        ("AKT508", "Standar Akuntansi Keuangan", 3),
    ],
    6: [
        ("AKT601", "Akuntansi Perpajakan Lanjutan", 3),
        ("AKT602", "Audit Kinerja", 3),
        ("AKT603", "Akuntansi Keuangan Syariah", 3),
        ("AKT604", "Pengauditan Lanjutan", 3),
        ("AKT605", "Akuntansi Manajemen Strategis", 3),
        ("AKT606", "Seminar Akuntansi", 2),
        ("AKT607", "Praktikum Akuntansi", 4),
        ("AKT608", "Lab Komputer Akuntansi", 2),
    ],
    7: [
        ("AKT701", "Akuntansi Kontemporer", 3),
        ("AKT702", "Audit Investigatif", 3),
        ("AKT703", "Akuntansi Asuransi", 3),
        ("AKT704", "Akuntansi Konstruksi", 3),
        ("AKT705", "Magang", 4),
        ("AKT706", "Kuliah Kerja Nyata", 3),
        ("AKT707", "Proposal Skripsi", 2),
        ("AKT708", "Pelaporan Korporat", 2),
    ],
    8: [
        ("AKT801", "Skripsi", 6),
    ]
}

# ===== KURIKULUM FAKULTAS SASTRA =====

MATKUL_SASTRA_INGGRIS = {
    1: [
        ("ING101", "Introduction to Linguistics", 3),
        ("ING102", "Basic English Grammar", 3),
        ("ING103", "Listening and Speaking I", 3),
        ("ING104", "Reading and Writing I", 3),
        ("ING105", "Introduction to Literature", 3),
        ("ING106", "Phonetics and Phonology", 3),
        ("ING107", "Kewarganegaraan", 2),
        ("ING108", "Pendidikan Agama", 2),
        ("ING109", "Bahasa Indonesia", 2),
    ],
    2: [
        ("ING201", "Intermediate English Grammar", 3),
        ("ING202", "Listening and Speaking II", 3),
        ("ING203", "Reading and Writing II", 3),
        ("ING204", "Morphology and Syntax", 3),
        ("ING205", "British Literature I", 3),
        ("ING206", "American Literature I", 3),
        ("ING207", "Introduction to Translation", 3),
        ("ING208", "English for Specific Purposes", 2),
    ],
    3: [
        ("ING301", "Advanced English Grammar", 3),
        ("ING302", "Academic Writing", 3),
        ("ING303", "Semantics and Pragmatics", 3),
        ("ING304", "British Literature II", 3),
        ("ING305", "American Literature II", 3),
        ("ING306", "Translation Theory and Practice", 3),
        ("ING307", "Sociolinguistics", 3),
        ("ING308", "English Teaching Methodology", 3),
    ],
    4: [
        ("ING401", "Discourse Analysis", 3),
        ("ING402", "Psycholinguistics", 3),
        ("ING403", "Literary Criticism", 3),
        ("ING404", "Poetry Analysis", 3),
        ("ING405", "Drama Analysis", 3),
        ("ING406", "Novel Analysis", 3),
        ("ING407", "Interpreting", 3),
        ("ING408", "Research Methodology", 3),
    ],
    5: [
        ("ING501", "Applied Linguistics", 3),
        ("ING502", "Second Language Acquisition", 3),
        ("ING503", "World Literature", 3),
        ("ING504", "Comparative Literature", 3),
        ("ING505", "Creative Writing", 3),
        ("ING506", "English for Business", 3),
        ("ING507", "Film and Literature", 3),
        ("ING508", "Corpus Linguistics", 3),
    ],
    6: [
        ("ING601", "Language Testing and Assessment", 3),
        ("ING602", "Curriculum Development", 3),
        ("ING603", "Postcolonial Literature", 3),
        ("ING604", "Gender Studies in Literature", 3),
        ("ING605", "English for Academic Purposes", 3),
        ("ING606", "Seminar in English Studies", 2),
        ("ING607", "Teaching Practicum", 4),
        ("ING608", "Professional Translation", 2),
    ],
    7: [
        ("ING701", "Contemporary English Literature", 3),
        ("ING702", "Advanced Translation", 3),
        ("ING703", "English for Tourism", 3),
        ("ING704", "Media English", 3),
        ("ING705", "Internship", 4),
        ("ING706", "Community Service", 3),
        ("ING707", "Thesis Proposal", 2),
        ("ING708", "Academic Presentation", 2),
    ],
    8: [
        ("ING801", "Thesis", 6),
    ]
}

MATKUL_SASTRA_JEPANG = {
    1: [
        ("JPN101", "Hiragana dan Katakana", 3),
        ("JPN102", "Tata Bahasa Jepang Dasar I", 3),
        ("JPN103", "Kosakata Jepang Dasar", 3),
        ("JPN104", "Menyimak dan Berbicara I", 3),
        ("JPN105", "Membaca dan Menulis I", 3),
        ("JPN106", "Pengantar Budaya Jepang", 3),
        ("JPN107", "Kewarganegaraan", 2),
        ("JPN108", "Pendidikan Agama", 2),
        ("JPN109", "Bahasa Indonesia", 2),
    ],
    2: [
        ("JPN201", "Kanji Dasar", 3),
        ("JPN202", "Tata Bahasa Jepang Dasar II", 3),
        ("JPN203", "Menyimak dan Berbicara II", 3),
        ("JPN204", "Membaca dan Menulis II", 3),
        ("JPN205", "Kesusastraan Jepang Klasik", 3),
        ("JPN206", "Sejarah Jepang", 3),
        ("JPN207", "Bahasa Inggris", 2),
        ("JPN208", "Pengantar Linguistik", 2),
    ],
    3: [
        ("JPN301", "Kanji Menengah", 3),
        ("JPN302", "Tata Bahasa Jepang Menengah I", 3),
        ("JPN303", "Percakapan Jepang I", 3),
        ("JPN304", "Komposisi Jepang I", 3),
        ("JPN305", "Kesusastraan Jepang Modern", 3),
        ("JPN306", "Masyarakat dan Budaya Jepang", 3),
        ("JPN307", "Pengantar Penerjemahan", 3),
        ("JPN308", "Fonologi Bahasa Jepang", 3),
    ],
    4: [
        ("JPN401", "Kanji Lanjutan", 3),
        ("JPN402", "Tata Bahasa Jepang Menengah II", 3),
        ("JPN403", "Percakapan Jepang II", 3),
        ("JPN404", "Komposisi Jepang II", 3),
        ("JPN405", "Kesusastraan Jepang Kontemporer", 3),
        ("JPN406", "Sintaksis Bahasa Jepang", 3),
        ("JPN407", "Semantik Bahasa Jepang", 3),
        ("JPN408", "Metodologi Penelitian", 3),
    ],
    5: [
        ("JPN501", "Tata Bahasa Jepang Lanjutan", 3),
        ("JPN502", "Bahasa Jepang Bisnis", 3),
        ("JPN503", "Penerjemahan Jepang-Indonesia", 3),
        ("JPN504", "Analisis Wacana Jepang", 3),
        ("JPN505", "Sastra Jepang Periode Meiji", 3),
        ("JPN506", "Manga dan Anime", 3),
        ("JPN507", "Sosiolinguistik Jepang", 3),
        ("JPN508", "Pragmatik Bahasa Jepang", 3),
    ],
    6: [
        ("JPN601", "Bahasa Jepang untuk Pariwisata", 3),
        ("JPN602", "Interpretasi Lisan", 3),
        ("JPN603", "Penerjemahan Lanjutan", 3),
        ("JPN604", "Sastra Jepang Periode Showa", 3),
        ("JPN605", "Budaya Pop Jepang", 3),
        ("JPN606", "Seminar Bahasa dan Sastra Jepang", 2),
        ("JPN607", "Praktikum Bahasa Jepang", 4),
        ("JPN608", "Keigo (Bahasa Hormat)", 2),
    ],
    7: [
        ("JPN701", "Sastra Jepang Kontemporer", 3),
        ("JPN702", "Bahasa Jepang untuk Media", 3),
        ("JPN703", "Studi Perbandingan Jepang-Indonesia", 3),
        ("JPN704", "Jepang dalam Konteks Global", 3),
        ("JPN705", "Magang", 4),
        ("JPN706", "Kuliah Kerja Nyata", 3),
        ("JPN707", "Proposal Skripsi", 2),
        ("JPN708", "Presentasi Akademik", 2),
    ],
    8: [
        ("JPN801", "Skripsi", 6),
    ]
}

# ===== KURIKULUM FAKULTAS HUKUM =====

MATKUL_ILMU_HUKUM = {
    1: [
        ("HKM101", "Pengantar Ilmu Hukum", 3),
        ("HKM102", "Pengantar Hukum Indonesia", 3),
        ("HKM103", "Hukum Tata Negara", 3),
        ("HKM104", "Hukum Perdata", 3),
        ("HKM105", "Hukum Pidana", 3),
        ("HKM106", "Pancasila", 3),
        ("HKM107", "Kewarganegaraan", 2),
        ("HKM108", "Pendidikan Agama", 2),
        ("HKM109", "Bahasa Indonesia", 2),
    ],
    2: [
        ("HKM201", "Hukum Administrasi Negara", 3),
        ("HKM202", "Hukum Perdata (Perikatan)", 3),
        ("HKM203", "Hukum Pidana Khusus", 3),
        ("HKM204", "Hukum Acara Perdata", 3),
        ("HKM205", "Hukum Acara Pidana", 3),
        ("HKM206", "Hukum Islam", 3),
        ("HKM207", "Bahasa Inggris Hukum", 2),
        ("HKM208", "Logika Hukum", 2),
    ],
    3: [
        ("HKM301", "Hukum Dagang", 3),
        ("HKM302", "Hukum Perusahaan", 3),
        ("HKM303", "Hukum Agraria", 3),
        ("HKM304", "Hukum Ketenagakerjaan", 3),
        ("HKM305", "Hukum Lingkungan", 3),
        ("HKM306", "Hukum Internasional", 3),
        ("HKM307", "Hukum Adat", 3),
        ("HKM308", "Sosiologi Hukum", 3),
    ],
    4: [
        ("HKM401", "Hukum Perbankan", 3),
        ("HKM402", "Hukum Pajak", 3),
        ("HKM403", "Hukum Perlindungan Konsumen", 3),
        ("HKM404", "Hukum Hak Asasi Manusia", 3),
        ("HKM405", "Hukum Acara Mahkamah Konstitusi", 3),
        ("HKM406", "Hukum Ekonomi", 3),
        ("HKM407", "Filsafat Hukum", 3),
        ("HKM408", "Metodologi Penelitian Hukum", 3),
    ],
    5: [
        ("HKM501", "Hukum Investasi", 3),
        ("HKM502", "Hukum Kepailitan", 3),
        ("HKM503", "Hukum Persaingan Usaha", 3),
        ("HKM504", "Hukum Telekomunikasi dan Informatika", 3),
        ("HKM505", "Hukum Kekayaan Intelektual", 3),
        ("HKM506", "Hukum Pidana Korupsi", 3),
        ("HKM507", "Hukum Perikatan Internasional", 3),
        ("HKM508", "Viktimologi", 3),
    ],
    6: [
        ("HKM601", "Hukum Asuransi", 3),
        ("HKM602", "Hukum Perburuhan Lanjutan", 3),
        ("HKM603", "Hukum Jaminan", 3),
        ("HKM604", "Hukum Acara Peradilan Tata Usaha Negara", 3),
        ("HKM605", "Hukum Pembuktian", 3),
        ("HKM606", "Seminar Hukum", 2),
        ("HKM607", "Praktikum Peradilan Semu", 4),
        ("HKM608", "Klinik Hukum", 2),
    ],
    7: [
        ("HKM701", "Hukum Kontrak Internasional", 3),
        ("HKM702", "Hukum Arbitrase dan Alternatif Penyelesaian Sengketa", 3),
        ("HKM703", "Hukum Waris", 3),
        ("HKM704", "Kriminologi", 3),
        ("HKM705", "Magang", 4),
        ("HKM706", "Kuliah Kerja Nyata", 3),
        ("HKM707", "Proposal Skripsi", 2),
        ("HKM708", "Legal Drafting", 2),
    ],
    8: [
        ("HKM801", "Skripsi", 6),
    ]
}

print("="*80)
print(" "*20 + "COMPLETE DATABASE SEEDING")
print("="*80)
print("\nScript ini akan menambahkan:")
print("- 3 Fakultas baru (Ekonomi, Sastra, Hukum)")
print("- 5 Prodi baru (Manajemen, Akuntansi, Sastra Inggris, Sastra Jepang, Ilmu Hukum)")
print("- ~300 Mata Kuliah baru")
print("- ~150 Dosen baru")
print("- ~50 Mahasiswa sample")
print("- Assign semua dosen ke mata kuliah")
print("\nProses akan memakan waktu ~2-3 menit...")
print("="*80)

input("\nTekan ENTER untuk melanjutkan...")

conn = sqlite3.connect(DATABASE_NAME)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Track NIP dan NIM yang sudah digunakan
used_nips = set()
used_nims = set()

cursor.execute("SELECT nip FROM tbDosen")
used_nips = {row[0] for row in cursor.fetchall()}

cursor.execute("SELECT nim FROM tbMahasiswa")
used_nims = {row[0] for row in cursor.fetchall()}

def get_unique_nip():
    while True:
        nip = generate_nip(random.randint(2015, 2023))
        if nip not in used_nips:
            used_nips.add(nip)
            return nip

def get_unique_nim(tahun, prodi_code):
    while True:
        nim = generate_nim(tahun, prodi_code)
        if nim not in used_nims:
            used_nims.add(nim)
            return nim

print("\n[1/6] Menambahkan Mata Kuliah...")
total_mk = 0

# Fakultas Ekonomi - Manajemen
print("  - Manajemen...", end=" ")
for sem, matkul_list in MATKUL_MANAJEMEN.items():
    for kode, nama, sks in matkul_list:
        cursor.execute("""
            INSERT OR IGNORE INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi)
            VALUES (?, ?, ?, ?, ?)
        """, (kode, nama, sks, sem, "Manajemen"))
        total_mk += 1
print(f"{len([mk for sem in MATKUL_MANAJEMEN.values() for mk in sem])} mata kuliah")

# Fakultas Ekonomi - Akuntansi
print("  - Akuntansi...", end=" ")
for sem, matkul_list in MATKUL_AKUNTANSI.items():
    for kode, nama, sks in matkul_list:
        cursor.execute("""
            INSERT OR IGNORE INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi)
            VALUES (?, ?, ?, ?, ?)
        """, (kode, nama, sks, sem, "Akuntansi"))
        total_mk += 1
print(f"{len([mk for sem in MATKUL_AKUNTANSI.values() for mk in sem])} mata kuliah")

# Fakultas Sastra - Sastra Inggris
print("  - Sastra Inggris...", end=" ")
for sem, matkul_list in MATKUL_SASTRA_INGGRIS.items():
    for kode, nama, sks in matkul_list:
        cursor.execute("""
            INSERT OR IGNORE INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi)
            VALUES (?, ?, ?, ?, ?)
        """, (kode, nama, sks, sem, "Sastra Inggris"))
        total_mk += 1
print(f"{len([mk for sem in MATKUL_SASTRA_INGGRIS.values() for mk in sem])} mata kuliah")

# Fakultas Sastra - Sastra Jepang
print("  - Sastra Jepang...", end=" ")
for sem, matkul_list in MATKUL_SASTRA_JEPANG.items():
    for kode, nama, sks in matkul_list:
        cursor.execute("""
            INSERT OR IGNORE INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi)
            VALUES (?, ?, ?, ?, ?)
        """, (kode, nama, sks, sem, "Sastra Jepang"))
        total_mk += 1
print(f"{len([mk for sem in MATKUL_SASTRA_JEPANG.values() for mk in sem])} mata kuliah")

# Fakultas Hukum - Ilmu Hukum
print("  - Ilmu Hukum...", end=" ")
for sem, matkul_list in MATKUL_ILMU_HUKUM.items():
    for kode, nama, sks in matkul_list:
        cursor.execute("""
            INSERT OR IGNORE INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi)
            VALUES (?, ?, ?, ?, ?)
        """, (kode, nama, sks, sem, "Ilmu Hukum"))
        total_mk += 1
print(f"{len([mk for sem in MATKUL_ILMU_HUKUM.values() for mk in sem])} mata kuliah")

conn.commit()
print(f"  Total: {total_mk} mata kuliah ditambahkan")

print("\n[2/6] Menambahkan Dosen Baru...")

# Hitung berapa dosen yang dibutuhkan untuk mata kuliah baru
cursor.execute("SELECT COUNT(*) FROM tbMatakuliah WHERE prodi IN ('Manajemen', 'Akuntansi', 'Sastra Inggris', 'Sastra Jepang', 'Ilmu Hukum')")
mk_baru_count = cursor.fetchone()[0]

dosen_needed = mk_baru_count  # 1 dosen per mata kuliah
print(f"  Membuat {dosen_needed} dosen baru...")

for i in range(dosen_needed):
    nip = get_unique_nip()
    nama = generate_nama_dosen()
    telepon = f"08{random.randint(1000000000, 9999999999)}"
    
    cursor.execute("""
        INSERT INTO tbDosen (nip, nama, matkul_ajar, telepon)
        VALUES (?, ?, NULL, ?)
    """, (nip, nama, telepon))
    
    if (i + 1) % 50 == 0:
        print(f"    {i + 1}/{dosen_needed} dosen dibuat...")

conn.commit()
print(f"  Total: {dosen_needed} dosen ditambahkan")

print("\n[3/6] Assign Dosen ke Mata Kuliah...")

# Get all mata kuliah tanpa dosen
cursor.execute("""
    SELECT kode_matkul, nama_matkul, prodi 
    FROM tbMatakuliah 
    WHERE kode_matkul NOT IN (SELECT COALESCE(matkul_ajar, '') FROM tbDosen WHERE matkul_ajar IS NOT NULL)
    ORDER BY prodi, kode_matkul
""")
unassigned_mk = cursor.fetchall()

# Get dosen tanpa mata kuliah
cursor.execute("""
    SELECT nip, nama 
    FROM tbDosen 
    WHERE matkul_ajar IS NULL 
    ORDER BY nip
""")
available_dosen = cursor.fetchall()

print(f"  Mata kuliah tanpa dosen: {len(unassigned_mk)}")
print(f"  Dosen tersedia: {len(available_dosen)}")

assigned_count = 0
for i, mk in enumerate(unassigned_mk):
    if i < len(available_dosen):
        dosen = available_dosen[i]
        cursor.execute("""
            UPDATE tbDosen 
            SET matkul_ajar = ? 
            WHERE nip = ?
        """, (mk['kode_matkul'], dosen['nip']))
        assigned_count += 1
        
        if (assigned_count) % 50 == 0:
            print(f"    {assigned_count}/{len(unassigned_mk)} assigned...")

conn.commit()
print(f"  Total: {assigned_count} dosen di-assign ke mata kuliah")

print("\n[4/6] Menambahkan Mahasiswa Sample...")

prodi_codes = {
    "Manajemen": "11",
    "Akuntansi": "12",
    "Sastra Inggris": "21",
    "Sastra Jepang": "22",
    "Ilmu Hukum": "31"
}

fakultas_map = {
    "Manajemen": "Fakultas Ekonomi",
    "Akuntansi": "Fakultas Ekonomi",
    "Sastra Inggris": "Fakultas Sastra",
    "Sastra Jepang": "Fakultas Sastra",
    "Ilmu Hukum": "Fakultas Hukum"
}

total_mhs = 0
for prodi, code in prodi_codes.items():
    print(f"  - {prodi}...", end=" ")
    for i in range(10):  # 10 mahasiswa per prodi
        nim = get_unique_nim(2023, code)
        nama_depan = random.choice(NAMA_DOSEN_PRIA + NAMA_DOSEN_WANITA)
        nama_belakang = random.choice(NAMA_DOSEN_PRIA + NAMA_DOSEN_WANITA)
        nama = f"{nama_depan} {nama_belakang}"
        alamat = f"Jl. {random.choice(['Merdeka', 'Sudirman', 'Gatot Subroto', 'Ahmad Yani', 'Diponegoro'])} No. {random.randint(1, 100)}"
        
        cursor.execute("""
            INSERT INTO tbMahasiswa (nim, nama, alamat, prodi, fakultas)
            VALUES (?, ?, ?, ?, ?)
        """, (nim, nama, alamat, prodi, fakultas_map[prodi]))
        
        # Buat user account
        from werkzeug.security import generate_password_hash
        hashed_pw = generate_password_hash(nim, method='pbkdf2:sha256')
        cursor.execute("""
            INSERT OR IGNORE INTO tbUser (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (nim, hashed_pw, "Mahasiswa"))
        
        total_mhs += 1
    print(f"10 mahasiswa")

conn.commit()
print(f"  Total: {total_mhs} mahasiswa ditambahkan")

print("\n[5/6] Update Fakultas Mahasiswa Existing...")
cursor.execute("""
    UPDATE tbMahasiswa 
    SET fakultas = 'Fakultas Teknik' 
    WHERE prodi IN ('Informatika', 'Sistem Informasi', 'Teknik Elektro', 'Teknik Sipil')
""")
conn.commit()
print(f"  {cursor.rowcount} mahasiswa diupdate")

print("\n[6/6] Verifikasi Final...")

# Cek total per fakultas
cursor.execute("SELECT DISTINCT fakultas FROM tbMahasiswa ORDER BY fakultas")
fakultas_final = [row[0] for row in cursor.fetchall()]
print(f"  Fakultas: {len(fakultas_final)}")
for fak in fakultas_final:
    cursor.execute("SELECT COUNT(*) FROM tbMahasiswa WHERE fakultas = ?", (fak,))
    count = cursor.fetchone()[0]
    print(f"    - {fak}: {count} mahasiswa")

# Cek total prodi
cursor.execute("SELECT DISTINCT prodi FROM tbMatakuliah WHERE prodi != 'Umum' ORDER BY prodi")
prodi_final = [row[0] for row in cursor.fetchall()]
print(f"\n  Prodi: {len(prodi_final)}")
for prodi in prodi_final:
    cursor.execute("SELECT COUNT(*) FROM tbMatakuliah WHERE prodi = ?", (prodi,))
    count = cursor.fetchone()[0]
    print(f"    - {prodi}: {count} mata kuliah")

# Cek dosen assignment
cursor.execute("SELECT COUNT(*) FROM tbDosen WHERE matkul_ajar IS NOT NULL")
assigned_dosen = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM tbDosen")
total_dosen = cursor.fetchone()[0]
print(f"\n  Dosen: {total_dosen} total, {assigned_dosen} mengajar")

# Cek mata kuliah tanpa dosen
cursor.execute("""
    SELECT COUNT(*) FROM tbMatakuliah m
    LEFT JOIN tbDosen d ON m.kode_matkul = d.matkul_ajar
    WHERE d.nip IS NULL AND m.prodi != 'Umum'
""")
mk_no_dosen = cursor.fetchone()[0]
print(f"  Mata kuliah tanpa dosen: {mk_no_dosen}")

conn.close()

print("\n" + "="*80)
print("SEEDING SELESAI!")
print("="*80)
print("\nDatabase sekarang memiliki:")
print(f"- {len(fakultas_final)} Fakultas")
print(f"- {len(prodi_final)} Prodi")
print(f"- {sum([cursor.execute('SELECT COUNT(*) FROM tbMatakuliah WHERE prodi = ?', (p,)).fetchone()[0] for p in prodi_final])} Mata Kuliah (excluding Umum)")
print(f"- {total_dosen} Dosen")
print(f"- Mahasiswa di semua prodi")
print("\nJalankan verify_integration.py untuk verifikasi lengkap!")
print("="*80)
