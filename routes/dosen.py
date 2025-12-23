from flask import render_template, redirect, url_for, request, flash, session
import repository as repo
from math import ceil
from . import dosen_bp
from .general import get_db

PER_PAGE = 10

def konversi_nilai(angka):
    if angka >= 85: return 'A'
    elif angka >= 75: return 'B'
    elif angka >= 60: return 'C'
    elif angka >= 50: return 'D'
    else: return 'E'

# ----------------- ROUTE DOSEN -----------------

@dosen_bp.route('/dosen')
def daftar_dosen():
    # PROTEKSI ROUTE
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('auth.login'))

    conn = get_db()
    
    # Ambil parameter halaman (page), pencarian (q), prodi, dan fakultas
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    prodi = request.args.get('prodi', '')
    fakultas = request.args.get('fakultas', '') 
    
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

# ----------------- ROUTE PENILAIAN (DOSEN) -----------------

@dosen_bp.route('/dosen/nilai', methods=['GET', 'POST'])
def dosen_nilai_dashboard():
    if not session.get('logged_in') or session.get('role') not in ['Dosen', 'Admin Sistem']:
        return redirect(url_for('auth.login'))
    
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

@dosen_bp.route('/dosen/nilai/input/<kode_matkul>', methods=['GET', 'POST'])
def input_nilai(kode_matkul):
    if not session.get('logged_in') or session.get('role') not in ['Dosen', 'Admin Sistem']:
        return redirect(url_for('auth.login'))
        
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
            return redirect(url_for('dosen.dosen_nilai_dashboard', semester=semester, tahun_ajaran=tahun_ajaran))
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
        return redirect(url_for('dosen.input_nilai', kode_matkul=kode_matkul, semester=semester, tahun_ajaran=tahun_ajaran))
    
    mahasiswa_list = repo.ambil_mahasiswa_kelas(conn, kode_matkul, semester, tahun_ajaran)
    
    return render_template('input_nilai.html', 
                           matkul=matkul,
                           mahasiswa_list=mahasiswa_list,
                           semester=semester,
                           tahun_ajaran=tahun_ajaran)
