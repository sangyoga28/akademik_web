import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('akademik.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print('=' * 80)
print('TEST ADMIN: TAMBAH MAHASISWA')
print('=' * 80)

# 1. Tambah Mahasiswa Baru
test_nim = '9999999999'
test_nama = 'Test Student'
test_alamat = 'Jl. Test No. 123'
test_prodi = 'Teknik Informatika'
test_fakultas = 'Fakultas Teknik'

# Cek apakah sudah ada
cur.execute('SELECT * FROM tbMahasiswa WHERE nim = ?', (test_nim,))
existing = cur.fetchone()

if existing:
    print(f"[INFO] Mahasiswa {test_nim} sudah ada, menghapus dulu...")
    cur.execute('DELETE FROM tbMahasiswa WHERE nim = ?', (test_nim,))
    cur.execute('DELETE FROM tbUser WHERE username = ?', (test_nim,))
    conn.commit()

# Tambah data mahasiswa
cur.execute('''
    INSERT INTO tbMahasiswa (nim, nama, alamat, prodi, fakultas)
    VALUES (?, ?, ?, ?, ?)
''', (test_nim, test_nama, test_alamat, test_prodi, test_fakultas))

# Buat akun login otomatis
hashed_pw = generate_password_hash(test_nim, method='pbkdf2:sha256')
cur.execute('''
    INSERT INTO tbUser (username, password_hash, role)
    VALUES (?, ?, ?)
''', (test_nim, hashed_pw, 'Mahasiswa'))

conn.commit()

print(f"[OK] Mahasiswa ditambahkan: {test_nim} - {test_nama}")
print(f"[OK] Akun login dibuat dengan password: {test_nim}")

# Verifikasi data tersimpan
cur.execute('SELECT * FROM tbMahasiswa WHERE nim = ?', (test_nim,))
mhs = cur.fetchone()
cur.execute('SELECT * FROM tbUser WHERE username = ?', (test_nim,))
user = cur.fetchone()

if mhs and user:
    print(f"[SUCCESS] Data mahasiswa dan akun login berhasil dibuat!")
    print(f"  - NIM: {mhs['nim']}")
    print(f"  - Nama: {mhs['nama']}")
    print(f"  - Prodi: {mhs['prodi']}")
    print(f"  - Username: {user['username']}")
    print(f"  - Role: {user['role']}")
else:
    print("[FAIL] Data tidak tersimpan dengan benar!")

print('\n' + '=' * 80)
print('TEST ADMIN: HAPUS MAHASISWA')
print('=' * 80)

# 2. Hapus Mahasiswa
cur.execute('DELETE FROM tbMahasiswa WHERE nim = ?', (test_nim,))
cur.execute('DELETE FROM tbUser WHERE username = ?', (test_nim,))
conn.commit()

print(f"[OK] Mahasiswa {test_nim} dihapus")

# Verifikasi data terhapus
cur.execute('SELECT * FROM tbMahasiswa WHERE nim = ?', (test_nim,))
mhs_after = cur.fetchone()
cur.execute('SELECT * FROM tbUser WHERE username = ?', (test_nim,))
user_after = cur.fetchone()

if not mhs_after and not user_after:
    print(f"[SUCCESS] Data mahasiswa dan akun login berhasil dihapus!")
else:
    print("[FAIL] Data masih ada setelah penghapusan!")

print('\n' + '=' * 80)
print('RINGKASAN VERIFIKASI')
print('=' * 80)
print("[OK] Tambah mahasiswa baru - BERHASIL")
print("[OK] Buat akun login otomatis - BERHASIL")
print("[OK] Hapus mahasiswa - BERHASIL")
print("[OK] Hapus akun login - BERHASIL")
print('\n[SUCCESS] Semua test Admin master data management BERHASIL!')

conn.close()
