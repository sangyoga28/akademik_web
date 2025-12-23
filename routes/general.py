from flask import render_template, redirect, url_for, session, flash, g
import repository as repo
from . import general_bp

# ----------------- SETUP KONEKSI DB -----------------

def get_db():
    return repo.get_db()

# ----------------- ROUTE UTAMA -----------------

@general_bp.route('/')
def index():
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('auth.login'))
        
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
        return redirect(url_for('mahasiswa.manage_krs', nim=session.get('username')))
        
    # Jika Dosen, redirect atau tampilkan dashboard simple
    elif role == 'Dosen':
        return render_template('home.html', 
                               total_mahasiswa=0, total_dosen=0, total_matkul=0) # Dummy data agar tidak error
    
    return render_template('home.html')

@general_bp.route('/api/prodi/<fakultas>')
def api_prodi(fakultas):
    conn = get_db()
    prodi_list = repo.ambil_prodi_by_fakultas(conn, fakultas)
    return {"prodi": prodi_list}
