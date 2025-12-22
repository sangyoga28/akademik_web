# File: repository.py (MODIFIED FOR REGISTRATION SYSTEM)

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
            prodi TEXT,
            fakultas TEXT
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
            semester INTEGER,
            prodi TEXT
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

    # 7. Tabel Pendaftaran (Pending Approval)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbPendaftaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            role TEXT NOT NULL, 
            alamat TEXT,
            prodi TEXT,         
            fakultas TEXT,      
            telepon TEXT,
            matkul_ajar TEXT,   
            password_hash TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            nim_nip TEXT,
            tanggal_daftar TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def tambah_data_mahasiswa(conn, nim, nama, alamat, prodi, fakultas=None):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbMahasiswa (nim, nama, alamat, prodi, fakultas) VALUES (?, ?, ?, ?, ?)", 
                   (nim, nama, alamat, prodi, fakultas))
    conn.commit()

# FUNGSI INI MENDUKUNG PAGINATION DAN SEARCH
def daftar_mahasiswa(conn, search_term=None, fakultas=None, prodi=None, limit=None, offset=0):
    cursor = conn.cursor()
    query = "SELECT * FROM tbMahasiswa WHERE 1=1"
    params = []
    
    if search_term:
        query += " AND (nim LIKE ? OR nama LIKE ?)"
        params.extend([f'%{search_term}%', f'%{search_term}%'])
    
    if fakultas:
        query += " AND fakultas = ?"
        params.append(fakultas)
    
    if prodi:
        query += " AND prodi = ?"
        params.append(prodi)
        
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

def ubah_data_mahasiswa(conn, nim, nama, alamat, prodi, fakultas=None):
    cursor = conn.cursor()
    cursor.execute("UPDATE tbMahasiswa SET nama=?, alamat=?, prodi=?, fakultas=? WHERE nim=?", 
                   (nama, alamat, prodi, fakultas, nim))
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
def daftar_dosen(conn, search_term=None, fakultas=None, prodi=None, limit=None, offset=0):
    cursor = conn.cursor()
    
    # Base query: Always join to allow filtering by prodi/fakultas of their matkul
    query = """
        SELECT DISTINCT d.* FROM tbDosen d
        LEFT JOIN tbMatakuliah m ON d.matkul_ajar = m.nama_matkul
        WHERE 1=1
    """
    params = []
    
    if search_term:
        query += " AND (d.nip LIKE ? OR d.nama LIKE ?)"
        params.extend([f'%{search_term}%', f'%{search_term}%'])
        
    if fakultas:
        query += " AND m.fakultas_temp = ?" # Note: We might need a proper join or assume name-based logic
        # Actually, tbMatakuliah doesn't have fakultas. We mapping it via prodi.
        # Let's use prodi filtering for now or a subquery if needed.
        # But wait, audit_database.py uses tbMahasiswa for faculties. 
        # Typically Faculty -> Prodi -> Matkul.
        pass

    if prodi:
        query += " AND m.prodi = ?"
        params.append(prodi)
        
    query += " ORDER BY d.nip"
    
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

def tambah_data_matkul(conn, kode, nama, sks, semester, prodi=None):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tbMatakuliah (kode_matkul, nama_matkul, sks, semester, prodi) VALUES (?, ?, ?, ?, ?)", 
                   (kode, nama, sks, semester, prodi))
    conn.commit()

# FUNGSI INI MENDUKUNG PAGINATION DAN SEARCH
def daftar_matkul(conn, search_term=None, prodi=None, semester=None, limit=None, offset=0):
    cursor = conn.cursor()
    query = "SELECT * FROM tbMatakuliah WHERE 1=1"
    params = []
    if search_term:
        query += " AND (kode_matkul LIKE ? OR nama_matkul LIKE ?)"
        params.extend([f'%{search_term}%', f'%{search_term}%'])
    
    if prodi:
        query += " AND prodi = ?"
        params.append(prodi)
    
    if semester:
        query += " AND semester = ?"
        params.append(semester)

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

def ubah_data_matkul(conn, kode, nama, sks, semester, prodi=None):
    cursor = conn.cursor()
    cursor.execute("UPDATE tbMatakuliah SET nama_matkul=?, sks=?, semester=?, prodi=? WHERE kode_matkul=?", 
                   (nama, sks, semester, prodi, kode))
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
def hitung_jumlah_mahasiswa(conn, search_term=None, fakultas=None, prodi=None):
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM tbMahasiswa WHERE 1=1"
    params = []
    if search_term:
        query += " AND (nim LIKE ? OR nama LIKE ?)"
        params.extend([f'%{search_term}%', f'%{search_term}%'])
    if fakultas:
        query += " AND fakultas = ?"
        params.append(fakultas)
    if prodi:
        query += " AND prodi = ?"
        params.append(prodi)
    cursor.execute(query, params)
    return cursor.fetchone()[0]

