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
        ("JPN209", "Dasar Etika Budaya Jepang", 2),
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
        ("JPN608", "Keigo (Bahasa Hormat)", 3),
    ],
    7: [
        ("JPN701", "Sastra Jepang Kontemporer", 3),
        ("JPN702", "Bahasa Jepang untuk Media", 3),
        ("JPN703", "Studi Perbandingan Jepang-Indonesia", 3),
        ("JPN704", "Jepang dalam Konteks Global", 3),
        ("JPN705", "Magang", 4),
        ("JPN706", "Kuliah Kerja Nyata", 3),
        ("JPN707", "Proposal Skripsi", 3),
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

# ===== KURIKULUM FAKULTAS TEKNIK =====

MATKUL_INFORMATIKA = {
    1: [
        ("INF101", "Dasar Pemrograman", 3), ("INF102", "Matematika Diskrit", 3),
        ("INF103", "Pengantar Teknologi Informasi", 3), ("INF104", "Logika Informatika", 3),
        ("INF105", "Bahasa Inggris I", 2), ("INF106", "Pendidikan Agama", 2),
        ("INF107", "Pancasila", 2), ("INF108", "Kalkulus I", 3), ("INF109", "Fisika Dasar", 3),
    ],
    2: [
        ("INF201", "Struktur Data", 4), ("INF202", "Algoritma Pemrograman", 4),
        ("INF203", "Arsitektur Komputer", 3), ("INF204", "Aljabar Linear", 3),
        ("INF205", "Kalkulus II", 3), ("INF206", "Bahasa Inggris II", 2),
        ("INF207", "Kewarganegaraan", 2), ("INF208", "Statistika Dasar", 3),
    ],
    3: [
        ("INF301", "Pemrograman Berorientasi Objek", 4), ("INF302", "Basis Data", 4),
        ("INF303", "Sistem Operasi", 3), ("INF304", "Matematika Numerik", 3),
        ("INF305", "Jaringan Komputer Dasar", 3), ("INF306", "Interaksi Manusia dan Komputer", 3),
        ("INF307", "Probabilitas dan Statistika", 2), ("INF308", "Etika Profesi", 2),
    ],
    4: [
        ("INF401", "Pemrograman Web", 4), ("INF402", "Sistem Basis Data Lanjut", 3),
        ("INF403", "Jaringan Komputer Lanjut", 3), ("INF404", "Analisis dan Desain Algoritma", 3),
        ("INF405", "Pemrograman Mobile", 4), ("INF406", "Grafika Komputer", 3),
        ("INF407", "Teori Bahasa dan Automata", 2), ("INF408", "Kewirausahaan", 2),
    ],
    5: [
        ("INF501", "Rekayasa Perangkat Lunak", 4), ("INF502", "Kecerdasan Buatan", 4),
        ("INF503", "Sistem Terdistribusi", 3), ("INF504", "Keamanan Informasi", 3),
        ("INF505", "Pemrograman Framework", 3), ("INF506", "Data Mining", 3),
        ("INF507", "Manajemen Proyek TI", 2), ("INF508", "Bahasa Indonesia", 2),
    ],
    6: [
        ("INF601", "Machine Learning", 4), ("INF602", "Cloud Computing", 3),
        ("INF603", "Internet of Things", 3), ("INF604", "Pengolahan Citra Digital", 3),
        ("INF605", "Sistem Informasi Enterprise", 3), ("INF606", "Pemrograman Game", 3),
        ("INF607", "Metodologi Penelitian", 2), ("INF608", "Komputer dan Masyarakat", 3),
    ],
    7: [
        ("INF701", "Big Data Analytics", 3), ("INF702", "Blockchain Technology", 3),
        ("INF703", "Cyber Security", 3), ("INF704", "DevOps dan CI/CD", 3),
        ("INF705", "Artificial Intelligence Lanjut", 3), ("INF706", "Kerja Praktek", 3),
        ("INF707", "Proposal Skripsi", 3), ("INF708", "Bahasa Indonesia II", 3),
    ],
    8: [("INF801", "Skripsi", 6)]
}

MATKUL_SISTEM_INFORMASI = {
    1: [
        ("SI101", "Pengantar Sistem Informasi", 3), ("SI102", "Dasar Pemrograman", 3),
        ("SI103", "Matematika Bisnis", 3), ("SI104", "Pengantar Manajemen", 3),
        ("SI105", "Pengantar Akuntansi", 3), ("SI106", "Bahasa Inggris I", 2),
        ("SI107", "Pendidikan Agama", 2), ("SI108", "Pancasila", 2), ("SI109", "Statistika Bisnis", 3),
    ],
    2: [
        ("SI201", "Analisis Proses Bisnis", 4), ("SI202", "Basis Data", 4),
        ("SI203", "Pemrograman Berorientasi Objek", 3), ("SI204", "Sistem Operasi", 3),
        ("SI205", "Manajemen Organisasi", 3), ("SI206", "Akuntansi Manajemen", 3),
        ("SI207", "Bahasa Inggris II", 2), ("SI208", "Kewarganegaraan", 2),
    ],
    3: [
        ("SI301", "Manajemen Database", 4), ("SI302", "Analisis dan Desain Sistem", 4),
        ("SI303", "Pemrograman Web", 3), ("SI304", "Jaringan Komputer", 3),
        ("SI305", "Manajemen Pemasaran", 3), ("SI306", "Sistem Informasi Manajemen", 3),
        ("SI307", "Etika Profesi", 2), ("SI308", "Riset Operasi", 2),
    ],
    4: [
        ("SI401", "E-Business", 4), ("SI402", "Desain UI/UX", 3),
        ("SI403", "Pemrograman Mobile", 3), ("SI404", "Manajemen Rantai Pasok", 3),
        ("SI405", "Sistem Informasi Akuntansi", 3), ("SI406", "Manajemen Keuangan", 3),
        ("SI407", "Kewirausahaan", 2), ("SI408", "Komunikasi Bisnis", 3),
    ],
    5: [
        ("SI501", "Manajemen Proyek SI", 4), ("SI502", "Enterprise Resource Planning", 4),
        ("SI503", "Business Intelligence", 3), ("SI504", "Audit Sistem Informasi", 3),
        ("SI505", "CRM Systems", 3), ("SI506", "E-Commerce", 3),
        ("SI507", "Bahasa Indonesia", 2), ("SI508", "Manajemen Strategi", 2),
    ],
    6: [
        ("SI601", "Perencanaan Strategis SI", 4), ("SI602", "Data Warehouse", 3),
        ("SI603", "Tata Kelola TI", 3), ("SI604", "Keamanan Sistem Informasi", 3),
        ("SI605", "Sistem Pendukung Keputusan", 3), ("SI606", "Digital Marketing", 3),
        ("SI607", "Metodologi Penelitian", 2), ("SI608", "Manajemen Risiko TI", 3),
    ],
    7: [
        ("SI701", "Inovasi Sistem Informasi", 3), ("SI702", "Cloud Computing Bisnis", 3),
        ("SI703", "Analytics Big Data", 3), ("SI704", "Proposal Skripsi", 3),
        ("SI705", "Magang", 4), ("SI706", "Kuliah Kerja Nyata", 3),
        ("SI707", "Pilihan I", 3), ("SI708", "Pilihan II", 3),
    ],
    8: [("SI801", "Skripsi", 6)]
}

MATKUL_TEKNIK_ELEKTRO = {
    1: [
        ("TE101", "Rangkaian Listrik I", 3), ("TE102", "Fisika Dasar I", 3),
        ("TE103", "Kalkulus I", 3), ("TE104", "Kimia Dasar", 3),
        ("TE105", "Gambar Teknik", 2), ("TE106", "Pengantar Teknik Elektro", 3),
        ("TE107", "Bahasa Inggris I", 2), ("TE108", "Pendidikan Agama", 2),
        ("TE109", "Pancasila", 2), ("TE110", "Praktikum Fisika Dasar", 1),
    ],
    2: [
        ("TE201", "Rangkaian Listrik II", 3), ("TE202", "Elektronika Dasar", 4),
        ("TE203", "Fisika Dasar II", 3), ("TE204", "Kalkulus II", 3),
        ("TE205", "Pemrograman Komputer", 3), ("TE206", "Matematika Teknik I", 3),
        ("TE207", "Bahasa Inggris II", 2), ("TE208", "Kewarganegaraan", 2),
        ("TE209", "Praktikum Elektronika Dasar", 1),
    ],
    3: [
        ("TE301", "Sistem Digital", 4), ("TE302", "Sinyal dan Sistem", 3),
        ("TE303", "Elektronika Analog", 4), ("TE304", "Matematika Teknik II", 3),
        ("TE305", "Mesin Listrik I", 3), ("TE306", "Pengukuran Listrik", 3),
        ("TE307", "Etika Profesi", 2), ("TE308", "Praktikum Sistem Digital", 2),
    ],
    4: [
        ("TE401", "Medan Elektromagnetik", 3), ("TE402", "Sistem Kendali", 4),
        ("TE403", "Elektronika Daya", 3), ("TE404", "Mesin Listrik II", 3),
        ("TE405", "Mikroprosesor", 4), ("TE406", "Teknik Telekomunikasi", 3),
        ("TE407", "Kewirausahaan", 2), ("TE408", "Praktikum Mikroprosesor", 2),
    ],
    5: [
        ("TE501", "Mikrokontroler", 4), ("TE502", "Sistem Tenaga Listrik", 3),
        ("TE503", "Pengolahan Sinyal Digital", 3), ("TE504", "Sistem Komunikasi", 3),
        ("TE505", "Instrumentasi Industri", 3), ("TE506", "Sistem Embedded", 3),
        ("TE507", "Bahasa Indonesia", 2), ("TE508", "Praktikum Mikrokontroler", 3),
    ],
    6: [
        ("TE601", "Sistem Kendali Digital", 3), ("TE602", "Proteksi Sistem Tenaga", 3),
        ("TE603", "Antena dan Propagasi", 3), ("TE604", "Robotika", 4),
        ("TE605", "PLC dan SCADA", 3), ("TE606", "Energi Terbarukan", 3),
        ("TE607", "Metodologi Penelitian", 2), ("TE608", "Praktikum Robotika", 3),
    ],
    7: [
        ("TE701", "Teknik Tegangan Tinggi", 3), ("TE702", "Sistem Kontrol Cerdas", 3),
        ("TE703", "IoT Systems", 3), ("TE704", "Proposal Skripsi", 3),
        ("TE705", "Magang", 4), ("TE706", "Kuliah Kerja Nyata", 3),
        ("TE707", "Pilihan I", 3), ("TE708", "Pilihan II", 3),
    ],
    8: [("TE801", "Skripsi", 6)]
}

MATKUL_TEKNIK_SIPIL = {
    1: [
        ("SIP101", "Mekanika Fluida", 3), ("SIP102", "Statika", 3),
        ("SIP103", "Gambar Teknik Sipil", 3), ("SIP104", "Matematika Teknik I", 3),
        ("SIP105", "Bahasa Inggris I", 2), ("SIP106", "Pendidikan Agama", 2),
        ("SIP107", "Pancasila", 2), ("SIP108", "Fisika Dasar Sipil", 3), ("SIP109", "Geologi Teknik", 3),
    ],
    2: [
        ("SIP201", "Mekanika Bahan", 4), ("SIP202", "Rekayasa Hidrologi", 3),
        ("SIP203", "Ilmu Ukur Tanah", 3), ("SIP204", "Matematika Teknik II", 3),
        ("SIP205", "Teknologi Bahan Konstruksi", 3), ("SIP206", "Kewarganegaraan", 2),
        ("SIP207", "Bahan Perkerasan Jalan", 3), ("SIP208", "Statistika dan Probabilitas", 3),
    ],
    3: [
        ("SIP301", "Analisa Struktur I", 3), ("SIP302", "Mekanika Tanah I", 3),
        ("SIP303", "Rekayasa Lalu Lintas", 3), ("SIP304", "Hidrolika", 3),
        ("SIP305", "Konstruksi Kayu", 2), ("SIP306", "Pemindahan Tanah Mekanis", 3),
        ("SIP307", "Etika Profesi Sipil", 2), ("SIP308", "Survey Dasar", 2),
    ],
    4: [
        ("SIP401", "Analisa Struktur II", 4), ("SIP402", "Mekanika Tanah II", 3),
        ("SIP403", "Struktur Beton Bertulang I", 3), ("SIP404", "Rekayasa Penyehatan", 3),
        ("SIP405", "Rekayasa Jalan Raya", 3), ("SIP406", "Hukum Pranata Pembangunan", 2),
        ("SIP407", "Kewirausahaan Sipil", 3), ("SIP408", "Irigasi dan Bangunan Air", 3),
    ],
    5: [
        ("SIP501", "Struktur Beton Bertulang II", 3), ("SIP502", "Struktur Baja I", 3),
        ("SIP503", "Rekayasa Pondasi I", 3), ("SIP504", "Metode Numerik Sipil", 3),
        ("SIP505", "Pelabuhan", 3), ("SIP506", "Lapangan Terbang", 3),
        ("SIP507", "Bahasa Indonesia", 2), ("SIP508", "Manajemen Konstruksi I", 3),
    ],
    6: [
        ("SIP601", "Struktur Baja II", 3), ("SIP602", "Rekayasa Pondasi II", 3),
        ("SIP603", "Struktur Kayu Lanjut", 2), ("SIP604", "Drainase Perkotaan", 3),
        ("SIP605", "Metode Pelaksanaan Konstruksi", 3), ("SIP606", "Estimasi Biaya", 3),
        ("SIP607", "Metodologi Penelitian Sipil", 2), ("SIP608", "Analisa Dinamika Struktur", 3),
    ],
    7: [
        ("SIP701", "Jembatan", 3), ("SIP702", "Perencanaan Transportasi", 3),
        ("SIP703", "Ekonomi Teknik", 3), ("SIP704", "Proposal Skripsi", 3),
        ("SIP705", "Magang Proyek", 4), ("SIP706", "Kuliah Kerja Nyata", 3),
        ("SIP707", "Pilihan I", 3), ("SIP708", "Pilihan II", 3),
    ],
    8: [("SIP801", "Skripsi", 6)]
}


# --- [AUTO-PATCH] ENSURE 24 SKS PER SEMESTER ---
ALL_DICTS = [
    ("Manajemen", MATKUL_MANAJEMEN),
    ("Akuntansi", MATKUL_AKUNTANSI),
    ("Sastra Inggris", MATKUL_SASTRA_INGGRIS),
    ("Sastra Jepang", MATKUL_SASTRA_JEPANG),
    ("Ilmu Hukum", MATKUL_ILMU_HUKUM),
    ("Informatika", MATKUL_INFORMATIKA),
    ("Sistem Informasi", MATKUL_SISTEM_INFORMASI),
    ("Teknik Elektro", MATKUL_TEKNIK_ELEKTRO),
    ("Teknik Sipil", MATKUL_TEKNIK_SIPIL)
]

print("Patching SKS requirements (Ensuring >= 24 SKS)...")
for prodi_name, kurikulum in ALL_DICTS:
    for sem in range(1, 8): # Sem 1-7 check
        if sem not in kurikulum: continue
        
        current_sks = sum(m[2] for m in kurikulum[sem])
        if current_sks < 24:
            # print(f"  - Patching {prodi_name} Sem {sem} (Current: {current_sks})")
            while current_sks < 24:
                idx = len([m for m in kurikulum[sem] if "Kapita Selekta" in m[1]]) + 1
                sup_code = f"{prodi_name[:3].upper()}X{sem}{idx}"
                if prodi_name == "Sistem Informasi": sup_code = f"SIX{sem}{idx}"
                sup_name = f"Kapita Selekta {prodi_name} {idx}"
                sup_sks = 3
                
                kurikulum[sem].append((sup_code, sup_name, sup_sks))
                current_sks += sup_sks
                # print(f"    [+] Added {sup_name} (3 SKS)")

print("="*80)
print(" "*20 + "COMPLETE DATABASE SEEDING")
print("="*80)
print("\nScript ini akan menambahkan:")
print("- 4 Fakultas (Teknik, Ekonomi, Sastra, Hukum)")
print("- 9 Prodi (Informatika, SI, Elektro, Sipil, Manajemen, Akuntansi, Inggris, Jepang, Hukum)")
print("- ~500 Mata Kuliah baru")
print("- ~500 Dosen baru")
print("- ~90 Mahasiswa sample")
print("- Assign semua dosen ke mata kuliah (berdasar Nama)")
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

# Fakultas Teknik
PRODI_TEKNIK = [
    ("Informatika", MATKUL_INFORMATIKA),
    ("Sistem Informasi", MATKUL_SISTEM_INFORMASI),
    ("Teknik Elektro", MATKUL_TEKNIK_ELEKTRO),
    ("Teknik Sipil", MATKUL_TEKNIK_SIPIL)
]
for p_name, p_dict in PRODI_TEKNIK:
    print(f"  - {p_name}...", end=" ")
    for sem, mk_list in p_dict.items():
        for kode, nama, sks in mk_list:
            cursor.execute("""
                INSERT OR IGNORE INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi)
                VALUES (?, ?, ?, ?, ?)
            """, (kode, nama, sks, sem, p_name))
            total_mk += 1
    print(f"{sum(len(l) for l in p_dict.values())} mk")

# Hitung berapa dosen yang dibutuhkan
cursor.execute("SELECT COUNT(*) FROM tbMatakuliah")
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
        """, (mk['nama_matkul'], dosen['nip']))
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
    "Ilmu Hukum": "31",
    "Informatika": "41",
    "Sistem Informasi": "42",
    "Teknik Elektro": "43",
    "Teknik Sipil": "44"
}

fakultas_map = {
    "Manajemen": "Fakultas Ekonomi",
    "Akuntansi": "Fakultas Ekonomi",
    "Sastra Inggris": "Fakultas Sastra",
    "Sastra Jepang": "Fakultas Sastra",
    "Ilmu Hukum": "Fakultas Hukum",
    "Informatika": "Fakultas Teknik",
    "Sistem Informasi": "Fakultas Teknik",
    "Teknik Elektro": "Fakultas Teknik",
    "Teknik Sipil": "Fakultas Teknik"
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
    LEFT JOIN tbDosen d ON m.nama_matkul = d.matkul_ajar
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
