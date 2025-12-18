# File: repository.py (VERSI LENGKAP & FINAL)

import sqlite3
import os
from flask import g

# Gunakan absolute path agar tidak bingung lokasi DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

# ----------------- FUNGSI KONTEKS DATABASE FLASK -----------------

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_NAME)
        # Mengatur row_factory menjadi sqlite3.Row agar hasil query dapat diakses seperti dictionary
        db.row_factory = sqlite3.Row 
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# ----------------- FUNGSI UTAMA (INIT) -----------------

def buat_tabel(conn):
    """Membuat tabel Mahasiswa, Dosen, Mata Kuliah, dan User jika belum ada."""
    cursor = conn.cursor()
    
    # 1. Tabel Mahasiswa
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbMahasiswa (
            nim TEXT PRIMARY KEY, 
            nama TEXT NOT NULL, 
            alamat TEXT,
            prodi TEXT
        );
    """)
    
    # 2. Tabel Dosen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbDosen (
            nip TEXT PRIMARY KEY, 
            nama TEXT NOT NULL, 
            matkul_ajar TEXT,
            telepon TEXT
        );
    """)
    
    # 3. Tabel Mata Kuliah
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbMatakuliah (
            kode_matkul TEXT PRIMARY KEY, 
            nama_matkul TEXT NOT NULL, 
            sks INTEGER,
            semester INTEGER
        );
    """)
    
    # 4. Tabel User (untuk Login)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbUser (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT 
        );
    """)

    # 5. Tabel KRS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbKRS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nim TEXT, 
            kode_matkul TEXT,
            semester INTEGER,
            tahun_ajaran TEXT,
            nilai_angka REAL,
            nilai_huruf TEXT,
            FOREIGN KEY(nim) REFERENCES tbMahasiswa(nim),
            FOREIGN KEY(kode_matkul) REFERENCES tbMatakuliah(kode_matkul)
        );
    """)

    # 6. Tabel Pembayaran
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbPembayaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nim TEXT,
            semester INTEGER,
            tahun_ajaran TEXT,
            total_sks INTEGER,
            total_bayar INTEGER,
            metode_pembayaran TEXT,
            status TEXT,    -- 'Belum Lunas', 'Lunas'
            tanggal_bayar TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(nim) REFERENCES tbMahasiswa(nim)
        );
    """)
    
    conn.commit()


# ----------------- FUNGSI USER/LOGIN -----------------

def tambah_user(conn, username, password_hash, role='Pengguna'):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbUser (username, password_hash, role) VALUES (?, ?, ?)", 
                   (username, password_hash, role))
    conn.commit()

def cari_user_by_username(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbUser WHERE username=?", (username,))
    return cursor.fetchone()

def hapus_user(conn, username):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbUser WHERE username=?", (username,))
    conn.commit()

# ----------------- FUNGSI MAHASISWA -----------------

def tambah_data_mahasiswa(conn, nim, nama, alamat, prodi):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbMahasiswa (nim, nama, alamat, prodi) VALUES (?, ?, ?, ?)", 
                   (nim, nama, alamat, prodi))
    conn.commit()

# FUNGSI INI MENDUKUNG PAGINATION DAN SEARCH
def daftar_mahasiswa(conn, search_term=None, limit=None, offset=0):
    cursor = conn.cursor()
    query = "SELECT * FROM tbMahasiswa"
    params = []
    
    if search_term:
        query += " WHERE nim LIKE ? OR nama LIKE ?"
        params = [f'%{search_term}%', f'%{search_term}%']
        
    query += " ORDER BY nim"
    
    if limit is not None:
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
    cursor.execute(query, params)
    return cursor.fetchall()

def cari_by_nim(conn, nim):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbMahasiswa WHERE nim=?", (nim,))
    return cursor.fetchone()

def ubah_data_mahasiswa(conn, nim, nama, alamat, prodi):
    cursor = conn.cursor()
    cursor.execute("UPDATE tbMahasiswa SET nama=?, alamat=?, prodi=? WHERE nim=?", 
                   (nama, alamat, prodi, nim))
    conn.commit()
    return cursor.rowcount > 0

def hapus_data_mahasiswa(conn, nim):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbMahasiswa WHERE nim=?", (nim, ))
    conn.commit()
    return cursor.rowcount > 0

# ----------------- FUNGSI DOSEN -----------------

def tambah_data_dosen(conn, nip, nama, matkul_ajar, telepon):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbDosen (nip, nama, matkul_ajar, telepon) VALUES (?, ?, ?, ?)", 
                   (nip, nama, matkul_ajar, telepon))
    conn.commit()

# FUNGSI INI MENDUKUNG PAGINATION DAN SEARCH
def daftar_dosen(conn, search_term=None, limit=None, offset=0):
    cursor = conn.cursor()
    query = "SELECT * FROM tbDosen"
    params = []
    
    if search_term:
        query += " WHERE nip LIKE ? OR nama LIKE ?"
        params = [f'%{search_term}%', f'%{search_term}%']
        
    query += " ORDER BY nip"
    
    if limit is not None:
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
    cursor.execute(query, params)
    return cursor.fetchall()

