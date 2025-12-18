# File: app.py (VERSI FINAL & LENGKAP)

from flask import (
    Flask, render_template, redirect, url_for, 
    request, flash, g, session 
)
from werkzeug.security import generate_password_hash, check_password_hash 
from math import ceil # Digunakan untuk menghitung total halaman
import repository as repo

# Konfigurasi Aplikasi
app = Flask(__name__)
app.secret_key = 'kunci_rahasia_akademik_anda_yang_sangat_panjang_dan_aman' 
app.secret_key = 'kunci_rahasia_akademik_anda_yang_sangat_panjang_dan_aman' 
PER_PAGE = 10 # Konstanta jumlah data per halaman
HARGA_PER_SKS = 150000 # Harga per SKS

# ----------------- SETUP KONEKSI DB -----------------

def get_db():
    return repo.get_db()

@app.teardown_appcontext
def close_connection(exception):
    repo.close_connection(exception)
    
# Inisialisasi DB dan data dummy saat startup
with app.app_context():
    conn = get_db()
    repo.buat_tabel(conn)
    
    # --- Tambahkan Dummy User untuk Login ---
    try:
        if repo.cari_user_by_username(conn, 'admin') is None:
            # Hashing password sebelum disimpan. Password: 'admin123'
            hashed_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
            repo.tambah_user(conn, 'admin', hashed_pw, role='Admin Sistem')
            print("User 'admin' berhasil ditambahkan (Password: admin123).")
    except Exception as e:
        print(f"Error tambah user dummy: {e}") 
        
    # --- Data Dummy Mahasiswa (21 Data) ---
    try:
        repo.tambah_data_mahasiswa(conn, '123', 'Ahmad Budiman', 'Bandung', 'TI')
        repo.tambah_data_mahasiswa(conn, '124', 'Budi Cahyono', 'Jakarta', 'TI')
        repo.tambah_data_mahasiswa(conn, '125', 'Citra Dewi', 'Surabaya', 'SI')
        repo.tambah_data_mahasiswa(conn, '126', 'Dedi Firmansyah', 'Malang', 'TE')
        repo.tambah_data_mahasiswa(conn, '127', 'Eka Lestari', 'Yogyakarta', 'TI')
        repo.tambah_data_mahasiswa(conn, '128', 'Fajar Gunawan', 'Bandung', 'SI')
        repo.tambah_data_mahasiswa(conn, '129', 'Gita Hutami', 'Jakarta', 'TI')
        repo.tambah_data_mahasiswa(conn, '130', 'Hendra Irawan', 'Surabaya', 'TE')
        repo.tambah_data_mahasiswa(conn, '131', 'Indah Jaya', 'Malang', 'SI')
        repo.tambah_data_mahasiswa(conn, '132', 'Joko Kusuma', 'Yogyakarta', 'TI')
        repo.tambah_data_mahasiswa(conn, '133', 'Kiki Larasati', 'Bandung', 'SI') 
        repo.tambah_data_mahasiswa(conn, '134', 'Lukman Nur', 'Jakarta', 'TI')
        repo.tambah_data_mahasiswa(conn, '135', 'Mia Puspita', 'Surabaya', 'SI')
        repo.tambah_data_mahasiswa(conn, '136', 'Nanda Octavia', 'Malang', 'TE')
        repo.tambah_data_mahasiswa(conn, '137', 'Oscar Putra', 'Yogyakarta', 'TI')
        repo.tambah_data_mahasiswa(conn, '138', 'Putri Qalesya', 'Bandung', 'SI')
        repo.tambah_data_mahasiswa(conn, '139', 'Rizky Satria', 'Jakarta', 'TI')
        repo.tambah_data_mahasiswa(conn, '140', 'Sinta Tania', 'Surabaya', 'TE')
        repo.tambah_data_mahasiswa(conn, '141', 'Umar Vanu', 'Malang', 'SI')
        repo.tambah_data_mahasiswa(conn, '142', 'Wulan Xena', 'Yogyakarta', 'TI')
        repo.tambah_data_mahasiswa(conn, '143', 'Yusuf Zaki', 'Bandung', 'SI')
    except Exception as e:
        # print(f"Error tambah data dummy mahasiswa: {e}") 
        pass 
        
    # --- Data Dummy Dosen (12 Data) ---
    try:
        repo.tambah_data_dosen(conn, '9901', 'Dr. Ir. Budi Utama', 'Pemrograman Web', '0812123456')
        repo.tambah_data_dosen(conn, '9902', 'Prof. Dr. Citra Sari', 'Jaringan Komputer', '0813234567')
        repo.tambah_data_dosen(conn, '9903', 'M.T. Dedi Irawan', 'Basis Data', '0815456789')
        repo.tambah_data_dosen(conn, '9904', 'Drs. Eka Putra', 'Kalkulus', '0817678901')
        repo.tambah_data_dosen(conn, '9905', 'Ir. Fajar Setiawan', 'Sistem Operasi', '0818890123')
        repo.tambah_data_dosen(conn, '9906', 'Ph.D. Gita Larasati', 'Statistika', '0819012345')
        repo.tambah_data_dosen(conn, '9907', 'M.Kom. Haris Jaya', 'Keamanan Informasi', '0812234567')
        repo.tambah_data_dosen(conn, '9908', 'M.Sc. Intan Permata', 'Pemrograman Mobile', '0813345678')
        repo.tambah_data_dosen(conn, '9909', 'Dr. Joko Susilo', 'Riset Operasi', '0815567890')
        repo.tambah_data_dosen(conn, '9910', 'Ir. Kiki Andriani', 'Grafika Komputer', '0817789012')
        repo.tambah_data_dosen(conn, '9911', 'Prof. Lukman S.', 'Struktur Data', '0818901234')
        repo.tambah_data_dosen(conn, '9912', 'M.T. Nia Zulaika', 'Manajemen Proyek', '0812345678')
    except Exception as e:
        pass
        
    # --- Data Dummy Mata Kuliah (11 Data) ---
    try:
        repo.tambah_data_matkul(conn, 'WEB101', 'Pemrograman Web', 3, 3)
        repo.tambah_data_matkul(conn, 'NET201', 'Jaringan Komputer', 3, 4)
        repo.tambah_data_matkul(conn, 'DBA301', 'Basis Data', 3, 5)
        repo.tambah_data_matkul(conn, 'MTH101', 'Kalkulus I', 4, 1)
        repo.tambah_data_matkul(conn, 'OSY202', 'Sistem Operasi', 3, 4)
        repo.tambah_data_matkul(conn, 'STA102', 'Statistika Dasar', 3, 2)
        repo.tambah_data_matkul(conn, 'INF305', 'Keamanan Informasi', 3, 6)
        repo.tambah_data_matkul(conn, 'MOB401', 'Pemrograman Mobile', 3, 7)
        repo.tambah_data_matkul(conn, 'RSO402', 'Riset Operasi', 3, 7)
        repo.tambah_data_matkul(conn, 'GRA403', 'Grafika Komputer', 3, 8)
        repo.tambah_data_matkul(conn, 'STR203', 'Struktur Data', 3, 3)
    except Exception as e:
        pass

