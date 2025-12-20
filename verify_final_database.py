import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

print("=" * 70)
print("FINAL DATABASE VERIFICATION")
print("=" * 70)

# 1. Program Studi Overview
cursor.execute('SELECT DISTINCT prodi FROM tbMatakuliah ORDER BY prodi')
prodis = [r[0] for r in cursor.fetchall()]
print(f'\nProgram Studi: {prodis}')

# 2. SKS Distribution per Prodi
print('\n' + '=' * 70)
print('SKS DISTRIBUTION PER PROGRAM STUDI')
print('=' * 70)
cursor.execute('''
    SELECT prodi, semester, COUNT(*) as jumlah_matkul, SUM(sks) as total_sks 
    FROM tbMatakuliah 
    WHERE prodi IN ('Informatika', 'Sistem Informasi', 'Teknik Elektro', 'Teknik Sipil')
    GROUP BY prodi, semester 
    ORDER BY prodi, semester
''')

for r in cursor.fetchall():
    status = "[OK]" if r[3] >= 24 or r[1] == 8 else "[!!]"
    print(f'{status} {r[0]:25} Sem {r[1]}: {r[2]:2} courses, {r[3]:2} SKS')

# 3. Statistics
print('\n' + '=' * 70)
print('DATABASE STATISTICS')
print('=' * 70)

cursor.execute('SELECT COUNT(*) FROM tbMatakuliah')
total_courses = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM tbDosen')
total_lecturers = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM tbMahasiswa')
total_students = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM tbUser')
total_users = cursor.fetchone()[0]

print(f'Total Courses:    {total_courses}')
print(f'Total Lecturers:  {total_lecturers}')
print(f'Total Students:   {total_students}')
print(f'Total Users:      {total_users}')

# 4. Students per Prodi
print('\n' + '=' * 70)
print('STUDENTS PER PROGRAM STUDI')
print('=' * 70)
cursor.execute('''
    SELECT prodi, COUNT(*) as jumlah_mahasiswa
    FROM tbMahasiswa
    GROUP BY prodi
    ORDER BY prodi
''')

for r in cursor.fetchall():
    print(f'{r[0]:25}: {r[1]:3} students')

conn.close()

print('\n' + '=' * 70)
print('VERIFICATION COMPLETE')
print('=' * 70)
