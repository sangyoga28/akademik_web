"""
Script untuk assign dosen ke mata kuliah yang masih kosong
"""

import sqlite3
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

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
    nomor = random.randint(100000, 999999)
    return f"{tahun}{nomor:06d}"

print("="*70)
print("ASSIGN DOSEN KE MATA KULIAH YANG KOSONG")
print("="*70)

conn = sqlite3.connect(DATABASE_NAME)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get existing NIPs
cursor.execute("SELECT nip FROM tbDosen")
used_nips = {row[0] for row in cursor.fetchall()}

def get_unique_nip():
    while True:
        nip = generate_nip(random.randint(2015, 2023))
        if nip not in used_nips:
            used_nips.add(nip)
            return nip

# Get mata kuliah tanpa dosen
cursor.execute("""
    SELECT m.kode_matkul, m.nama_matkul, m.prodi, m.semester
    FROM tbMatakuliah m
    LEFT JOIN tbDosen d ON m.kode_matkul = d.matkul_ajar
    WHERE d.nip IS NULL AND m.prodi != 'Umum'
    ORDER BY m.prodi, m.semester
""")
unassigned_mk = cursor.fetchall()

print(f"\nMata kuliah tanpa dosen: {len(unassigned_mk)}")

if len(unassigned_mk) > 0:
    print("\nMembuat dosen baru dan assign...")
    for i, mk in enumerate(unassigned_mk, 1):
        nip = get_unique_nip()
        nama = generate_nama_dosen()
        telepon = f"08{random.randint(1000000000, 9999999999)}"
        
        # Insert dosen
        cursor.execute("""
            INSERT INTO tbDosen (nip, nama, matkul_ajar, telepon)
            VALUES (?, ?, ?, ?)
        """, (nip, nama, mk['kode_matkul'], telepon))
        
        # Create user account
        from werkzeug.security import generate_password_hash
        hashed_pw = generate_password_hash(nip, method='pbkdf2:sha256')
        cursor.execute("""
            INSERT OR IGNORE INTO tbUser (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (nip, hashed_pw, "Dosen"))
        
        print(f"  [{i}/{len(unassigned_mk)}] {mk['kode_matkul']}: {mk['nama_matkul']} -> {nama}")
    
    conn.commit()
    print(f"\n[OK] {len(unassigned_mk)} dosen ditambahkan dan di-assign")
else:
    print("\n[OK] Semua mata kuliah sudah punya dosen!")

# Verifikasi
cursor.execute("""
    SELECT COUNT(*) FROM tbMatakuliah m
    LEFT JOIN tbDosen d ON m.kode_matkul = d.matkul_ajar
    WHERE d.nip IS NULL AND m.prodi != 'Umum'
""")
remaining = cursor.fetchone()[0]

print(f"\nMata kuliah tanpa dosen setelah fix: {remaining}")

conn.close()

print("\n" + "="*70)
print("SELESAI!")
print("="*70)