def hitung_jumlah_dosen(conn, search_term=None, fakultas=None, prodi=None):
    cursor = conn.cursor()
    query = """
        SELECT COUNT(DISTINCT d.nip) FROM tbDosen d
        LEFT JOIN tbMatakuliah m ON d.matkul_ajar = m.nama_matkul
        WHERE 1=1
    """
    params = []
    if search_term:
        query += " AND (d.nip LIKE ? OR d.nama LIKE ?)"
        params.extend([f'%{search_term}%', f'%{search_term}%'])
    if prodi:
        query += " AND m.prodi = ?"
        params.append(prodi)
    cursor.execute(query, params)
    return cursor.fetchone()[0]

def hitung_jumlah_matkul(conn, search_term=None, prodi=None, semester=None):
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM tbMatakuliah WHERE 1=1"
    params = []
    if search_term:
        query += " AND (kode_matkul LIKE ? OR nama_matkul LIKE ?)"
        params.extend([f'%{search_term}%', f'%{search_term}%'])
    if prodi:
        query += " AND prodi = ?"
        params.append(prodi)
    if semester:
        query += " AND semester = ?"
        params.append(semester)
    cursor.execute(query, params)
    return cursor.fetchone()[0]

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

def tambah_krs_bulk(conn, nim, semester, tahun_ajaran):
    """Menambahkan semua mata kuliah prodi mahasiswa untuk semester tertentu (Max 24 SKS)."""
    # 1. Ambil prodi mahasiswa
    mhs = cari_by_nim(conn, nim)
    if not mhs: return False, "Mahasiswa tidak ditemukan."
    prodi = mhs['prodi']
    
    # 2. Ambil semua matkul prodi tsb di semester tsb
    matkul_tersedia = ambil_matkul_by_prodi_semester(conn, prodi, semester)
    
    # 3. Hitung SKS saat ini
    current_sks = hitung_sks_krs(conn, nim, semester, tahun_ajaran)
    
    added_count = 0
    skipped_count = 0
    
    for mk in matkul_tersedia:
        kode = mk['kode_matkul']
        sks = mk['sks']
        
        # Cek apakah sudah ada
        if cek_krs_exist(conn, nim, kode, semester, tahun_ajaran):
            skipped_count += 1
            continue
            
        # Cek batas SKS
        if current_sks + sks > 24:
            break
            
        # Tambah
        tambah_krs(conn, nim, kode, semester, tahun_ajaran)
        current_sks += sks
        added_count += 1
        
    return True, f"Berhasil menambahkan {added_count} mata kuliah. {skipped_count} sudah ada."

# --- FUNGSI PENILAIAN ---

def ambil_mahasiswa_kelas(conn, kode_matkul, semester, tahun_ajaran):
    """Mengambil daftar mahasiswa yang mengambil suatu MK dan SUDAH LUNAS pembayarannya."""
    cursor = conn.cursor()
    query = """
        SELECT k.id, k.nim, mhs.nama, k.nilai_angka, k.nilai_huruf
        FROM tbKRS k
        JOIN tbMahasiswa mhs ON k.nim = mhs.nim
        JOIN tbPembayaran p ON k.nim = p.nim AND k.semester = p.semester AND k.tahun_ajaran = p.tahun_ajaran
        WHERE k.kode_matkul = ? AND k.semester = ? AND k.tahun_ajaran = ? AND p.status = 'Lunas'
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

# ----------------- FUNGSI HELPER UNTUK DROPDOWN DINAMIS -----------------

def ambil_daftar_prodi(conn):
    """Mengambil daftar program studi unik dari database (kecuali 'Umum')."""
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT prodi FROM tbMatakuliah WHERE prodi != "Umum" ORDER BY prodi')
    return [row[0] for row in cursor.fetchall()]

def ambil_daftar_fakultas(conn):
    """Mengambil daftar fakultas unik dari database mahasiswa."""
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT fakultas FROM tbMahasiswa WHERE fakultas IS NOT NULL ORDER BY fakultas')
    result = [row[0] for row in cursor.fetchall()]
    # Jika belum ada data, return default fakultas
    if not result:
        return ['Fakultas Teknik', 'Fakultas Ekonomi', 'Fakultas Sastra', 'Fakultas Hukum']
    return result

def ambil_matkul_by_prodi_semester(conn, prodi, semester):
    """Mengambil mata kuliah berdasarkan prodi dan semester tertentu."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT kode_matkul, nama_matkul, sks, semester, prodi 
        FROM tbMatakuliah 
        WHERE (prodi = ? OR prodi = 'Umum') AND semester = ?
        ORDER BY semester, nama_matkul
    ''', (prodi, semester))
    return cursor.fetchall()

def ambil_semua_matkul_untuk_dosen(conn):
    """Mengambil semua mata kuliah untuk dropdown dosen (kecuali Umum)."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT kode_matkul, nama_matkul, prodi, semester 
        FROM tbMatakuliah 
        WHERE prodi != 'Umum'
        ORDER BY prodi, semester, nama_matkul
    ''')
    return cursor.fetchall()

