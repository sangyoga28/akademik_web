from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import repository as repo
from . import auth_bp
from .general import get_db

# ----------------- ROUTE LOGIN & LOGOUT -----------------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('general.index'))
        
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
            return redirect(url_for('general.index'))
        else:
            flash('Login gagal. Periksa username dan password Anda.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear() # Hapus semua sesi
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('auth.login'))

# ----------------- ROUTE PENDAFTARAN (PUBLIK) -----------------

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('logged_in'):
        return redirect(url_for('general.index'))
        
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
            return redirect(url_for('auth.register'))
            
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        
        try:
            repo.tambah_pendaftaran(conn, nama, role, alamat, prodi, fakultas, telepon, matkul_ajar, hashed_pw)
            flash('Pendaftaran berhasil! Tunggu persetujuan admin untuk mendapatkan NIM/NIP.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Gagal mendaftar: {str(e)}', 'danger')
            
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    daftar_fakultas = repo.ambil_daftar_fakultas(conn)
    matkul_list = repo.ambil_semua_matkul_untuk_dosen(conn)
    
    return render_template('register.html', 
                           daftar_prodi=daftar_prodi,
                           daftar_fakultas=daftar_fakultas,
                           matkul_list=matkul_list)

@auth_bp.route('/pendaftaran/status', methods=['GET', 'POST'])
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

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if session.get('logged_in'):
        return redirect(url_for('general.index'))
        
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
                return redirect(url_for('auth.login'))
            else:
                flash('Gagal memperbarui kata sandi.', 'danger')
                
    return render_template('reset_password.html', verified=verified, verified_username=verified_username)
