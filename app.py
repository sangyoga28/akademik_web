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
PER_PAGE = 10 # Konstanta jumlah data per halaman
HARGA_PER_SKS = 150000 # Harga per SKS

# ----------------- SETUP KONEKSI DB -----------------

def get_db():
    return repo.get_db()

@app.context_processor
def inject_totals():
    if session.get('logged_in') and session.get('role') == 'Admin Sistem':
        try:
            conn = get_db()
            count = repo.hitung_pendaftaran_pending(conn)
            return dict(nav_total_pending=count)
        except:
            pass
    return dict(nav_total_pending=0)

@app.teardown_appcontext
def close_connection(exception):
    repo.close_connection(exception)
    
# Inisialisasi DB saat startup (Hanya buat tabel)
with app.app_context():
    conn = get_db()
    repo.buat_tabel(conn)
    # Seeding dilakukan secara terpisah melalui reset_and_seed.py

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

# ----------------- ROUTE PENDAFTARAN (PUBLIK) -----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('logged_in'):
        return redirect(url_for('index'))
        
    conn = get_db()
    if request.method == 'POST':
        role = request.form.get('role')
        nama = request.form.get('nama')
        password = request.form.get('password')
        alamat = request.form.get('alamat')
        telepon = request.form.get('telepon')
        
        # Mahasiswa specific
        prodi = request.form.get('prodi')
        fakultas = request.form.get('fakultas')
        
        # Dosen specific
        matkul_ajar = request.form.get('matkul_ajar')
        
        if not nama or not password:
            flash('Nama dan Password wajib diisi!', 'danger')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        
        try:
            repo.tambah_pendaftaran(conn, nama, role, alamat, prodi, fakultas, telepon, matkul_ajar, hashed_pw)
            flash('Pendaftaran berhasil! Tunggu persetujuan admin untuk mendapatkan NIM/NIP.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Gagal mendaftar: {str(e)}', 'danger')
            
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    daftar_fakultas = repo.ambil_daftar_fakultas(conn)
    matkul_list = repo.ambil_semua_matkul_untuk_dosen(conn)
    
    return render_template('register.html', 
                           daftar_prodi=daftar_prodi,
                           daftar_fakultas=daftar_fakultas,
                           matkul_list=matkul_list)

    return render_template('pendaftaran_status.html', status_data=status_data)

@app.route('/pendaftaran/status', methods=['GET', 'POST'])
def pendaftaran_status():
    status_data = None
    if request.method == 'POST':
        nama = request.form.get('nama')
        telepon = request.form.get('telepon')
        conn = get_db()
        status_data = repo.cek_status_pendaftaran_user(conn, nama, telepon)
        if not status_data:
            flash('Data pendaftaran tidak ditemukan. Pastikan Nama dan No. Telepon sesuai.', 'warning')
            
    return render_template('pendaftaran_status.html', status_data=status_data)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if session.get('logged_in'):
        return redirect(url_for('index'))
        
    verified = False
    verified_username = None
    
    if request.method == 'POST':
        step = request.form.get('step')
        
        if step == 'verify':
            username = request.form.get('username')
            telepon = request.form.get('telepon')
            
            conn = get_db()
            is_valid, role = repo.verifikasi_identitas_user(conn, username, telepon)
            
            if is_valid:
                verified = True
                verified_username = username
                flash(f'Identitas {role} berhasil diverifikasi. Silakan masukkan kata sandi baru.', 'success')
            else:
                flash('Verifikasi gagal. Username atau Nomor Telepon tidak cocok.', 'danger')
                
        elif step == 'reset':
            username = request.form.get('username')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if new_password != confirm_password:
                flash('Konfirmasi kata sandi tidak cocok!', 'danger')
                return render_template('reset_password.html', verified=True, verified_username=username)
                
            conn = get_db()
            hashed_pw = generate_password_hash(new_password, method='pbkdf2:sha256')
            if repo.update_user_password(conn, username, hashed_pw):
                flash('Kata sandi berhasil diperbarui! Silakan login dengan kata sandi baru.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Gagal memperbarui kata sandi.', 'danger')
                
    return render_template('reset_password.html', verified=verified, verified_username=verified_username)

