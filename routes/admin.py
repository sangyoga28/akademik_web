from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash
from math import ceil
import repository as repo
from . import admin_bp
from .dosen import konversi_nilai
from .general import get_db

PER_PAGE = 10

# ----------------- ADMIN PENDAFTARAN -----------------

@admin_bp.route('/admin/pendaftaran')
def admin_pendaftaran():
    if not session.get('role') == 'Admin Sistem':
        return redirect(url_for('auth.login'))
        
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

@admin_bp.route('/admin/pendaftaran/approve/<int:id_pendaftaran>')
def approve_pendaftaran(id_pendaftaran):
    if not session.get('role') == 'Admin Sistem':
        return redirect(url_for('auth.login'))
        
    conn = get_db()
    p = repo.ambil_pendaftaran_by_id(conn, id_pendaftaran)
    
    if not p:
        flash('Data pendaftaran tidak ditemukan.', 'danger')
        return redirect(url_for('admin.admin_pendaftaran'))
        
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
        
    return redirect(url_for('admin.admin_pendaftaran'))

@admin_bp.route('/admin/pendaftaran/reject/<int:id_pendaftaran>')
def reject_pendaftaran(id_pendaftaran):
    if not session.get('role') == 'Admin Sistem':
        return redirect(url_for('auth.login'))
        
    conn = get_db()
    repo.update_status_pendaftaran(conn, id_pendaftaran, 'Rejected')
    flash('Pendaftaran ditolak.', 'warning')
    return redirect(url_for('admin.admin_pendaftaran'))

# ----------------- ADMIN INPUT NILAI -----------------

@admin_bp.route('/admin/nilai/mahasiswa')
def admin_nilai_mahasiswa_list():
    if not session.get('logged_in') or session.get('role') != 'Admin Sistem':
        return redirect(url_for('auth.login'))
        
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

@admin_bp.route('/admin/nilai/input/mahasiswa/<nim>', methods=['GET', 'POST'])
def input_nilai_mahasiswa(nim):
    if not session.get('logged_in') or session.get('role') != 'Admin Sistem':
        return redirect(url_for('auth.login'))
        
    conn = get_db()
    semester = request.args.get('semester', 1, type=int)
    tahun_ajaran = request.args.get('tahun_ajaran', '2023/2024')
    
    mahasiswa = repo.cari_by_nim(conn, nim)
    if not mahasiswa:
        flash('Mahasiswa tidak ditemukan', 'danger')
        return redirect(url_for('admin.admin_nilai_mahasiswa_list'))
        
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
        return redirect(url_for('admin.input_nilai_mahasiswa', nim=nim, semester=semester, tahun_ajaran=tahun_ajaran))
    
    # Get KRS data which includes courses taken by this student
    # Note: repo.ambil_krs_mahasiswa returns joined data including nilai_angka
    krs_data = repo.ambil_krs_mahasiswa(conn, nim, semester, tahun_ajaran)
    
    return render_template('admin_input_nilai_mahasiswa.html',
                           mahasiswa=mahasiswa,
                           krs_data=krs_data,
                           semester=semester,
                           tahun_ajaran=tahun_ajaran)

# ----------------- ADMIN CRUD (MAHASISWA, DOSEN, MATKUL) -----------------

@admin_bp.route('/mahasiswa/tambah', methods=['GET', 'POST'])
def tambah_mahasiswa():
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
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
            return redirect(url_for('admin.tambah_mahasiswa'))
            
        if repo.cari_by_nim(conn, nim):
            flash(f'NIM {nim} sudah terdaftar!', 'danger')
            return redirect(url_for('admin.tambah_mahasiswa'))
            
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
            return redirect(url_for('mahasiswa.daftar_mahasiswa'))
        except Exception as e:
            flash(f'Gagal menyimpan: {str(e)}', 'danger')
            return redirect(url_for('admin.tambah_mahasiswa'))
    
    # GET: Kirim data untuk dropdown
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    daftar_fakultas = repo.ambil_daftar_fakultas(conn)
    
    return render_template('tambah_mahasiswa.html', 
                          daftar_prodi=daftar_prodi,
                          daftar_fakultas=daftar_fakultas)