# ----------------- ROUTE LOGIN & LOGOUT -----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = repo.cari_user_by_username(conn, username)
        
        if user and check_password_hash(user['password_hash'], password):
            session['logged_in'] = True
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Selamat datang, {user["username"]}! Anda berhasil login.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login gagal. Periksa username dan password Anda.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() # Hapus semua sesi
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('login'))

# ----------------- ROUTE UTAMA -----------------

# ----------------- ROUTE UTAMA -----------------

@app.route('/')
def index():
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('login'))
        
    conn = get_db()
    
    # Kustomisasi Dashboard berdasarkan Role
    role = session.get('role')
    
    # Jika Admin, tampilkan statistik
    if role == 'Admin Sistem':
        total_mahasiswa = repo.hitung_jumlah_mahasiswa(conn)
        total_dosen = repo.hitung_jumlah_dosen(conn)
        total_matkul = repo.hitung_jumlah_matkul(conn)
        
        return render_template('home.html',
            total_mahasiswa=total_mahasiswa,
            total_dosen=total_dosen,
            total_matkul=total_matkul
        )
    
    # Jika Mahasiswa, mungkin redirect ke KRS atau tampilkan info mahasiswa
    elif role == 'Mahasiswa':
        # Bisa redirect langsung ke halaman KRS milik sendiri
        return redirect(url_for('manage_krs', nim=session.get('username')))
        
    # Jika Dosen, redirect atau tampilkan dashboard simple
    elif role == 'Dosen':
        return render_template('home.html', 
                               total_mahasiswa=0, total_dosen=0, total_matkul=0) # Dummy data agar tidak error
    
    return render_template('home.html')

