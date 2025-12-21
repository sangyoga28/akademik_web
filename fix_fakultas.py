"""
Script untuk memperbaiki fakultas mahasiswa
Saat ini hanya ada 2 fakultas: Teknik, Teknik & Ilmu Komputer
Perlu diperbaiki menjadi 4 fakultas sesuai prodi
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

print("="*70)
print("FIX FAKULTAS MAHASISWA")
print("="*70)

conn = sqlite3.connect(DATABASE_NAME)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Cek fakultas saat ini
cursor.execute("SELECT DISTINCT fakultas FROM tbMahasiswa WHERE fakultas IS NOT NULL ORDER BY fakultas")
fakultas_before = [row[0] for row in cursor.fetchall()]
print(f"\nFakultas sebelum fix: {fakultas_before}")

# Mapping prodi ke fakultas yang benar
prodi_to_fakultas = {
    'Informatika': 'Fakultas Teknik',
    'Sistem Informasi': 'Fakultas Teknik',
    'Teknik Elektro': 'Fakultas Teknik',
    'Teknik Sipil': 'Fakultas Teknik'
}

print("\nMapping prodi ke fakultas:")
for prodi, fakultas in prodi_to_fakultas.items():
    print(f"  {prodi} -> {fakultas}")

# Update fakultas berdasarkan prodi
print("\nUpdating fakultas...")
for prodi, fakultas in prodi_to_fakultas.items():
    cursor.execute("UPDATE tbMahasiswa SET fakultas = ? WHERE prodi = ?", (fakultas, prodi))
    if cursor.rowcount > 0:
        print(f"  [OK] Updated {cursor.rowcount} mahasiswa {prodi} -> {fakultas}")

conn.commit()

# Verifikasi hasil
cursor.execute("SELECT DISTINCT fakultas FROM tbMahasiswa WHERE fakultas IS NOT NULL ORDER BY fakultas")
fakultas_after = [row[0] for row in cursor.fetchall()]
print(f"\nFakultas setelah fix: {fakultas_after}")

# Cek distribusi per fakultas
print("\nDistribusi mahasiswa per fakultas:")
cursor.execute("""
    SELECT fakultas, COUNT(*) as jumlah 
    FROM tbMahasiswa 
    WHERE fakultas IS NOT NULL 
    GROUP BY fakultas 
    ORDER BY fakultas
""")
for row in cursor.fetchall():
    print(f"  {row['fakultas']}: {row['jumlah']} mahasiswa")

conn.close()

print("\n" + "="*70)
print("SELESAI!")
print("="*70)
