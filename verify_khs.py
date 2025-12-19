import sqlite3

conn = sqlite3.connect('akademik.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Query KHS data untuk mahasiswa 2023100001
cur.execute('''
    SELECT k.id, m.nim, m.nama, mk.nama_matkul, k.nilai_angka, k.nilai_huruf 
    FROM tbKRS k 
    JOIN tbMahasiswa m ON k.nim = m.nim 
    JOIN tbMatakuliah mk ON k.kode_matkul = mk.kode_matkul 
    WHERE m.nim = "2023100001" 
    AND k.semester = 1 
    AND k.tahun_ajaran = "2023/2024"
''')

rows = cur.fetchall()

print('=' * 80)
print('KHS Data untuk Mahasiswa 2023100001 (Ahmad Fauzi)')
print('Semester 1, Tahun Ajaran 2023/2024')
print('=' * 80)

if rows:
    for row in rows:
        print(f"Mata Kuliah: {row['nama_matkul']}")
        print(f"  Nilai Angka: {row['nilai_angka']}")
        print(f"  Nilai Huruf: {row['nilai_huruf']}")
        print('-' * 80)
    print(f"\nTotal Mata Kuliah: {len(rows)}")
else:
    print("Tidak ada data KHS ditemukan.")

print('\n' + '=' * 80)
print('Verifikasi Khusus: Dasar Pemrograman')
print('=' * 80)

cur.execute('''
    SELECT mk.nama_matkul, k.nilai_angka, k.nilai_huruf 
    FROM tbKRS k 
    JOIN tbMatakuliah mk ON k.kode_matkul = mk.kode_matkul 
    WHERE k.nim = "2023100001" 
    AND mk.nama_matkul = "Dasar Pemrograman"
    AND k.semester = 1 
    AND k.tahun_ajaran = "2023/2024"
''')

dp_row = cur.fetchone()
if dp_row:
    print(f"[OK] Mata Kuliah: {dp_row['nama_matkul']}")
    print(f"[OK] Nilai Angka: {dp_row['nilai_angka']}")
    print(f"[OK] Nilai Huruf: {dp_row['nilai_huruf']}")
    
    if dp_row['nilai_angka'] == 85.0 and dp_row['nilai_huruf'] == 'A':
        print("\n[SUCCESS] VERIFIKASI BERHASIL! Nilai 85 (A) tersimpan dengan benar!")
    else:
        print(f"\n[FAIL] VERIFIKASI GAGAL! Expected: 85 (A), Got: {dp_row['nilai_angka']} ({dp_row['nilai_huruf']})")
else:
    print("[FAIL] Data Dasar Pemrograman tidak ditemukan!")

conn.close()