# ----------------- ROUTE MAHASISWA -----------------

@app.route('/mahasiswa')
def daftar_mahasiswa():
    # PROTEKSI ROUTE
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('login'))

    conn = get_db()
    
    # Ambil parameter halaman (page) dan pencarian (q) dari URL
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    
    # Hitung offset untuk database
    offset = (page - 1) * PER_PAGE
    
    # Ambil data dengan limit dan offset
    data = repo.daftar_mahasiswa(conn, search_term=q, limit=PER_PAGE, offset=offset)
    
    # Hitung total data dan total halaman
    total_data = repo.hitung_jumlah_mahasiswa(conn, search_term=q)
    total_pages = ceil(total_data / PER_PAGE)
    
    # Jika hasil pencarian kosong, tampilkan notifikasi
    if q and not data and total_data == 0:
        flash(f"Tidak ada data Mahasiswa yang ditemukan untuk pencarian '{q}'.", 'info')

    return render_template('mahasiswa.html', 
                           data=data, 
                           page=page, 
                           total_pages=total_pages, 
                           q=q, 
                           total_data=total_data,
                           PER_PAGE=PER_PAGE) # Kirim PER_PAGE ke template

@app.route('/mahasiswa/tambah', methods=['GET', 'POST'])
def tambah_mahasiswa():
    if not session.get('logged_in'): return redirect(url_for('login'))
        
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        alamat = request.form['alamat']
        prodi = request.form['prodi']
        
        if not nim or not nama:
            flash('NIM dan Nama wajib diisi!', 'danger')
            return redirect(url_for('tambah_mahasiswa'))
            
        conn = get_db()
        if repo.cari_by_nim(conn, nim):
            flash(f'NIM {nim} sudah terdaftar!', 'danger')
            return redirect(url_for('tambah_mahasiswa'))
            
        try:
            repo.tambah_data_mahasiswa(conn, nim, nama, alamat, prodi)
            
            # --- AUTO REGISTER USER MAHASISWA ---
            # Default Password = NIM
            hashed_pw = generate_password_hash(nim, method='pbkdf2:sha256')
            repo.tambah_user(conn, nim, hashed_pw, role='Mahasiswa')
            
            flash(f'Data Mahasiswa {nim} berhasil ditambahkan! Akun Login otomatis dibuat (Pass: {nim}).', 'success')
            return redirect(url_for('daftar_mahasiswa'))
        except:
            flash('Gagal simpan atau NIM sudah ada akun.', 'danger')
            
    return render_template('tambah_mahasiswa.html')

@app.route('/mahasiswa/edit/<nim>', methods=['GET', 'POST'])
def edit_mahasiswa(nim):
    if not session.get('logged_in'): return redirect(url_for('login'))
        
    conn = get_db()
    data = repo.cari_by_nim(conn, nim)
    if not data: return redirect(url_for('daftar_mahasiswa'))

    if request.method == 'POST':
        nama_baru = request.form['nama']
        alamat_baru = request.form['alamat']
        prodi_baru = request.form['prodi']

        if not nama_baru:
            flash('Nama wajib diisi!', 'danger')
            return redirect(url_for('edit_mahasiswa', nim=nim))
            
        repo.ubah_data_mahasiswa(conn, nim, nama_baru, alamat_baru, prodi_baru)
        flash(f'Data Mahasiswa {nim} berhasil diubah!', 'warning')
        return redirect(url_for('daftar_mahasiswa'))
        
    return render_template('edit_mahasiswa.html', mhs=data)

@app.route('/mahasiswa/hapus/<nim>', methods=['POST'])
def hapus_mahasiswa(nim):
    if not session.get('logged_in'): return redirect(url_for('login'))
        
    conn = get_db()
    
    # Hapus Data Mahasiswa
    success = repo.hapus_data_mahasiswa(conn, nim)
    
    if success:
        # --- HAPUS JUGA AKUN LOGIN ---
        repo.hapus_user(conn, username=nim)
        flash(f'Data Mahasiswa {nim} dan akun loginnya berhasil dihapus!', 'danger')
    else:
        flash(f'Gagal menghapus data Mahasiswa {nim}.', 'danger')
        
    return redirect(url_for('daftar_mahasiswa'))

# ----------------- ROUTE DOSEN -----------------

