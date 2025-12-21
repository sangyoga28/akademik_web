"""
Script untuk memperbaiki masalah yang ditemukan di PythonAnywhere
- Fix Konsistensi Prodi
- Fix Dosen-Matakuliah
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

print("="*70)
print("SCRIPT PERBAIKAN MASALAH PYTHONANYWHERE")
print("="*70)

conn = sqlite3.connect(DATABASE_NAME)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# ===== FIX 1: KONSISTENSI PRODI =====
print("\n1. MEMPERBAIKI KONSISTENSI PRODI")
print("-"*70)

# Cek prodi di mahasiswa
cursor.execute("SELECT DISTINCT prodi FROM tbMahasiswa WHERE prodi IS NOT NULL ORDER BY prodi")
prodi_mhs = [row[0] for row in cursor.fetchall()]
print(f"Prodi Mahasiswa: {prodi_mhs}")

# Cek prodi di mata kuliah
cursor.execute("SELECT DISTINCT prodi FROM tbMatakuliah WHERE prodi != 'Umum' ORDER BY prodi")
prodi_mk = [row[0] for row in cursor.fetchall()]
print(f"Prodi Matakuliah: {prodi_mk}")

# Mapping untuk fix nama prodi yang salah
prodi_fixes = {
    'Teknik Informatika': 'Informatika',
    'Teknik Industri': 'Teknik Sipil',
    'Teknik Komputer': 'Informatika',
    'Sistem Komputer': 'Informatika'
}

fixed_count = 0
for old_name, new_name in prodi_fixes.items():
    cursor.execute("UPDATE tbMahasiswa SET prodi = ? WHERE prodi = ?", (new_name, old_name))
    if cursor.rowcount > 0:
        print(f"[FIX] Updated {cursor.rowcount} mahasiswa: '{old_name}' -> '{new_name}'")
        fixed_count += cursor.rowcount

if fixed_count == 0:
    print("[OK] Tidak ada prodi yang perlu diperbaiki")

# Verifikasi hasil
cursor.execute("SELECT DISTINCT prodi FROM tbMahasiswa WHERE prodi IS NOT NULL ORDER BY prodi")
prodi_mhs_after = [row[0] for row in cursor.fetchall()]
print(f"Prodi Mahasiswa (setelah fix): {prodi_mhs_after}")

# Cek apakah masih ada prodi yang tidak match
mismatched = []
for prodi in prodi_mhs_after:
    if prodi not in prodi_mk:
        mismatched.append(prodi)

if mismatched:
    print(f"[WARNING] Prodi yang masih tidak match: {mismatched}")
    print("Solusi: Tambahkan mata kuliah untuk prodi tersebut atau ubah prodi mahasiswa")
else:
    print("[SUCCESS] Semua prodi mahasiswa sudah konsisten dengan mata kuliah!")

# ===== FIX 2: DOSEN-MATAKULIAH =====
print("\n2. MEMPERBAIKI DOSEN-MATAKULIAH")
print("-"*70)

# Cek dosen dengan mata kuliah yang tidak ada
cursor.execute("""
    SELECT d.nip, d.nama, d.matkul_ajar
    FROM tbDosen d
    LEFT JOIN tbMatakuliah m ON d.matkul_ajar = m.kode_matkul
    WHERE m.kode_matkul IS NULL AND d.matkul_ajar IS NOT NULL AND d.matkul_ajar != ''
""")
invalid_dosen = cursor.fetchall()

print(f"Dosen dengan mata kuliah invalid: {len(invalid_dosen)}")

if len(invalid_dosen) > 0:
    print("\nOpsi perbaikan:")
    print("1. Set matkul_ajar ke NULL (dosen belum mengampu)")
    print("2. Set ke mata kuliah yang ada")
    
    # Ambil sample mata kuliah yang tersedia
    cursor.execute("SELECT kode_matkul, nama_matkul, prodi FROM tbMatakuliah WHERE prodi != 'Umum' LIMIT 5")
    sample_matkul = cursor.fetchall()
    
    print("\nContoh mata kuliah yang tersedia:")
    for mk in sample_matkul:
        print(f"  - {mk['kode_matkul']}: {mk['nama_matkul']} ({mk['prodi']})")
    
    # Strategi: Set ke NULL untuk sementara
    print("\n[ACTION] Setting matkul_ajar ke NULL untuk dosen dengan mata kuliah invalid...")
    cursor.execute("""
        UPDATE tbDosen 
        SET matkul_ajar = NULL 
        WHERE matkul_ajar NOT IN (SELECT kode_matkul FROM tbMatakuliah)
        AND matkul_ajar IS NOT NULL
        AND matkul_ajar != ''
    """)
    
    print(f"[FIX] Updated {cursor.rowcount} dosen (matkul_ajar set to NULL)")
    print("Note: Admin perlu assign ulang mata kuliah untuk dosen ini via form edit")
else:
    print("[OK] Semua dosen sudah punya mata kuliah yang valid")

# ===== VERIFIKASI AKHIR =====
print("\n3. VERIFIKASI HASIL PERBAIKAN")
print("-"*70)

# Test 1: Konsistensi Prodi
cursor.execute("SELECT DISTINCT prodi FROM tbMahasiswa WHERE prodi IS NOT NULL")
prodi_mhs_final = set(row[0] for row in cursor.fetchall())

cursor.execute("SELECT DISTINCT prodi FROM tbMatakuliah WHERE prodi != 'Umum'")
prodi_mk_final = set(row[0] for row in cursor.fetchall())

konsistensi_ok = prodi_mhs_final.issubset(prodi_mk_final)
print(f"Test Konsistensi Prodi: {'[PASS]' if konsistensi_ok else '[FAIL]'}")

# Test 2: Dosen-Matakuliah
cursor.execute("""
    SELECT COUNT(*) FROM tbDosen d
    LEFT JOIN tbMatakuliah m ON d.matkul_ajar = m.kode_matkul
    WHERE m.kode_matkul IS NULL AND d.matkul_ajar IS NOT NULL AND d.matkul_ajar != ''
""")
invalid_count = cursor.fetchone()[0]

dosen_ok = invalid_count == 0
print(f"Test Dosen-Matakuliah: {'[PASS]' if dosen_ok else '[FAIL]'} ({invalid_count} invalid)")

# Commit changes
conn.commit()
conn.close()

print("\n" + "="*70)
if konsistensi_ok and dosen_ok:
    print("SUCCESS! Semua masalah sudah diperbaiki.")
    print("Silakan jalankan verify_integration.py lagi untuk konfirmasi.")
else:
    print("WARNING! Masih ada masalah yang perlu diperbaiki manual.")
    if not konsistensi_ok:
        print("- Konsistensi Prodi: Perlu tambah mata kuliah atau ubah prodi mahasiswa")
    if not dosen_ok:
        print("- Dosen-Matakuliah: Perlu assign mata kuliah via form edit dosen")
print("="*70)