@app.route('/api/prodi/<fakultas>')
def api_prodi(fakultas):
    conn = get_db()
    prodi_list = repo.ambil_prodi_by_fakultas(conn, fakultas)
    return {"prodi": prodi_list}

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
        total_pending = repo.hitung_pendaftaran_pending(conn)
        
        return render_template('home.html',
            total_mahasiswa=total_mahasiswa,
            total_dosen=total_dosen,
            total_matkul=total_matkul,
            total_pending=total_pending
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
    
    # Ambil parameter halaman (page), pencarian (q), fakultas, dan prodi
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    fakultas = request.args.get('fakultas', '')
    prodi = request.args.get('prodi', '')
    
    # Hitung offset untuk database
    offset = (page - 1) * PER_PAGE
    
    # Ambil data dengan limit dan offset
    data = repo.daftar_mahasiswa(conn, search_term=q, fakultas=fakultas, prodi=prodi, limit=PER_PAGE, offset=offset)
    
    # Hitung total data dan total halaman
    total_data = repo.hitung_jumlah_mahasiswa(conn, search_term=q, fakultas=fakultas, prodi=prodi)
    total_pages = ceil(total_data / PER_PAGE)
    
    # Dropdown data
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    daftar_fakultas = repo.ambil_daftar_fakultas(conn)
    
    # Jika hasil pencarian kosong, tampilkan notifikasi
    if (q or fakultas or prodi) and not data and total_data == 0:
        flash(f"Tidak ada data Mahasiswa yang ditemukan.", 'info')

    return render_template('mahasiswa.html', 
                           data=data, 
                           page=page, 
                           total_pages=total_pages, 
                           q=q, 
                           fakultas=fakultas,
                           prodi=prodi,
                           daftar_prodi=daftar_prodi,
                           daftar_fakultas=daftar_fakultas,
                           total_data=total_data,
                           PER_PAGE=PER_PAGE)

@app.route('/mahasiswa/tambah', methods=['GET', 'POST'])
def tambah_mahasiswa():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    conn = get_db()
        
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        alamat = request.form['alamat']
        prodi = request.form['prodi']
        fakultas = request.form['fakultas']
        telepon = request.form['telepon']
        
        if not nim or not nama:
            flash('NIM dan Nama wajib diisi!', 'danger')
            return redirect(url_for('tambah_mahasiswa'))
            
        if repo.cari_by_nim(conn, nim):
            flash(f'NIM {nim} sudah terdaftar!', 'danger')
            return redirect(url_for('tambah_mahasiswa'))
            
        try:
            # 1. Tambah Biodata
            repo.tambah_data_mahasiswa(conn, nim, nama, alamat, prodi, fakultas, telepon)
            
            # 2. Buat Akun Login Otomatis (Default Pass: NIM)
            if repo.cari_user_by_username(conn, nim) is None:
                hashed_pw = generate_password_hash(nim, method='pbkdf2:sha256')
                repo.tambah_user(conn, nim, hashed_pw, role='Mahasiswa')
                msg = f'Data {nim} disimpan & Akun Login dibuat.'
            else:
                msg = f'Data {nim} disimpan (Akun sudah ada).'
            
            flash(msg, 'success')
            return redirect(url_for('daftar_mahasiswa'))
        except Exception as e:
            flash(f'Gagal menyimpan: {str(e)}', 'danger')
            return redirect(url_for('tambah_mahasiswa'))
    
    # GET: Kirim data untuk dropdown
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    daftar_fakultas = repo.ambil_daftar_fakultas(conn)
    
    return render_template('tambah_mahasiswa.html', 
                          daftar_prodi=daftar_prodi,
                          daftar_fakultas=daftar_fakultas)

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
        fakultas_baru = request.form['fakultas']
        telepon_baru = request.form['telepon']

        if not nama_baru:
            flash('Nama wajib diisi!', 'danger')
            return redirect(url_for('edit_mahasiswa', nim=nim))
            
        try:
            repo.ubah_data_mahasiswa(conn, nim, nama_baru, alamat_baru, prodi_baru, fakultas_baru, telepon_baru)
            flash(f'Data Mahasiswa {nim} berhasil diubah!', 'success')
        except Exception as e:
            flash(f'Gagal mengubah data: {e}', 'danger')
            
        return redirect(url_for('daftar_mahasiswa'))
    
    # GET: Kirim data untuk dropdown
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    daftar_fakultas = repo.ambil_daftar_fakultas(conn)
        
    return render_template('edit_mahasiswa.html', 
                          mhs=data,
                          daftar_prodi=daftar_prodi,
                          daftar_fakultas=daftar_fakultas)

@app.route('/mahasiswa/hapus/<nim>', methods=['POST'])
def hapus_mahasiswa(nim):
    if not session.get('logged_in'): return redirect(url_for('login'))
        
    conn = get_db()
    
    # Hapus Data Mahasiswa
    success = repo.hapus_data_mahasiswa(conn, nim)
    
    if success:
        # --- HAPUS JUGA AKUN LOGIN ---
        repo.hapus_user(conn, username=nim)
        # --- HAPUS DATA PENDAFTARAN (CLEAN TRACE) ---
        repo.hapus_pendaftaran_by_nim_nip(conn, nim)
        flash(f'Data Mahasiswa {nim}, akun login, dan riwayat pendaftaran berhasil dihapus!', 'danger')
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
    
    # Ambil parameter halaman (page), pencarian (q), prodi, dan fakultas
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    prodi = request.args.get('prodi', '')
    fakultas = request.args.get('fakultas', '') # Added for consistency though join logic needs care
    
    # Hitung offset untuk database
    offset = (page - 1) * PER_PAGE
    
    # Ambil data dengan limit dan offset
    data = repo.daftar_dosen(conn, search_term=q, fakultas=fakultas, prodi=prodi, limit=PER_PAGE, offset=offset)
    
    # Hitung total data dan total halaman
    total_data = repo.hitung_jumlah_dosen(conn, search_term=q, fakultas=fakultas, prodi=prodi)
    total_pages = ceil(total_data / PER_PAGE)
    
    # Ambil daftar prodi & fakultas untuk dropdown filter
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    daftar_fakultas = repo.ambil_daftar_fakultas(conn)
    
    # Jika hasil pencarian kosong, tampilkan notifikasi
    if (q or prodi or fakultas) and not data and total_data == 0:
        flash(f"Tidak ada data Dosen yang ditemukan.", 'info')

    return render_template('dosen.html', 
                           data=data, 
                           page=page, 
                           total_pages=total_pages, 
                           q=q, 
                           prodi=prodi,
                           fakultas=fakultas,
                           daftar_prodi=daftar_prodi,
                           daftar_fakultas=daftar_fakultas,
                           total_data=total_data,
                           PER_PAGE=PER_PAGE)
                           
@app.route('/dosen/tambah', methods=['GET', 'POST'])
def tambah_dosen():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    conn = get_db()
        
    if request.method == 'POST':
        nip = request.form['nip']
        nama = request.form['nama']
        matkul_ajar = request.form['matkul_ajar']
        telepon = request.form['telepon']
        
        if not nip or not nama:
            flash('NIP dan Nama wajib diisi!', 'danger')
            return redirect(url_for('tambah_dosen'))
            
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
    
    # GET: Kirim daftar mata kuliah untuk dropdown
    matkul_list = repo.ambil_semua_matkul_untuk_dosen(conn)
            
    return render_template('tambah_dosen.html', matkul_list=matkul_list)

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
    
    # GET: Kirim daftar mata kuliah untuk dropdown
    matkul_list = repo.ambil_semua_matkul_untuk_dosen(conn)
        
    return render_template('edit_dosen.html', 
                          dosen=data,
                          matkul_list=matkul_list)

@app.route('/dosen/hapus/<nip>', methods=['POST'])
def hapus_dosen(nip):
    if not session.get('logged_in'): return redirect(url_for('login'))
        
    conn = get_db()
    success = repo.hapus_data_dosen(conn, nip)
    if success:
        # --- HAPUS JUGA AKUN LOGIN ---
        repo.hapus_user(conn, username=nip)
        # --- HAPUS DATA PENDAFTARAN (CLEAN TRACE) ---
        repo.hapus_pendaftaran_by_nim_nip(conn, nip)
        flash(f'Data Dosen {nip}, akun login, dan riwayat pendaftaran berhasil dihapus!', 'danger')
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

# --- NEW: INPUT NILAI PER MAHASISWA (ADMIN) ---
@app.route('/admin/nilai/mahasiswa')
def admin_nilai_mahasiswa_list():
    if not session.get('logged_in') or session.get('role') != 'Admin Sistem':
        return redirect(url_for('login'))
        
    conn = get_db()
    
    # Filter Params
    semester = request.args.get('semester', 1, type=int)
    tahun_ajaran = request.args.get('tahun_ajaran', '2023/2024')
    prodi = request.args.get('prodi', '')
    
    # Get Students
    mahasiswa_list = repo.daftar_mahasiswa(conn, prodi=prodi, limit=1000)
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    
    return render_template('admin_nilai_mahasiswa_list.html',
                           mahasiswa_list=mahasiswa_list,
                           semester=semester,
                           tahun_ajaran=tahun_ajaran,
                           prodi=prodi,
                           daftar_prodi=daftar_prodi)

@app.route('/admin/nilai/input/mahasiswa/<nim>', methods=['GET', 'POST'])
def input_nilai_mahasiswa(nim):
    if not session.get('logged_in') or session.get('role') != 'Admin Sistem':
        return redirect(url_for('login'))
        
    conn = get_db()
    semester = request.args.get('semester', 1, type=int)
    tahun_ajaran = request.args.get('tahun_ajaran', '2023/2024')
    
    mahasiswa = repo.cari_by_nim(conn, nim)
    if not mahasiswa:
        flash('Mahasiswa tidak ditemukan', 'danger')
        return redirect(url_for('admin_nilai_mahasiswa_list'))
        
    if request.method == 'POST':
        # Loop form items starting with nilai_angka_{id_krs}
        count = 0
        for key, val in request.form.items():
            if key.startswith('nilai_angka_'):
                id_krs = key.split('_')[2]
                try:
                    if val and val.strip() != "":
                        nilai_angka = float(val)
                        nilai_huruf = konversi_nilai(nilai_angka)
                        repo.simpan_nilai(conn, id_krs, nilai_angka, nilai_huruf)
                        count += 1
                except ValueError:
                    pass
        
        flash(f'Berhasil menyimpan {count} nilai untuk {mahasiswa["nama"]}.', 'success')
        return redirect(url_for('input_nilai_mahasiswa', nim=nim, semester=semester, tahun_ajaran=tahun_ajaran))
    
    # Get KRS data which includes courses taken by this student
    # Note: repo.ambil_krs_mahasiswa returns joined data including nilai_angka
    krs_data = repo.ambil_krs_mahasiswa(conn, nim, semester, tahun_ajaran)
    
    return render_template('admin_input_nilai_mahasiswa.html',
                           mahasiswa=mahasiswa,
                           krs_data=krs_data,
                           semester=semester,
                           tahun_ajaran=tahun_ajaran)

@app.route('/dosen/nilai', methods=['GET', 'POST'])
def dosen_nilai_dashboard():
    if not session.get('logged_in') or session.get('role') not in ['Dosen', 'Admin Sistem']:
        return redirect(url_for('login'))
    
    conn = get_db()
    
    # Filter by prodi and semester
    semester = request.args.get('semester', 1, type=int)
    tahun_ajaran = request.args.get('tahun_ajaran', '2023/2024')
    prodi_filter = request.args.get('prodi', '')
    
    # Ambil daftar mata kuliah berdasarkan hak akses
    if session.get('role') == 'Dosen':
        # Dosen hanya boleh lihat MK yang dia ajar
        nip_dosen = session.get('username')
        dosen_profile = repo.cari_by_nip(conn, nip_dosen)
        matkul_diampu = dosen_profile['matkul_ajar'] if dosen_profile else None
        
        # Ambil matkul dengan filter
        semua_mk = repo.daftar_matkul(conn, prodi=prodi_filter, semester=semester, limit=1000)
        # Filter berdasarkan NAMA matkul yang cocok dengan data profile dosen
        daftar_matkul = [mk for mk in semua_mk if mk['nama_matkul'] == matkul_diampu]
    else:
        # Admin / Lainnya bisa lihat semua sesuai filter
        daftar_matkul = repo.daftar_matkul(conn, prodi=prodi_filter, semester=semester, limit=1000)
    
    # Kategorikan mata kuliah sesuai prodi
    matkul_per_prodi = {}
    for mk in daftar_matkul:
        p = mk['prodi'] or 'Lainnya'
        if p not in matkul_per_prodi:
            matkul_per_prodi[p] = []
        matkul_per_prodi[p].append(mk)
    
    return render_template('dosen_nilai_dashboard.html', 
                           matkul_list=daftar_matkul,
                           matkul_per_prodi=matkul_per_prodi,
                           semester=semester,
                           tahun_ajaran=tahun_ajaran,
                           prodi_filter=prodi_filter,
                           daftar_prodi=repo.ambil_daftar_prodi(conn))

@app.route('/dosen/nilai/input/<kode_matkul>', methods=['GET', 'POST'])
def input_nilai(kode_matkul):
    if not session.get('logged_in') or session.get('role') not in ['Dosen', 'Admin Sistem']:
        return redirect(url_for('login'))
        
    conn = get_db()
    semester = request.args.get('semester', 1, type=int)
    tahun_ajaran = request.args.get('tahun_ajaran', '2023/2024')
    
    matkul = repo.cari_by_kode_matkul(conn, kode_matkul)
    
    # --- SECURITY CHECK ---
    # Pastikan Dosen tidak "nembak" URL matkul orang lain
    if session.get('role') == 'Dosen':
        nip_dosen = session.get('username')
        dosen_profile = repo.cari_by_nip(conn, nip_dosen)
        matkul_diampu = dosen_profile['matkul_ajar'] if dosen_profile else None
        
        if not matkul or matkul['nama_matkul'] != matkul_diampu:
            flash(f'Anda tidak memiliki akses untuk menilai mata kuliah "{matkul["nama_matkul"] if matkul else kode_matkul}".', 'danger')
            return redirect(url_for('dosen_nilai_dashboard', semester=semester, tahun_ajaran=tahun_ajaran))
    # ----------------------
    
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
        return redirect(url_for('input_nilai', kode_matkul=kode_matkul, semester=semester, tahun_ajaran=tahun_ajaran))
    
    mahasiswa_list = repo.ambil_mahasiswa_kelas(conn, kode_matkul, semester, tahun_ajaran)
    
    return render_template('input_nilai.html', 
                           matkul=matkul,
                           mahasiswa_list=mahasiswa_list,
                           semester=semester,
                           tahun_ajaran=tahun_ajaran)

@app.route('/mahasiswa/krs/tambah_bulk', methods=['POST'])
def tambah_krs_bulk():
    if not session.get('logged_in') or session.get('role') != 'Mahasiswa':
        return redirect(url_for('login'))
        
    nim = session.get('username')
    semester = request.form.get('semester', type=int)
    tahun_ajaran = request.form.get('tahun_ajaran')
    
    if not semester or not tahun_ajaran:
        flash('Semester dan Tahun Ajaran tidak valid.', 'danger')
        return redirect(url_for('manage_krs', nim=nim))
        
    conn = get_db()
    success, message = repo.tambah_krs_bulk(conn, nim, semester, tahun_ajaran)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
        
    return redirect(url_for('manage_krs', nim=nim, semester=semester, tahun_ajaran=tahun_ajaran))

@app.route('/mahasiswa/krs/cetak')
def cetak_krs():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    conn = get_db()
    nim = request.args.get('nim') or session.get('username')
    semester = request.args.get('semester', 1, type=int)
    tahun_ajaran = request.args.get('tahun_ajaran', '2023/2024')
    
    # Security check for Students
    if session.get('role') == 'Mahasiswa' and session.get('username') != nim:
        return redirect(url_for('index'))
        
    mahasiswa = repo.cari_by_nim(conn, nim)
    krs_data = repo.ambil_krs_mahasiswa(conn, nim, semester, tahun_ajaran)
    total_sks = repo.hitung_sks_krs(conn, nim, semester, tahun_ajaran)
    
    import datetime
    # Format: 22 Desember 2025
    bulan_indo = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni',
        7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    today = datetime.date.today()
    current_date = f"{today.day} {bulan_indo[today.month]} {today.year}"
    
    return render_template('cetak_krs.html',
                           mahasiswa=mahasiswa,
                           krs_data=krs_data,
                           semester=semester,
                           tahun_ajaran=tahun_ajaran,
                           total_sks=total_sks,
                           current_date=current_date,
                           auto_print=True)

@app.route('/matkul')
def daftar_matkul():
    # PROTEKSI ROUTE
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('login'))
        
    conn = get_db()

    # Ambil parameter halaman (page), pencarian (q), prodi, dan semester dari URL
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    prodi = request.args.get('prodi', '')
    semester = request.args.get('semester', '', type=str)

    # Hitung offset untuk database
    offset = (page - 1) * PER_PAGE
    
    # Ambil data dengan limit dan offset
    data = repo.daftar_matkul(conn, search_term=q, prodi=prodi, semester=semester, limit=PER_PAGE, offset=offset)
    
    # Hitung total data dan total halaman
    total_data = repo.hitung_jumlah_matkul(conn, search_term=q, prodi=prodi, semester=semester)
    total_pages = ceil(total_data / PER_PAGE)
    
    # Daftar prodi untuk dropdown filter
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    
    # Jika hasil pencarian kosong, tampilkan notifikasi
    if (q or prodi or semester) and not data and total_data == 0:
        flash(f"Tidak ada data Mata Kuliah yang ditemukan.", 'info')

    return render_template('matkul.html', 
                           data=data, 
                           page=page, 
                           total_pages=total_pages, 
                           q=q, 
                           prodi=prodi,
                           semester=semester,
                           daftar_prodi=daftar_prodi,
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
        prodi = request.form.get('prodi')

        if not kode or not nama:
            flash('Kode dan Nama Mata Kuliah wajib diisi!', 'danger')
            return redirect(url_for('tambah_matkul'))
            
        conn = get_db()
        if repo.cari_by_kode_matkul(conn, kode):
            flash(f'Kode Mata Kuliah {kode} sudah terdaftar!', 'danger')
            return redirect(url_for('tambah_matkul'))
            
        try:
            repo.tambah_data_matkul(conn, kode, nama, int(sks), int(smt), prodi)
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
        prodi_baru = request.form.get('prodi')

        if not nama_baru:
            flash('Nama Mata Kuliah wajib diisi!', 'danger')
            return redirect(url_for('edit_matkul', kode=kode))
        
        try:
            sks_baru = int(sks_baru)
            semester_baru = int(semester_baru)
        except ValueError:
            flash('SKS dan Semester harus berupa angka!', 'danger')
            return redirect(url_for('edit_matkul', kode=kode))
            
        repo.ubah_data_matkul(conn, kode, nama_baru, sks_baru, semester_baru, prodi_baru)
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
    
    # Filter available courses by Student's Prodi AND Semester
    # This addresses the user's request to restrict courses by major and semester
    matkul_tersedia = [
        mk for mk in semua_matkul 
        if mk['kode_matkul'] not in taken_codes and 
           (mk['prodi'] == mahasiswa['prodi'] or mk['prodi'] == 'Umum' or not mk['prodi']) and
           mk['semester'] == semester_aktif
    ]
    
    # Add KRS Logic
    if request.method == 'POST':
        kode_matkul = request.form.get('kode_matkul')
        
        if kode_matkul == 'ALL':
            success, message = repo.tambah_krs_bulk(conn, nim, semester_aktif, tahun_ajaran_aktif)
            if success:
                flash(message, 'success')
            else:
                flash(message, 'danger')
            return redirect(url_for('manage_krs', nim=nim, semester=semester_aktif, tahun_ajaran=tahun_ajaran_aktif))

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
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    conn = get_db()
    
    # Akses NIM: Mahasiswa ambil dari session, Admin/Dosen bisa ambil dari parameter
    if session.get('role') in ['Admin Sistem', 'Dosen']:
        nim = request.args.get('nim')
        if not nim:
            flash('NIM harus ditentukan.', 'warning')
            return redirect(url_for('index'))
    else:
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

@app.route('/mahasiswa/khs/cetak')
def cetak_khs():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    conn = get_db()
    nim = request.args.get('nim') or session.get('username')
    semester = request.args.get('semester', 1, type=int)
    tahun = request.args.get('tahun', '2023/2024')
    
    data_khs = repo.ambil_khs(conn, nim, semester, tahun)
    mahasiswa = repo.cari_by_nim(conn, nim)
    
    # Hitung IPS
    total_sks = 0
    total_bobot = 0
    bobot_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    for mk in data_khs:
        if mk['nilai_huruf']:
            total_sks += mk['sks']
            total_bobot += (mk['sks'] * bobot_map.get(mk['nilai_huruf'], 0))
    ips = 0 if total_sks == 0 else round(total_bobot / total_sks, 2)
    
    import datetime
    current_date = datetime.date.today().strftime('%d %B %Y')
    
    return render_template('cetak_khs.html',
                           mahasiswa=mahasiswa,
                           data=data_khs,
                           semester=semester,
                           tahun=tahun,
                           ips=ips,
                           current_date=current_date,
                           auto_print=True)

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

# ----------------- ROUTE ADMIN: KELOLA PENDAFTARAN -----------------

@app.route('/admin/pendaftaran')
def admin_pendaftaran():
    if not session.get('role') == 'Admin Sistem':
        return redirect(url_for('login'))
        
    conn = get_db()
    
    # Filters
    role_filter = request.args.get('role', '')
    prodi_filter = request.args.get('prodi', '')
    
    data = repo.ambil_pendaftaran_pending(conn, role=role_filter, prodi=prodi_filter)
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    
    return render_template('admin_pendaftaran.html', 
                           data=data,
                           role_filter=role_filter,
                           prodi_filter=prodi_filter,
                           daftar_prodi=daftar_prodi)

@app.route('/admin/pendaftaran/approve/<int:id_pendaftaran>')
def approve_pendaftaran(id_pendaftaran):
    if not session.get('role') == 'Admin Sistem':
        return redirect(url_for('login'))
        
    conn = get_db()
    p = repo.ambil_pendaftaran_by_id(conn, id_pendaftaran)
    
    if not p:
        flash('Data pendaftaran tidak ditemukan.', 'danger')
        return redirect(url_for('admin_pendaftaran'))
        
    try:
        if p['role'] == 'Mahasiswa':
            new_id = repo.generate_nim_baru(conn)
            # Pass telepon from pendaftaran
            repo.tambah_data_mahasiswa(conn, new_id, p['nama'], p['alamat'], p['prodi'], p['fakultas'], p['telepon'])
            repo.tambah_user(conn, new_id, p['password_hash'], role='Mahasiswa')
            msg = f"Pendaftaran {p['nama']} disetujui. NIM: {new_id}"
        else:
            new_id = repo.generate_nip_baru(conn)
            repo.tambah_data_dosen(conn, new_id, p['nama'], p['matkul_ajar'], p['telepon'])
            repo.tambah_user(conn, new_id, p['password_hash'], role='Dosen')
            msg = f"Pendaftaran {p['nama']} disetujui. NIP: {new_id}"
            
        repo.update_status_pendaftaran(conn, id_pendaftaran, 'Approved')
        repo.update_nim_nip_pendaftaran(conn, id_pendaftaran, new_id)
        flash(msg, 'success')
    except Exception as e:
        flash(f'Gagal menyetujui: {str(e)}', 'danger')
        
    return redirect(url_for('admin_pendaftaran'))

@app.route('/admin/pendaftaran/reject/<int:id_pendaftaran>')
def reject_pendaftaran(id_pendaftaran):
    if not session.get('role') == 'Admin Sistem':
        return redirect(url_for('login'))
        
    conn = get_db()
    repo.update_status_pendaftaran(conn, id_pendaftaran, 'Rejected')
    flash('Pendaftaran ditolak.', 'warning')
    return redirect(url_for('admin_pendaftaran'))