@app.route('/dosen')
def daftar_dosen():
    # PROTEKSI ROUTE
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('login'))

    conn = get_db()
    
    # Ambil parameter halaman (page) dan pencarian (q) dari URL
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    
    # Hitung offset untuk database
    offset = (page - 1) * PER_PAGE
    
    # Ambil data dengan limit dan offset
    data = repo.daftar_dosen(conn, search_term=q, limit=PER_PAGE, offset=offset)
    
    # Hitung total data dan total halaman
    total_data = repo.hitung_jumlah_dosen(conn, search_term=q)
    total_pages = ceil(total_data / PER_PAGE)
    
    # Jika hasil pencarian kosong, tampilkan notifikasi
    if q and not data and total_data == 0:
        flash(f"Tidak ada data Dosen yang ditemukan untuk pencarian '{q}'.", 'info')

    return render_template('dosen.html', 
                           data=data, 
                           page=page, 
                           total_pages=total_pages, 
                           q=q, 
                           total_data=total_data,
                           PER_PAGE=PER_PAGE) 
                           
@app.route('/dosen/tambah', methods=['GET', 'POST'])
def tambah_dosen():
    if not session.get('logged_in'): return redirect(url_for('login'))
        
    if request.method == 'POST':
        nip = request.form['nip']
        nama = request.form['nama']
        matkul_ajar = request.form['matkul_ajar']
        telepon = request.form['telepon']
        
        if not nip or not nama:
            flash('NIP dan Nama wajib diisi!', 'danger')
            return redirect(url_for('tambah_dosen'))
            
        conn = get_db()
        if repo.cari_by_nip(conn, nip):
            flash(f'NIP {nip} sudah terdaftar!', 'danger')
            return redirect(url_for('tambah_dosen'))
            
        try:
            repo.tambah_data_dosen(conn, nip, nama, matkul_ajar, telepon)
            
            # --- AUTO REGISTER USER DOSEN ---
            # Default Password = NIP
            hashed_pw = generate_password_hash(nip, method='pbkdf2:sha256')
            repo.tambah_user(conn, nip, hashed_pw, role='Dosen')
            
            flash(f'Data Dosen {nip} berhasil ditambahkan! Akun Login otomatis dibuat (Pass: {nip}).', 'success')
            return redirect(url_for('daftar_dosen'))
        except:
            flash('Gagal simpan atau NIP sudah ada akun.', 'danger')
            
    return render_template('tambah_dosen.html')

@app.route('/dosen/edit/<nip>', methods=['GET', 'POST'])
def edit_dosen(nip):
    if not session.get('logged_in'): return redirect(url_for('login'))
        
    conn = get_db()
    data = repo.cari_by_nip(conn, nip)
    if not data: return redirect(url_for('daftar_dosen'))

    if request.method == 'POST':
        nama_baru = request.form['nama']
        matkul_ajar_baru = request.form['matkul_ajar']
        telepon_baru = request.form['telepon']

        if not nama_baru:
            flash('Nama wajib diisi!', 'danger')
            return redirect(url_for('edit_dosen', nip=nip))
            
        repo.ubah_data_dosen(conn, nip, nama_baru, matkul_ajar_baru, telepon_baru)
        flash(f'Data Dosen {nip} berhasil diubah!', 'warning')
        return redirect(url_for('daftar_dosen'))
        
    return render_template('edit_dosen.html', dosen=data)

@app.route('/dosen/hapus/<nip>', methods=['POST'])
def hapus_dosen(nip):
    if not session.get('logged_in'): return redirect(url_for('login'))
        
    conn = get_db()
    success = repo.hapus_data_dosen(conn, nip)
    if success:
        # --- HAPUS JUGA AKUN LOGIN ---
        repo.hapus_user(conn, username=nip)
        flash(f'Data Dosen {nip} dan akun loginnya berhasil dihapus!', 'danger')
    else:
        flash(f'Gagal menghapus data Dosen {nip}.', 'danger')
        
    return redirect(url_for('daftar_dosen'))

    return redirect(url_for('daftar_dosen'))

# ----------------- ROUTE PENILAIAN (DOSEN) -----------------

def konversi_nilai(angka):
    if angka >= 85: return 'A'
    elif angka >= 75: return 'B'
    elif angka >= 60: return 'C'
    elif angka >= 50: return 'D'
    else: return 'E'