def cari_by_nip(conn, nip):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbDosen WHERE nip=?", (nip,))
    return cursor.fetchone()

def ubah_data_dosen(conn, nip, nama, matkul_ajar, telepon):
    cursor = conn.cursor()
    cursor.execute("UPDATE tbDosen SET nama=?, matkul_ajar=?, telepon=? WHERE nip=?", 
                   (nama, matkul_ajar, telepon, nip))
    conn.commit()
    return cursor.rowcount > 0

def hapus_data_dosen(conn, nip):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbDosen WHERE nip=?", (nip, ))
    conn.commit()
    return cursor.rowcount > 0

# ----------------- FUNGSI MATA KULIAH -----------------

def tambah_data_matkul(conn, kode, nama, sks, semester):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester) VALUES (?, ?, ?, ?)", 
                   (kode, nama, sks, semester))
    conn.commit()

# FUNGSI INI MENDUKUNG PAGINATION DAN SEARCH
def daftar_matkul(conn, search_term=None, limit=None, offset=0):
    cursor = conn.cursor()
    query = "SELECT * FROM tbMatakuliah"
    params = []
    if search_term:
        query += " WHERE kode_matkul LIKE ? OR nama_matkul LIKE ?"
        params = [f'%{search_term}%', f'%{search_term}%']
    query += " ORDER BY kode_matkul"
    
    if limit is not None:
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
    cursor.execute(query, params)
    return cursor.fetchall()

def cari_by_kode_matkul(conn, kode):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbMatakuliah WHERE kode_matkul=?", (kode,))
    return cursor.fetchone()

def ubah_data_matkul(conn, kode, nama, sks, semester):
    cursor = conn.cursor()
    cursor.execute("UPDATE tbMatakuliah SET nama_matkul=?, sks=?, semester=? WHERE kode_matkul=?", 
                   (nama, sks, semester, kode))
    conn.commit()
    return cursor.rowcount > 0

def hapus_data_matkul(conn, kode):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbMatakuliah WHERE kode_matkul=?", (kode, ))
    conn.commit()
    return cursor.rowcount > 0


# ----------------- FUNGSI UTILITY (PAGINATION) -----------------

# FUNGSI INI DIPERBARUI UNTUK MENGHITUNG TOTAL DATA DENGAN PENCARIAN
def hitung_jumlah_data(conn, nama_tabel, search_term=None):
    """Menghitung total data di tabel Mahasiswa, Dosen, atau Mata Kuliah, termasuk saat pencarian."""
    cursor = conn.cursor()
    query = f"SELECT COUNT(*) FROM {nama_tabel}" 
    params = []
    
    if search_term:
        if nama_tabel == 'tbMahasiswa':
            query += " WHERE nim LIKE ? OR nama LIKE ?"
            params = [f'%{search_term}%', f'%{search_term}%']
        elif nama_tabel == 'tbDosen':
            query += " WHERE nip LIKE ? OR nama LIKE ?"
            params = [f'%{search_term}%', f'%{search_term}%']
        elif nama_tabel == 'tbMatakuliah':
            query += " WHERE kode_matkul LIKE ? OR nama_matkul LIKE ?"
            params = [f'%{search_term}%', f'%{search_term}%']
            
    cursor.execute(query, params)
    return cursor.fetchone()[0]

# Fungsi wrapper untuk kemudahan
def hitung_jumlah_mahasiswa(conn, search_term=None):
    return hitung_jumlah_data(conn, 'tbMahasiswa', search_term)

def hitung_jumlah_dosen(conn, search_term=None):
    return hitung_jumlah_data(conn, 'tbDosen', search_term)
    
def hitung_jumlah_matkul(conn, search_term=None):
    return hitung_jumlah_data(conn, 'tbMatakuliah', search_term)

# ----------------- FUNGSI KRS -----------------

def tambah_krs(conn, nim, kode_matkul, semester, tahun_ajaran):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbKRS (nim, kode_matkul, semester, tahun_ajaran) VALUES (?, ?, ?, ?)", 
                   (nim, kode_matkul, semester, tahun_ajaran))
    conn.commit()

def ambil_krs_mahasiswa(conn, nim, semester, tahun_ajaran):
    cursor = conn.cursor()
    query = """
        SELECT k.id, k.nim, k.kode_matkul, k.semester, k.tahun_ajaran, m.nama_matkul, m.sks 
        FROM tbKRS k
        JOIN tbMatakuliah m ON k.kode_matkul = m.kode_matkul
        WHERE k.nim = ? AND k.semester = ? AND k.tahun_ajaran = ?
    """
    cursor.execute(query, (nim, semester, tahun_ajaran))
    return cursor.fetchall()

