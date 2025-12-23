from flask import render_template, redirect, url_for, request, flash, session
import repository as repo
from math import ceil
from . import mahasiswa_bp
from .general import get_db

PER_PAGE = 10
HARGA_PER_SKS = 150000

# ----------------- ROUTE MAHASISWA & KRS -----------------

@mahasiswa_bp.route('/mahasiswa')
def daftar_mahasiswa():
    # PROTEKSI ROUTE
    if not session.get('logged_in'):
        flash('Anda harus login untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('auth.login'))

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

# ----------------- KRS & KHS -----------------

@mahasiswa_bp.route('/krs')
def daftar_krs_mahasiswa():
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
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

@mahasiswa_bp.route('/krs/manage/<nim>', methods=['GET', 'POST'])
def manage_krs(nim):
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
    # --- PROTEKSI AKSES DATA ORANG LAIN ---
    if session.get('role') == 'Mahasiswa' and session.get('username') != nim:
        flash('Anda tidak memiliki izin mengakses data KRS mahasiswa lain.', 'danger')
        return redirect(url_for('mahasiswa.manage_krs', nim=session.get('username')))
    # --------------------------------------
    
    conn = get_db()
    mahasiswa = repo.cari_by_nim(conn, nim)
    if not mahasiswa:
        flash('Data mahasiswa tidak ditemukan', 'danger')
        return redirect(url_for('mahasiswa.daftar_krs_mahasiswa'))
        
    # Default semester/tahun (could be dynamic later)
    semester_aktif = request.args.get('semester', 1, type=int)
    tahun_ajaran_aktif = request.args.get('tahun_ajaran', '2023/2024')
    
    # List all available matkul
    semua_matkul = repo.daftar_matkul(conn, limit=1000) # Get all for dropdown
    
    # Get current KRS
    krs_data = repo.ambil_krs_mahasiswa(conn, nim, semester_aktif, tahun_ajaran_aktif)
    total_sks = repo.hitung_sks_krs(conn, nim, semester_aktif, tahun_ajaran_aktif)

    # Filter: Remove matkul that are already in KRS
    taken_codes = {item['kode_matkul'] for item in krs_data}
    
    # Filter available courses by Student's Prodi AND Semester
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
            return redirect(url_for('mahasiswa.manage_krs', nim=nim, semester=semester_aktif, tahun_ajaran=tahun_ajaran_aktif))

        # Check if already taken
        if repo.cek_krs_exist(conn, nim, kode_matkul, semester_aktif, tahun_ajaran_aktif):
             flash('Mata kuliah sudah diambil.', 'warning')
             return redirect(url_for('mahasiswa.manage_krs', nim=nim, semester=semester_aktif, tahun_ajaran=tahun_ajaran_aktif))
        
        # Check SKS Limit
        matkul_info = repo.cari_by_kode_matkul(conn, kode_matkul)
        if total_sks + matkul_info['sks'] > 24:
            flash(f'Gagal! Total SKS akan menjadi {total_sks + matkul_info["sks"]}. Maksimal 24 SKS.', 'danger')
        else:
            repo.tambah_krs(conn, nim, kode_matkul, semester_aktif, tahun_ajaran_aktif)
            flash('Mata kuliah berhasil ditambahkan ke KRS.', 'success')
            
        return redirect(url_for('mahasiswa.manage_krs', nim=nim, semester=semester_aktif, tahun_ajaran=tahun_ajaran_aktif))

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

@mahasiswa_bp.route('/krs/bayar/<nim>', methods=['POST'])
def bayar_krs(nim):
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
    conn = get_db()
    semester = request.form.get('semester', type=int)
    tahun_ajaran = request.form.get('tahun_ajaran')
    metode = request.form.get('metode_pembayaran')
    
    if not metode:
        flash('Pilih metode pembayaran!', 'danger')
        return redirect(url_for('mahasiswa.manage_krs', nim=nim, semester=semester, tahun_ajaran=tahun_ajaran))
        
    repo.bayar_tagihan(conn, nim, semester, tahun_ajaran, metode)
    flash('Pembayaran berhasil dikonfirmasi!', 'success')
    return redirect(url_for('mahasiswa.manage_krs', nim=nim, semester=semester, tahun_ajaran=tahun_ajaran))

@mahasiswa_bp.route('/krs/invoice/<int:id_pembayaran>')
def invoice_krs(id_pembayaran):
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
    conn = get_db()
    pembayaran = repo.ambil_pembayaran_by_id(conn, id_pembayaran)
    
    if not pembayaran:
        flash('Data pembayaran tidak ditemukan.', 'danger')
        return redirect(url_for('mahasiswa.daftar_krs_mahasiswa'))
        
    mahasiswa = repo.cari_by_nim(conn, pembayaran['nim'])
    
    # Get KRS details for this invoice context
    krs_data = repo.ambil_krs_mahasiswa(conn, pembayaran['nim'], pembayaran['semester'], pembayaran['tahun_ajaran'])
    
    return render_template('invoice.html', 
                           pembayaran=pembayaran, 
                           mahasiswa=mahasiswa,
                           krs_data=krs_data)

@mahasiswa_bp.route('/krs/hapus/<id_krs>', methods=['POST'])
def hapus_krs_item(id_krs):
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
    conn = get_db()
    repo.hapus_krs(conn, id_krs)
    flash('Mata kuliah dihapus dari KRS.', 'success')
    return redirect(request.referrer)

@mahasiswa_bp.route('/mahasiswa/krs/tambah_bulk', methods=['POST'])
def tambah_krs_bulk():
    if not session.get('logged_in') or session.get('role') != 'Mahasiswa':
        return redirect(url_for('auth.login'))
        
    nim = session.get('username')
    semester = request.form.get('semester', type=int)
    tahun_ajaran = request.form.get('tahun_ajaran')
    
    if not semester or not tahun_ajaran:
        flash('Semester dan Tahun Ajaran tidak valid.', 'danger')
        return redirect(url_for('mahasiswa.manage_krs', nim=nim))
        
    conn = get_db()
    
    # Fix: `tambah_krs_bulk` is in `repo`, so we need to call it from there. 
    # But wait, original code calls `repo.tambah_krs_bulk`.
    success, message = repo.tambah_krs_bulk(conn, nim, semester, tahun_ajaran)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
        
    return redirect(url_for('mahasiswa.manage_krs', nim=nim, semester=semester, tahun_ajaran=tahun_ajaran))

@mahasiswa_bp.route('/mahasiswa/krs/cetak')
def cetak_krs():
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
    conn = get_db()
    nim = request.args.get('nim') or session.get('username')
    semester = request.args.get('semester', 1, type=int)
    tahun_ajaran = request.args.get('tahun_ajaran', '2023/2024')
    
    # Security check for Students
    if session.get('role') == 'Mahasiswa' and session.get('username') != nim:
        return redirect(url_for('general.index'))
        
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

@mahasiswa_bp.route('/mahasiswa/khs')
def lihat_khs():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
        
    conn = get_db()
    
    # Akses NIM: Mahasiswa ambil dari session, Admin/Dosen bisa ambil dari parameter
    if session.get('role') in ['Admin Sistem', 'Dosen']:
        nim = request.args.get('nim')
        if not nim:
            flash('NIM harus ditentukan.', 'warning')
            return redirect(url_for('general.index'))
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

@mahasiswa_bp.route('/mahasiswa/khs/cetak')
def cetak_khs():
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
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

@mahasiswa_bp.route('/mahasiswa/transkrip')
def transkrip_nilai():
    if not session.get('logged_in'): return redirect(url_for('auth.login'))
    
    conn = get_db()
    # Akses NIM: Mahasiswa ambil dari session, Admin/Dosen bisa ambil dari parameter
    if session.get('role') in ['Admin Sistem', 'Dosen']:
        nim = request.args.get('nim')
        if not nim:
            flash('NIM harus ditentukan.', 'warning')
            return redirect(url_for('general.index'))
    else:
        nim = session.get('username')
        
    mahasiswa = repo.cari_by_nim(conn, nim)
    if not mahasiswa:
        flash('Mahasiswa tidak ditemukan.', 'danger')
        return redirect(url_for('general.index'))

    # Ambil SEMUA data KRS (riwayat studi)
    # Kita perlu query custom atau helper baru di repo, tapi untuk sekarang kita bisa fetch semua dan filter manual
    # Atau, kita asumsikan ambil_khs bisa fleksibel. Tapi ambil_khs filter by semester.
    # Kita buat logic sederhana: Ambil semua data krs yang ada nilai_huruf nya.
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT k.semester, m.kode_matkul, m.nama_matkul, m.sks, k.nilai_huruf, k.nilai_angka
        FROM tbKRS k
        JOIN tbMatakuliah m ON k.kode_matkul = m.kode_matkul
        WHERE k.nim = ? AND k.nilai_huruf IS NOT NULL
        ORDER BY k.semester ASC, m.nama_matkul ASC
    """, (nim,))
    rows = cursor.fetchall()
    
    transkrip = {}
    total_sks_kumulatif = 0
    total_bobot_kumulatif = 0
    bobot_map = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
    
    for row in rows:
        sem = row[0]
        mk = {
            'kode_matkul': row[1],
            'nama_matkul': row[2],
            'sks': row[3],
            'nilai_huruf': row[4],
            'bobot': bobot_map.get(row[4], 0)
        }
        
        if sem not in transkrip:
            transkrip[sem] = {'matkul': [], 'sks_semester': 0, 'bobot_semester': 0}
            
        transkrip[sem]['matkul'].append(mk)
        transkrip[sem]['sks_semester'] += mk['sks']
        transkrip[sem]['bobot_semester'] += (mk['sks'] * mk['bobot'])
        
        total_sks_kumulatif += mk['sks']
        total_bobot_kumulatif += (mk['sks'] * mk['bobot'])
        
    # Hitung IPS per semester
    for sem in transkrip:
        sks = transkrip[sem]['sks_semester']
        bobot = transkrip[sem]['bobot_semester']
        if sks > 0:
            transkrip[sem]['ips'] = round(bobot / sks, 2)
        else:
            transkrip[sem]['ips'] = 0.00
            
    # Hitung IPK
    ipk = 0.00
    if total_sks_kumulatif > 0:
        ipk = round(total_bobot_kumulatif / total_sks_kumulatif, 2)
        
    return render_template('transkrip.html',
                           mahasiswa=mahasiswa,
                           transkrip_per_semester=transkrip,
                           total_sks=total_sks_kumulatif,
                           ipk=ipk)