@app.route('/dosen/nilai', methods=['GET', 'POST'])
def dosen_nilai_dashboard():
    if not session.get('logged_in') or session.get('role') not in ['Dosen', 'Admin Sistem']:
        return redirect(url_for('login'))
    
    conn = get_db()
    
    # Filter Default
    semester = request.args.get('semester', 1, type=int)
    tahun = request.args.get('tahun', '2023/2024')
    
    # Dosen bisa memilih mata kuliah apa saja yg mau dinilai (Simplifikasi)
    # Idealnya hanya MK yang diajar, tapi karena struktur DB simple, kita tampilkan semua MK
    # Nanti sistem akan cek apakah ada mahasiswa di MK itu di sem/tahun tsb
    daftar_matkul = repo.daftar_matkul(conn, limit=1000)
    
    return render_template('dosen_nilai_dashboard.html', 
                           matkul_list=daftar_matkul,
                           semester=semester,
                           tahun=tahun)

@app.route('/dosen/nilai/input/<kode_matkul>', methods=['GET', 'POST'])
def input_nilai(kode_matkul):
    if not session.get('logged_in') or session.get('role') not in ['Dosen', 'Admin Sistem']:
        return redirect(url_for('login'))
        
    conn = get_db()
    semester = request.args.get('semester', 1, type=int)
    tahun = request.args.get('tahun', '2023/2024')
    
    matkul = repo.cari_by_kode_matkul(conn, kode_matkul)
    
    if request.method == 'POST':
        # Loop semua input dari form
        # Form name pattern: nilai_angka_{id_krs}
        for key, val in request.form.items():
            if key.startswith('nilai_angka_'):
                id_krs = key.split('_')[2]
                try:
                    nilai_angka = float(val)
                    nilai_huruf = konversi_nilai(nilai_angka)
                    repo.simpan_nilai(conn, id_krs, nilai_angka, nilai_huruf)
                except ValueError:
                    pass # Ignore invalid input
                    
        flash('Nilai berhasil disimpan!', 'success')
        return redirect(url_for('input_nilai', kode_matkul=kode_matkul, semester=semester, tahun=tahun))
    
    mahasiswa_list = repo.ambil_mahasiswa_kelas(conn, kode_matkul, semester, tahun)
    
    return render_template('input_nilai.html', 
                           matkul=matkul,
                           mahasiswa_list=mahasiswa_list,
                           semester=semester,
                           tahun=tahun)

@app.route('/matkul')
def daftar_matkul():
    # PROTEKSI ROUTE
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('login'))
        
    conn = get_db()

    # Ambil parameter halaman (page) dan pencarian (q) dari URL
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')

    # Hitung offset untuk database
    offset = (page - 1) * PER_PAGE
    
    # Ambil data dengan limit dan offset
    data = repo.daftar_matkul(conn, search_term=q, limit=PER_PAGE, offset=offset)

    # Hitung total data dan total halaman
    total_data = repo.hitung_jumlah_matkul(conn, search_term=q)
    total_pages = ceil(total_data / PER_PAGE)
    
    # Jika hasil pencarian kosong, tampilkan notifikasi
    if q and not data and total_data == 0:
        flash(f"Tidak ada data Mata Kuliah yang ditemukan untuk pencarian '{q}'.", 'info')
        
    return render_template('matkul.html', 
                           data=data, 
                           page=page, 
                           total_pages=total_pages, 
                           q=q,
                           total_data=total_data,
                           PER_PAGE=PER_PAGE)
                           
@app.route('/matkul/tambah', methods=['GET', 'POST'])
def tambah_matkul():
    if not session.get('logged_in'): return redirect(url_for('login'))
        
    if request.method == 'POST':
        kode = request.form['kode_matkul']
        nama = request.form['nama_matkul']
        sks = request.form['sks']
        smt = request.form['semester']

        if not kode or not nama:
            flash('Kode dan Nama Mata Kuliah wajib diisi!', 'danger')
            return redirect(url_for('tambah_matkul'))
            
        conn = get_db()
        if repo.cari_by_kode_matkul(conn, kode):
            flash(f'Kode Mata Kuliah {kode} sudah terdaftar!', 'danger')
            return redirect(url_for('tambah_matkul'))
            
        try:
            repo.tambah_data_matkul(conn, kode, nama, int(sks), int(smt))
            flash(f'Data Mata Kuliah {kode} berhasil ditambahkan!', 'success')
            return redirect(url_for('daftar_matkul'))
        except:
            flash('Gagal simpan. Pastikan SKS/Semester adalah angka.', 'danger')
            
    return render_template('tambah_matkul.html')

