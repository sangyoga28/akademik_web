"""
Script untuk menangani mahasiswa dengan prodi yang tidak punya mata kuliah
Khususnya untuk prodi 'Ilmu Hukum'
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

print("="*70)
print("FIX MAHASISWA DENGAN PRODI ILMU HUKUM")
print("="*70)

conn = sqlite3.connect(DATABASE_NAME)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Cek mahasiswa dengan prodi Ilmu Hukum
cursor.execute("""
    SELECT nim, nama, prodi, fakultas 
    FROM tbMahasiswa 
    WHERE prodi = 'Ilmu Hukum'
""")
ilmu_hukum_mhs = cursor.fetchall()

print(f"\nDitemukan {len(ilmu_hukum_mhs)} mahasiswa dengan prodi Ilmu Hukum:")
for mhs in ilmu_hukum_mhs:
    print(f"  - {mhs['nim']}: {mhs['nama']} ({mhs['fakultas']})")

if len(ilmu_hukum_mhs) > 0:
    print("\nOpsi perbaikan:")
    print("1. Hapus mahasiswa Ilmu Hukum (karena tidak ada mata kuliahnya)")
    print("2. Pindahkan ke prodi lain yang ada mata kuliahnya")
    print("3. Tambahkan mata kuliah Ilmu Hukum ke database")
    
    print("\n[PILIHAN] Menghapus mahasiswa Ilmu Hukum...")
    print("Alasan: Prodi Ilmu Hukum tidak punya mata kuliah di database")
    
    # Hapus user account terlebih dahulu
    for mhs in ilmu_hukum_mhs:
        cursor.execute("DELETE FROM tbUser WHERE username = ?", (mhs['nim'],))
        print(f"  - Deleted user account: {mhs['nim']}")
    
    # Hapus mahasiswa
    cursor.execute("DELETE FROM tbMahasiswa WHERE prodi = 'Ilmu Hukum'")
    deleted_count = cursor.rowcount
    print(f"\n[FIX] Deleted {deleted_count} mahasiswa dengan prodi Ilmu Hukum")
    
    conn.commit()
    
    # Verifikasi
    cursor.execute("SELECT DISTINCT prodi FROM tbMahasiswa ORDER BY prodi")
    prodi_after = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT prodi FROM tbMatakuliah WHERE prodi != 'Umum' ORDER BY prodi")
    prodi_mk = [row[0] for row in cursor.fetchall()]
    
    print("\nVerifikasi hasil:")
    print(f"Prodi Mahasiswa: {prodi_after}")
    print(f"Prodi Matakuliah: {prodi_mk}")
    
    if set(prodi_after).issubset(set(prodi_mk)):
        print("\n[SUCCESS] Semua prodi mahasiswa sekarang konsisten dengan mata kuliah!")
    else:
        mismatched = set(prodi_after) - set(prodi_mk)
        print(f"\n[WARNING] Masih ada prodi yang tidak match: {list(mismatched)}")
else:
    print("\n[OK] Tidak ada mahasiswa dengan prodi Ilmu Hukum")

conn.close()

print("\n" + "="*70)
print("SELESAI!")
print("="*70)