# ----------------- FUNGSI PENDAFTARAN & APPROVAL -----------------

def tambah_pendaftaran(conn, nama, role, alamat, prodi, fakultas, telepon, matkul_ajar, password_hash):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tbPendaftaran (nama, role, alamat, prodi, fakultas, telepon, matkul_ajar, password_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nama, role, alamat, prodi, fakultas, telepon, matkul_ajar, password_hash))
    conn.commit()

def ambil_pendaftaran_pending(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbPendaftaran WHERE status='Pending' ORDER BY id DESC")
    return cursor.fetchall()

def ambil_pendaftaran_by_id(conn, id_pendaftaran):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbPendaftaran WHERE id=?", (id_pendaftaran,))
    return cursor.fetchone()

def update_status_pendaftaran(conn, id_pendaftaran, status):
    cursor = conn.cursor()
    cursor.execute("UPDATE tbPendaftaran SET status=? WHERE id=?", (status, id_pendaftaran))
    conn.commit()

def update_nim_nip_pendaftaran(conn, id_pendaftaran, nim_nip):
    cursor = conn.cursor()
    cursor.execute("UPDATE tbPendaftaran SET nim_nip=? WHERE id=?", (nim_nip, id_pendaftaran))
    conn.commit()

def generate_nim_baru(conn):
    import datetime
    tahun = datetime.datetime.now().year
    prefix = f"{tahun}01"
    cursor = conn.cursor()
    cursor.execute("SELECT nim FROM tbMahasiswa WHERE nim LIKE ? ORDER BY nim DESC LIMIT 1", (f"{prefix}%",))
    last = cursor.fetchone()
    if last:
        new_seq = str(int(last[0][6:]) + 1).zfill(4)
    else:
        new_seq = "0001"
    return f"{prefix}{new_seq}"

def generate_nip_baru(conn):
    import datetime
    tahun = datetime.datetime.now().year
    prefix = f"{tahun}02"
    cursor = conn.cursor()
    cursor.execute("SELECT nip FROM tbDosen WHERE nip LIKE ? ORDER BY nip DESC LIMIT 1", (f"{prefix}%",))
    last = cursor.fetchone()
    if last:
        new_seq = str(int(last[0][6:]) + 1).zfill(4)
    else:
        new_seq = "0001"
    return f"{prefix}{new_seq}"

def hitung_pendaftaran_pending(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tbPendaftaran WHERE status='Pending'")
    return cursor.fetchone()[0]

def cek_status_pendaftaran_user(conn, nama, telepon):
    """Mencari status pendaftaran berdasarkan nama dan telepon."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM tbPendaftaran 
        WHERE nama = ? AND telepon = ? 
        ORDER BY id DESC LIMIT 1
    """, (nama, telepon))
    return cursor.fetchone()

def ambil_prodi_by_fakultas(conn, fakultas):
    """Mengambil daftar prodi yang berasosiasi dengan fakultas tertentu."""
    mapping = {
        'Fakultas Teknik': ['Informatika', 'Sistem Informasi', 'Teknik Elektro', 'Teknik Sipil'],
        'Fakultas Ekonomi': ['Manajemen', 'Akuntansi'],
        'Fakultas Sastra': ['Sastra Inggris', 'Sastra Jepang'],
        'Fakultas Hukum': ['Ilmu Hukum']
    }
    return mapping.get(fakultas, [])