@app.route('/matkul/edit/<kode>', methods=['GET', 'POST'])
def edit_matkul(kode):
    if not session.get('logged_in'): return redirect(url_for('login'))
        
    conn = get_db()
    data = repo.cari_by_kode_matkul(conn, kode)
    if not data: return redirect(url_for('daftar_matkul'))

    if request.method == 'POST':
        nama_baru = request.form['nama_matkul']
        sks_baru = request.form['sks']
        semester_baru = request.form['semester']

        if not nama_baru:
            flash('Nama Mata Kuliah wajib diisi!', 'danger')
            return redirect(url_for('edit_matkul', kode=kode))
        
        try:
            sks_baru = int(sks_baru)
            semester_baru = int(semester_baru)
        except ValueError:
            flash('SKS dan Semester harus berupa angka!', 'danger')
            return redirect(url_for('edit_matkul', kode=kode))
            
        repo.ubah_data_matkul(conn, kode, nama_baru, sks_baru, semester_baru)
        flash(f'Data Mata Kuliah {kode} berhasil diubah!', 'warning')
        return redirect(url_for('daftar_matkul'))
        
    return render_template('edit_matkul.html', matkul=data)

@app.route('/matkul/hapus/<kode>', methods=['POST'])
def hapus_matkul(kode):
    # PROTEKSI ROUTE
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('login'))
        
    conn = get_db()
    success = repo.hapus_data_matkul(conn, kode)
    if success:
        flash(f'Data Mata Kuliah {kode} berhasil dihapus!', 'danger')
    else:
        flash(f'Gagal menghapus data Mata Kuliah {kode}.', 'danger')
        
    return redirect(url_for('daftar_matkul'))

# ----------------- ROUTE KRS -----------------

@app.route('/krs')
def daftar_krs_mahasiswa():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    conn = get_db()
    
    # Reuse `daftar_mahasiswa` repository function to list students
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    offset = (page - 1) * PER_PAGE
    
    data = repo.daftar_mahasiswa(conn, search_term=q, limit=PER_PAGE, offset=offset)
    total_data = repo.hitung_jumlah_mahasiswa(conn, search_term=q)
    total_pages = ceil(total_data / PER_PAGE)
    
    return render_template('krs_list.html', 
                           data=data, 
                           page=page, 
                           total_pages=total_pages, 
                           q=q, 
                           total_data=total_data,
                           PER_PAGE=PER_PAGE)

@app.route('/krs/manage/<nim>', methods=['GET', 'POST'])
def manage_krs(nim):
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    # --- PROTEKSI AKSES DATA ORANG LAIN ---
    if session.get('role') == 'Mahasiswa' and session.get('username') != nim:
        flash('Anda tidak memiliki izin mengakses data KRS mahasiswa lain.', 'danger')
        return redirect(url_for('manage_krs', nim=session.get('username')))
    # --------------------------------------
    
    conn = get_db()
    mahasiswa = repo.cari_by_nim(conn, nim)
    if not mahasiswa:
        flash('Data mahasiswa tidak ditemukan', 'danger')
        return redirect(url_for('daftar_krs_mahasiswa'))
        
    # Default semester/tahun (could be dynamic later)
    semester_aktif = request.args.get('semester', 1, type=int)
    tahun_ajaran_aktif = request.args.get('tahun_ajaran', '2023/2024')
    
    # List all available matkul
    semua_matkul = repo.daftar_matkul(conn, limit=1000) # Get all for dropdown
    
    # Get current KRS
    krs_data = repo.ambil_krs_mahasiswa(conn, nim, semester_aktif, tahun_ajaran_aktif)
    total_sks = repo.hitung_sks_krs(conn, nim, semester_aktif, tahun_ajaran_aktif)

    # Filter: Remove matkul that are already in KRS
    # Create a set of taken course codes for O(1) lookup
    taken_codes = {item['kode_matkul'] for item in krs_data}
    
    # Filter available courses
    matkul_tersedia = [mk for mk in semua_matkul if mk['kode_matkul'] not in taken_codes]
    
    # Add KRS Logic
    if request.method == 'POST':
        kode_matkul = request.form.get('kode_matkul')
        
        # Check if already taken
        if repo.cek_krs_exist(conn, nim, kode_matkul, semester_aktif, tahun_ajaran_aktif):
             flash('Mata kuliah sudah diambil.', 'warning')
             return redirect(url_for('manage_krs', nim=nim, semester=semester_aktif, tahun_ajaran=tahun_ajaran_aktif))
        
        # Check SKS Limit
        matkul_info = repo.cari_by_kode_matkul(conn, kode_matkul)
        if total_sks + matkul_info['sks'] > 24:
            flash(f'Gagal! Total SKS akan menjadi {total_sks + matkul_info["sks"]}. Maksimal 24 SKS.', 'danger')
        else:
            repo.tambah_krs(conn, nim, kode_matkul, semester_aktif, tahun_ajaran_aktif)
            flash('Mata kuliah berhasil ditambahkan ke KRS.', 'success')
            
        return redirect(url_for('manage_krs', nim=nim, semester=semester_aktif, tahun_ajaran=tahun_ajaran_aktif))

    # Payment Logic
    total_biaya = total_sks * HARGA_PER_SKS
    # Update/Create Bill automatically when viewing (so it's up to date)
    repo.buat_tagihan(conn, nim, semester_aktif, tahun_ajaran_aktif, total_sks, total_biaya)
    status_pembayaran = repo.cek_status_pembayaran(conn, nim, semester_aktif, tahun_ajaran_aktif)

    return render_template('krs_manage.html', 
                           mahasiswa=mahasiswa,
                           krs_data=krs_data,
                           total_sks=total_sks,
                           semua_matkul=matkul_tersedia,
                           semester_aktif=semester_aktif,
                           tahun_ajaran_aktif=tahun_ajaran_aktif,
                           total_biaya=total_biaya,
                           harga_per_sks=HARGA_PER_SKS,
                           status_pembayaran=status_pembayaran)