@admin_bp.route('/mahasiswa/edit/<nim>', methods=['GET', 'POST'])
def edit_mahasiswa(nim):
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
        
    conn = get_db()
    data = repo.cari_by_nim(conn, nim)
    if not data: return redirect(url_for('mahasiswa.daftar_mahasiswa'))

    if request.method == 'POST':
        nama_baru = request.form['nama']
        alamat_baru = request.form['alamat']
        prodi_baru = request.form['prodi']
        fakultas_baru = request.form['fakultas']
        telepon_baru = request.form['telepon']

        if not nama_baru:
            flash('Nama wajib diisi!', 'danger')
            return redirect(url_for('admin.edit_mahasiswa', nim=nim))
            
        try:
            repo.ubah_data_mahasiswa(conn, nim, nama_baru, alamat_baru, prodi_baru, fakultas_baru, telepon_baru)
            flash(f'Data Mahasiswa {nim} berhasil diubah!', 'success')
        except Exception as e:
            flash(f'Gagal mengubah data: {e}', 'danger')
            
        return redirect(url_for('mahasiswa.daftar_mahasiswa'))
    
    # GET: Kirim data untuk dropdown
    daftar_prodi = repo.ambil_daftar_prodi(conn)
    daftar_fakultas = repo.ambil_daftar_fakultas(conn)
        
    return render_template('edit_mahasiswa.html', 
                          mhs=data,
                          daftar_prodi=daftar_prodi,
                          daftar_fakultas=daftar_fakultas)

@admin_bp.route('/mahasiswa/hapus/<nim>', methods=['POST'])
def hapus_mahasiswa(nim):
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
        
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
        
    return redirect(url_for('mahasiswa.daftar_mahasiswa'))

@admin_bp.route('/dosen/tambah', methods=['GET', 'POST'])
def tambah_dosen():
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
    conn = get_db()
        
    if request.method == 'POST':
        nip = request.form['nip']
        nama = request.form['nama']
        matkul_ajar = request.form['matkul_ajar']
        telepon = request.form['telepon']
        
        if not nip or not nama:
            flash('NIP dan Nama wajib diisi!', 'danger')
            return redirect(url_for('admin.tambah_dosen'))
            
        if repo.cari_by_nip(conn, nip):
            flash(f'NIP {nip} sudah terdaftar!', 'danger')
            return redirect(url_for('admin.tambah_dosen'))
            
        try:
            repo.tambah_data_dosen(conn, nip, nama, matkul_ajar, telepon)
            
            # --- AUTO REGISTER USER DOSEN ---
            # Default Password = NIP
            hashed_pw = generate_password_hash(nip, method='pbkdf2:sha256')
            repo.tambah_user(conn, nip, hashed_pw, role='Dosen')
            
            flash(f'Data Dosen {nip} berhasil ditambahkan! Akun Login otomatis dibuat (Pass: {nip}).', 'success')
            return redirect(url_for('dosen.daftar_dosen'))
        except:
            flash('Gagal simpan atau NIP sudah ada akun.', 'danger')
    
    # GET: Kirim daftar mata kuliah untuk dropdown
    matkul_list = repo.ambil_semua_matkul_untuk_dosen(conn)
            
    return render_template('tambah_dosen.html', matkul_list=matkul_list)

@admin_bp.route('/dosen/edit/<nip>', methods=['GET', 'POST'])
def edit_dosen(nip):
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
        
    conn = get_db()
    data = repo.cari_by_nip(conn, nip)
    if not data: return redirect(url_for('dosen.daftar_dosen'))

    if request.method == 'POST':
        nama_baru = request.form['nama']
        matkul_ajar_baru = request.form['matkul_ajar']
        telepon_baru = request.form['telepon']

        if not nama_baru:
            flash('Nama wajib diisi!', 'danger')
            return redirect(url_for('admin.edit_dosen', nip=nip))
            
        repo.ubah_data_dosen(conn, nip, nama_baru, matkul_ajar_baru, telepon_baru)
        flash(f'Data Dosen {nip} berhasil diubah!', 'warning')
        return redirect(url_for('dosen.daftar_dosen'))
    
    # GET: Kirim daftar mata kuliah untuk dropdown
    matkul_list = repo.ambil_semua_matkul_untuk_dosen(conn)
        
    return render_template('edit_dosen.html', 
                          dosen=data,
                          matkul_list=matkul_list)

@admin_bp.route('/dosen/hapus/<nip>', methods=['POST'])
def hapus_dosen(nip):
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
        
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
        
    return redirect(url_for('dosen.daftar_dosen'))