def hapus_krs(conn, id_krs):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tbKRS WHERE id=?", (id_krs,))
    conn.commit()
    return cursor.rowcount > 0

def hitung_sks_krs(conn, nim, semester, tahun_ajaran):
    cursor = conn.cursor()
    query = """
        SELECT SUM(m.sks) 
        FROM tbKRS k
        JOIN tbMatakuliah m ON k.kode_matkul = m.kode_matkul
        WHERE k.nim = ? AND k.semester = ? AND k.tahun_ajaran = ?
    """
    cursor.execute(query, (nim, semester, tahun_ajaran))
    total = cursor.fetchone()[0]
    return total if total else 0

def cek_krs_exist(conn, nim, kode_matkul, semester, tahun_ajaran):
    cursor = conn.cursor()
    query = "SELECT * FROM tbKRS WHERE nim=? AND kode_matkul=? AND semester=? AND tahun_ajaran=?"
    cursor.execute(query, (nim, kode_matkul, semester, tahun_ajaran))
    return cursor.fetchone()

# --- FUNGSI PENILAIAN ---

def ambil_mahasiswa_kelas(conn, kode_matkul, semester, tahun_ajaran):
    """Mengambil daftar mahasiswa yang mengambil suatu MK di semester/tahun tertentu."""
    cursor = conn.cursor()
    query = """
        SELECT k.id, k.nim, mhs.nama, k.nilai_angka, k.nilai_huruf
        FROM tbKRS k
        JOIN tbMahasiswa mhs ON k.nim = mhs.nim
        WHERE k.kode_matkul = ? AND k.semester = ? AND k.tahun_ajaran = ?
        ORDER BY k.nim
    """
    cursor.execute(query, (kode_matkul, semester, tahun_ajaran))
    return cursor.fetchall()

def simpan_nilai(conn, id_krs, nilai_angka, nilai_huruf):
    cursor = conn.cursor()
    cursor.execute("UPDATE tbKRS SET nilai_angka=?, nilai_huruf=? WHERE id=?", 
                   (nilai_angka, nilai_huruf, id_krs))
    conn.commit()
    return cursor.rowcount > 0

def ambil_khs(conn, nim, semester, tahun_ajaran):
    """Mengambil KHS (KRS + Nilai) untuk mahasiswa."""
    # Sebenarnya mirip ambil_krs, tapi kita fokuskan penamaan untuk KHS
    return ambil_krs_mahasiswa(conn, nim, semester, tahun_ajaran)

# Update ambil_krs_mahasiswa agar SELECT nilai juga
def ambil_krs_mahasiswa(conn, nim, semester, tahun_ajaran):
    cursor = conn.cursor()
    query = """
        SELECT k.id, k.nim, k.kode_matkul, k.semester, k.tahun_ajaran, 
               m.nama_matkul, m.sks, k.nilai_angka, k.nilai_huruf
        FROM tbKRS k
        JOIN tbMatakuliah m ON k.kode_matkul = m.kode_matkul
        WHERE k.nim = ? AND k.semester = ? AND k.tahun_ajaran = ?
    """
    cursor.execute(query, (nim, semester, tahun_ajaran))
    return cursor.fetchall()

# ----------------- FUNGSI PEMBAYARAN -----------------

def buat_tagihan(conn, nim, semester, tahun_ajaran, total_sks, total_bayar):
    cursor = conn.cursor()
    # Cek apakah sudah ada tagihan untuk semester ini, jika ada update
    cursor.execute("SELECT id FROM tbPembayaran WHERE nim=? AND semester=? AND tahun_ajaran=?", 
                   (nim, semester, tahun_ajaran))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute("""
            UPDATE tbPembayaran 
            SET total_sks=?, total_bayar=? 
            WHERE id=? AND status='Belum Lunas'
        """, (total_sks, total_bayar, existing['id']))
    else:
        cursor.execute("""
            INSERT INTO tbPembayaran (nim, semester, tahun_ajaran, total_sks, total_bayar, status)
            VALUES (?, ?, ?, ?, ?, 'Belum Lunas')
        """, (nim, semester, tahun_ajaran, total_sks, total_bayar))
    conn.commit()

def bayar_tagihan(conn, nim, semester, tahun_ajaran, metode):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tbPembayaran 
        SET status='Lunas', metode_pembayaran=?, tanggal_bayar=CURRENT_TIMESTAMP
        WHERE nim=? AND semester=? AND tahun_ajaran=?
    """, (metode, nim, semester, tahun_ajaran))
    conn.commit()
    return cursor.rowcount > 0

def cek_status_pembayaran(conn, nim, semester, tahun_ajaran):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbPembayaran WHERE nim=? AND semester=? AND tahun_ajaran=?", 
                   (nim, semester, tahun_ajaran))
    return cursor.fetchone()

def ambil_pembayaran_by_id(conn, id_pembayaran):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbPembayaran WHERE id=?", (id_pembayaran,))
    return cursor.fetchone()