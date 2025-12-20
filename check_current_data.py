import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

# Check distinct prodi
cursor.execute('SELECT DISTINCT prodi FROM tbMatakuliah')
prodis = [r[0] for r in cursor.fetchall()]
print('Program Studi:', prodis)
print()

# Check SKS per prodi per semester
cursor.execute('''
    SELECT prodi, semester, COUNT(*) as jumlah_matkul, SUM(sks) as total_sks 
    FROM tbMatakuliah 
    GROUP BY prodi, semester 
    ORDER BY prodi, semester
''')

print('SKS per Prodi per Semester:')
print('-' * 70)
for r in cursor.fetchall():
    print(f'{r[0]:25} - Semester {r[1]}: {r[2]:2} matkul, Total SKS: {r[3]:2}')

print()
print('=' * 70)

# Check all courses
cursor.execute('SELECT kode_matkul, nama_matkul, sks, semester, prodi FROM tbMatakuliah ORDER BY prodi, semester')
courses = cursor.fetchall()
print(f'\nTotal Mata Kuliah: {len(courses)}')

conn.close()
