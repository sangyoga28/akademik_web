"""
Script untuk audit lengkap database akademik
Cek: Fakultas, Prodi, Mata Kuliah, Dosen, Format Data
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

print("="*80)
print(" "*25 + "AUDIT DATABASE AKADEMIK")
print("="*80)

conn = sqlite3.connect(DATABASE_NAME)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# ===== 1. AUDIT FAKULTAS & PRODI =====
print("\n1. FAKULTAS & PRODI")
print("-"*80)

cursor.execute("SELECT DISTINCT fakultas FROM tbMahasiswa WHERE fakultas IS NOT NULL ORDER BY fakultas")
fakultas_list = [row[0] for row in cursor.fetchall()]
print(f"Fakultas yang ada: {len(fakultas_list)}")
for fak in fakultas_list:
    print(f"  - {fak}")

cursor.execute("SELECT DISTINCT prodi FROM tbMatakuliah WHERE prodi != 'Umum' ORDER BY prodi")
prodi_list = [row[0] for row in cursor.fetchall()]
print(f"\nProdi yang punya mata kuliah: {len(prodi_list)}")
for prodi in prodi_list:
    cursor.execute("SELECT COUNT(*) FROM tbMatakuliah WHERE prodi = ?", (prodi,))
    count = cursor.fetchone()[0]
    print(f"  - {prodi}: {count} mata kuliah")

# ===== 2. AUDIT SKS PER SEMESTER =====
print("\n2. SKS PER SEMESTER (Minimal 24 SKS)")
print("-"*80)

for prodi in prodi_list:
    print(f"\n{prodi}:")
    for sem in range(1, 9):
        cursor.execute("""
            SELECT SUM(sks) FROM tbMatakuliah 
            WHERE (prodi = ? OR prodi = 'Umum') AND semester = ?
        """, (prodi, sem))
        total_sks = cursor.fetchone()[0] or 0
        status = "OK" if total_sks >= 24 else "KURANG"
        print(f"  Semester {sem}: {total_sks} SKS [{status}]")

# ===== 3. AUDIT DOSEN =====
print("\n3. DOSEN & MATA KULIAH")
print("-"*80)

cursor.execute("SELECT COUNT(*) FROM tbDosen")
total_dosen = cursor.fetchone()[0]
print(f"Total dosen: {total_dosen}")

cursor.execute("""
    SELECT COUNT(*) FROM tbDosen 
    WHERE matkul_ajar IS NOT NULL AND matkul_ajar != ''
""")
dosen_with_matkul = cursor.fetchone()[0]
print(f"Dosen yang mengajar: {dosen_with_matkul}")
print(f"Dosen tanpa mata kuliah: {total_dosen - dosen_with_matkul}")

# Cek mata kuliah tanpa dosen
cursor.execute("""
    SELECT m.kode_matkul, m.nama_matkul, m.prodi, m.semester
    FROM tbMatakuliah m
    LEFT JOIN tbDosen d ON m.kode_matkul = d.matkul_ajar
    WHERE d.nip IS NULL AND m.prodi != 'Umum'
""")
matkul_no_dosen = cursor.fetchall()
print(f"\nMata kuliah tanpa dosen: {len(matkul_no_dosen)}")
if len(matkul_no_dosen) > 0 and len(matkul_no_dosen) <= 10:
    for mk in matkul_no_dosen:
        print(f"  - {mk['kode_matkul']}: {mk['nama_matkul']} ({mk['prodi']} Sem {mk['semester']})")

# ===== 4. AUDIT FORMAT DATA =====
print("\n4. FORMAT DATA")
print("-"*80)

# Cek NIM format
cursor.execute("SELECT nim, nama FROM tbMahasiswa WHERE LENGTH(nim) != 10")
invalid_nim = cursor.fetchall()
print(f"Mahasiswa dengan NIM bukan 10 digit: {len(invalid_nim)}")
if len(invalid_nim) > 0 and len(invalid_nim) <= 5:
    for mhs in invalid_nim:
        print(f"  - {mhs['nim']} ({len(mhs['nim'])} digit): {mhs['nama']}")

# Cek NIP format
cursor.execute("SELECT nip, nama FROM tbDosen WHERE LENGTH(nip) != 10")
invalid_nip = cursor.fetchall()
print(f"Dosen dengan NIP bukan 10 digit: {len(invalid_nip)}")
if len(invalid_nip) > 0 and len(invalid_nip) <= 5:
    for dsn in invalid_nip:
        print(f"  - {dsn['nip']} ({len(dsn['nip'])} digit): {dsn['nama']}")

# Cek kode mata kuliah format
cursor.execute("SELECT kode_matkul, nama_matkul FROM tbMatakuliah WHERE LENGTH(kode_matkul) < 5")
invalid_kode = cursor.fetchall()
print(f"Mata kuliah dengan kode tidak standar: {len(invalid_kode)}")

# ===== 5. AUDIT DUPLIKAT =====
print("\n5. DUPLIKAT DATA")
print("-"*80)

# Cek duplikat mahasiswa
cursor.execute("""
    SELECT nim, COUNT(*) as count 
    FROM tbMahasiswa 
    GROUP BY nim 
    HAVING count > 1
""")
dup_mhs = cursor.fetchall()
print(f"Mahasiswa duplikat: {len(dup_mhs)}")

# Cek duplikat dosen
cursor.execute("""
    SELECT nip, COUNT(*) as count 
    FROM tbDosen 
    GROUP BY nip 
    HAVING count > 1
""")
dup_dsn = cursor.fetchall()
print(f"Dosen duplikat: {len(dup_dsn)}")

# Cek duplikat mata kuliah
cursor.execute("""
    SELECT kode_matkul, COUNT(*) as count 
    FROM tbMatakuliah 
    GROUP BY kode_matkul 
    HAVING count > 1
""")
dup_mk = cursor.fetchall()
print(f"Mata kuliah duplikat: {len(dup_mk)}")

# ===== 6. SUMMARY =====
print("\n" + "="*80)
print("SUMMARY AUDIT")
print("="*80)

issues = []

if len(fakultas_list) < 4:
    issues.append(f"Fakultas kurang (ada {len(fakultas_list)}, seharusnya 4)")

if len(prodi_list) < 4:
    issues.append(f"Prodi kurang (ada {len(prodi_list)}, seharusnya minimal 4)")

if len(matkul_no_dosen) > 0:
    issues.append(f"{len(matkul_no_dosen)} mata kuliah tanpa dosen")

if len(invalid_nim) > 0:
    issues.append(f"{len(invalid_nim)} mahasiswa dengan NIM invalid")

if len(invalid_nip) > 0:
    issues.append(f"{len(invalid_nip)} dosen dengan NIP invalid")

if len(dup_mhs) > 0 or len(dup_dsn) > 0 or len(dup_mk) > 0:
    issues.append("Ada data duplikat")

if len(issues) == 0:
    print("[OK] Tidak ada masalah ditemukan!")
else:
    print(f"[WARNING] Ditemukan {len(issues)} masalah:")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")

print("\n" + "="*80)

conn.close()