@app.route('/krs/bayar/<nim>', methods=['POST'])
def bayar_krs(nim):
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    conn = get_db()
    semester = request.form.get('semester', type=int)
    tahun_ajaran = request.form.get('tahun_ajaran')
    metode = request.form.get('metode_pembayaran')
    
    if not metode:
        flash('Pilih metode pembayaran!', 'danger')
        return redirect(url_for('manage_krs', nim=nim, semester=semester, tahun_ajaran=tahun_ajaran))
        
    repo.bayar_tagihan(conn, nim, semester, tahun_ajaran, metode)
    flash('Pembayaran berhasil dikonfirmasi!', 'success')
    return redirect(url_for('manage_krs', nim=nim, semester=semester, tahun_ajaran=tahun_ajaran))

@app.route('/krs/invoice/<int:id_pembayaran>')
def invoice_krs(id_pembayaran):
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    conn = get_db()
    pembayaran = repo.ambil_pembayaran_by_id(conn, id_pembayaran)
    
    if not pembayaran:
        flash('Data pembayaran tidak ditemukan.', 'danger')
        return redirect(url_for('daftar_krs_mahasiswa'))
        
    mahasiswa = repo.cari_by_nim(conn, pembayaran['nim'])
    
    # Get KRS details for this invoice context
    krs_data = repo.ambil_krs_mahasiswa(conn, pembayaran['nim'], pembayaran['semester'], pembayaran['tahun_ajaran'])
    
    return render_template('invoice.html', 
                           pembayaran=pembayaran, 
                           mahasiswa=mahasiswa,
                           krs_data=krs_data)

@app.route('/krs/hapus/<id_krs>', methods=['POST'])
def hapus_krs_item(id_krs):
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    conn = get_db()
    # Need to redirect back to manage page, so we need to know nim/semester. 
    # For simplicity, we might referer or store in session, but let's query the specific item first before deleting if we want to be precise, Or just redirect to KRS list if tricky.
    # Actually, let's use 'next' param or just redirect back to referrer
    
    repo.hapus_krs(conn, id_krs)
    flash('Mata kuliah dihapus dari KRS.', 'success')
    return redirect(request.referrer)

    return redirect(request.referrer)

# ----------------- ROUTE KHS (MAHASISWA) -----------------

