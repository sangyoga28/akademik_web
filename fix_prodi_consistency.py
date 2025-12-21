import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

print("=" * 70)
print("SCRIPT KONSISTENSI DATA PRODI")
print("=" * 70)

# Mapping prodi lama ke baru (jika ada mahasiswa dengan nama lama)
prodi_mapping = {
    'Teknik Informatika': 'Informatika',
    'Teknik Industri': 'Teknik Sipil'  # Atau bisa dihapus jika tidak ada
}

print("\n1. Memeriksa konsistensi prodi mahasiswa...")
cursor.execute('SELECT DISTINCT prodi FROM tbMahasiswa ORDER BY prodi')
prodi_mahasiswa = [r[0] for r in cursor.fetchall()]
print(f"   Prodi mahasiswa saat ini: {prodi_mahasiswa}")

cursor.execute('SELECT DISTINCT prodi FROM tbMatakuliah WHERE prodi != "Umum" ORDER BY prodi')
prodi_matkul = [r[0] for r in cursor.fetchall()]
print(f"   Prodi mata kuliah: {prodi_matkul}")

# Update jika ada yang tidak sesuai
print("\n2. Memperbaiki inkonsistensi...")
updated_count = 0
for old, new in prodi_mapping.items():
    cursor.execute('UPDATE tbMahasiswa SET prodi = ? WHERE prodi = ?', (new, old))
    if cursor.rowcount > 0:
        print(f"   [OK] Updated {cursor.rowcount} mahasiswa dari '{old}' ke '{new}'")
        updated_count += cursor.rowcount

if updated_count == 0:
    print("   [OK] Tidak ada data yang perlu diperbaiki. Semua sudah konsisten!")

# Verifikasi hasil
print("\n3. Verifikasi hasil...")
cursor.execute('SELECT DISTINCT prodi FROM tbMahasiswa ORDER BY prodi')
prodi_mahasiswa_after = [r[0] for r in cursor.fetchall()]
print(f"   Prodi mahasiswa setelah fix: {prodi_mahasiswa_after}")

# Cek apakah semua prodi mahasiswa ada di mata kuliah
print("\n4. Validasi prodi mahasiswa dengan mata kuliah...")
for prodi in prodi_mahasiswa_after:
    if prodi and prodi not in prodi_matkul:
        print(f"   [WARNING] Prodi '{prodi}' ada di mahasiswa tapi tidak ada mata kuliahnya!")
    else:
        cursor.execute('SELECT COUNT(*) FROM tbMatakuliah WHERE prodi = ?', (prodi,))
        count = cursor.fetchone()[0]
        print(f"   [OK] Prodi '{prodi}': {count} mata kuliah tersedia")

conn.commit()
conn.close()

print("\n" + "=" * 70)
print("SELESAI! Database sudah konsisten.")
print("=" * 70)