@admin_bp.route('/matkul')
def daftar_matkul():
    # PROTEKSI ROUTE
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('auth.login'))
        
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

@admin_bp.route('/matkul/tambah', methods=['GET', 'POST'])
def tambah_matkul():
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        kode = request.form['kode_matkul']
        nama = request.form['nama_matkul']
        sks = request.form['sks']
        smt = request.form['semester']
        prodi = request.form.get('prodi')
        
        # New Schedule Params
        hari = request.form.get('hari')
        jam_mulai = request.form.get('jam_mulai')
        jam_selesai = request.form.get('jam_selesai')
        ruang = request.form.get('ruang')

        if not kode or not nama:
            flash('Kode dan Nama Mata Kuliah wajib diisi!', 'danger')
            return redirect(url_for('admin.tambah_matkul'))
            
        conn = get_db()
        if repo.cari_by_kode_matkul(conn, kode):
            flash(f'Kode Mata Kuliah {kode} sudah terdaftar!', 'danger')
            return redirect(url_for('admin.tambah_matkul'))
            
        try:
            repo.tambah_data_matkul(conn, kode, nama, int(sks), int(smt), prodi, hari, jam_mulai, jam_selesai, ruang)
            flash(f'Data Mata Kuliah {kode} berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.daftar_matkul'))
        except Exception as e:
            flash(f'Gagal simpan: {e}', 'danger')
            
    return render_template('tambah_matkul.html')

@admin_bp.route('/matkul/edit/<kode>', methods=['GET', 'POST'])
def edit_matkul(kode):
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
        
    conn = get_db()
    data = repo.cari_by_kode_matkul(conn, kode)
    if not data: return redirect(url_for('admin.daftar_matkul'))

    if request.method == 'POST':
        nama_baru = request.form['nama_matkul']
        sks_baru = request.form['sks']
        semester_baru = request.form['semester']
        prodi_baru = request.form.get('prodi')
        
        # New Schedule Params
        hari_baru = request.form.get('hari')
        jam_mulai_baru = request.form.get('jam_mulai')
        jam_selesai_baru = request.form.get('jam_selesai')
        ruang_baru = request.form.get('ruang')

        if not nama_baru:
            flash('Nama Mata Kuliah wajib diisi!', 'danger')
            return redirect(url_for('admin.edit_matkul', kode=kode))
        
        try:
            sks_baru = int(sks_baru)
            semester_baru = int(semester_baru)
        except ValueError:
            flash('SKS dan Semester harus berupa angka!', 'danger')
            return redirect(url_for('admin.edit_matkul', kode=kode))
            
        repo.ubah_data_matkul(conn, kode, nama_baru, sks_baru, semester_baru, prodi_baru, hari_baru, jam_mulai_baru, jam_selesai_baru, ruang_baru)
        flash(f'Data Mata Kuliah {kode} berhasil diubah!', 'warning')
        return redirect(url_for('admin.daftar_matkul'))
        
    return render_template('edit_matkul.html', matkul=data)

@admin_bp.route('/matkul/hapus/<kode>', methods=['POST'])
def hapus_matkul(kode):
    # PROTEKSI ROUTE
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('auth.login'))
        
    conn = get_db()
    success = repo.hapus_data_matkul(conn, kode)
    if success:
        flash(f'Data Mata Kuliah {kode} berhasil dihapus!', 'danger')
    else:
        flash(f'Gagal menghapus data Mata Kuliah {kode}.', 'danger')
        
    return redirect(url_for('admin.daftar_matkul'))

@admin_bp.route('/preview', methods=['POST'])
def preview_report():
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
    conn = get_db()
    report_type = request.form.get('type')
    selected_ids = list(set(request.form.getlist('selected_ids'))) 
    
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
        headers = ['NIM', 'Nama', 'Total SKS', 'Jumlah Matkul']
        for nim in selected_ids:
            mhs = repo.cari_by_nim(conn, nim)
            if mhs:
                sks = repo.hitung_sks_krs(conn, nim, 1, '2023/2024') 
                krs_items = repo.ambil_krs_mahasiswa(conn, nim, 1, '2023/2024')
                count = len(krs_items)
                data.append({'c1': mhs['nim'], 'c2': mhs['nama'], 'c3': sks, 'c4': count})
        
    return render_template('preview_print.html', 
                           title=title, 
                           headers=headers, 
                           data=data)