@app.route('/mahasiswa/khs')
def lihat_khs():
    if not session.get('logged_in') or session.get('role') != 'Mahasiswa':
        return redirect(url_for('login'))
        
    conn = get_db()
    nim = session.get('username')
    
    # Filter
    semester = request.args.get('semester', 1, type=int)
    tahun = request.args.get('tahun', '2023/2024')
    
    data_khs = repo.ambil_khs(conn, nim, semester, tahun)
    mahasiswa = repo.cari_by_nim(conn, nim)
    
    # Hitung IP Semester (IPS) Sederhana
    total_sks = 0
    total_bobot = 0
    bobot_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    
    for mk in data_khs:
        if mk['nilai_huruf']:
            sks = mk['sks']
            bobot = bobot_map.get(mk['nilai_huruf'], 0)
            total_sks += sks
            total_bobot += (sks * bobot)
            
    ips = 0 if total_sks == 0 else round(total_bobot / total_sks, 2)
    
    return render_template('khs.html',
                           mahasiswa=mahasiswa,
                           data=data_khs,
                           semester=semester,
                           tahun=tahun,
                           ips=ips)

# ----------------- ROUTE PREVIEW/REPORT -----------------

@app.route('/preview', methods=['POST'])
def preview_report():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    conn = get_db()
    report_type = request.form.get('type')
    conn = get_db()
    report_type = request.form.get('type')
    selected_ids = list(set(request.form.getlist('selected_ids'))) # list of primary keys, deduped
    
    if not selected_ids:
        flash('Tidak ada data yang dipilih untuk dicetak.', 'warning')
        return redirect(request.referrer)
        
    data = []
    headers = []
    title = ""
    
    if report_type == 'mahasiswa':
        title = "Laporan Data Mahasiswa"
        headers = ['NIM', 'Nama', 'Alamat', 'Prodi']
        for nim in selected_ids:
            row = repo.cari_by_nim(conn, nim)
            if row: 
                data.append({'c1': row['nim'], 'c2': row['nama'], 'c3': row['alamat'], 'c4': row['prodi']})
            
    elif report_type == 'dosen':
        title = "Laporan Data Dosen"
        headers = ['NIP', 'Nama', 'Mata Kuliah Ajar', 'Telepon']
        for nip in selected_ids:
            row = repo.cari_by_nip(conn, nip)
            if row: 
                data.append({'c1': row['nip'], 'c2': row['nama'], 'c3': row['matkul_ajar'], 'c4': row['telepon']})

    elif report_type == 'matkul':
        title = "Laporan Data Mata Kuliah"
        headers = ['Kode', 'Nama Matkul', 'SKS', 'Semester']
        for kode in selected_ids:
            row = repo.cari_by_kode_matkul(conn, kode)
            if row: 
                data.append({'c1': row['kode_matkul'], 'c2': row['nama_matkul'], 'c3': row['sks'], 'c4': row['semester']})

    elif report_type == 'krs':
        title = "Laporan Data KRS Mahasiswa"
        # For KRS, selected_ids might be nimble enough? OR we might just print what is currently visible?
        # The prompt says "pratinjau laporan berdasarkan data yang di pilih dari tabel".
        # If we are in KRS List page, we select Students. So we print KRS for those students.
        headers = ['NIM', 'Nama', 'Total SKS', 'Jumlah Matkul']
        for nim in selected_ids:
            mhs = repo.cari_by_nim(conn, nim)
            if mhs:
                # We need to calculate SKS and count matkul for this student
                # Use a fixed semester/year for now or aggregate?
                # Let's assume current active semester for report, or just general info.
                # Simplification: Print Student info + Summary of KRS
                # Actually, maybe we should print the list of courses for each student?
                # For a simple table report, let's just show summary.
                # If user wants detailed KRS, they go to manage.
                # BUT, maybe the user wants to print the ACTUAL KRS (List of courses) for a student?
                # Let's stick to the table structure: One row per selected item.
                # So Row = Student with KRS summary.
                
                # We need to default semester/year. Let's pick 1 and 2023/2024 as default or sum all?
                # Let's sum all compatible with current logic.
                # To make it robust, let's just show Mahasiswa info in context of KRS.
                
                # Wait, "preview print" for KRS might mean "Print the KRS Card".
                # If I select multiple students, do I get multiple KRS cards? 
                # Or a list of students who have filled KRS?
                # Given "tabel data", I assume it's the list of students in the KRS menu.
                sks = repo.hitung_sks_krs(conn, nim, 1, '2023/2024') # Example default
                krs_items = repo.ambil_krs_mahasiswa(conn, nim, 1, '2023/2024')
                count = len(krs_items)
                data.append({'c1': mhs['nim'], 'c2': mhs['nama'], 'c3': sks, 'c4': count})
        
    return render_template('preview_print.html', 
                           title=title, 
                           headers=headers, 
                           data=data)