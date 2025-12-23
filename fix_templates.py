import os, re

replacements = {
    'admin_nilai_mahasiswa_list': 'admin.admin_nilai_mahasiswa_list',
    'input_nilai_mahasiswa': 'admin.input_nilai_mahasiswa',
    'approve_pendaftaran': 'admin.approve_pendaftaran',
    'reject_pendaftaran': 'admin.reject_pendaftaran',
    'edit_dosen': 'admin.edit_dosen',
    'hapus_dosen': 'admin.hapus_dosen',
    'tambah_dosen': 'admin.tambah_dosen',
    'edit_mahasiswa': 'admin.edit_mahasiswa',
    'hapus_mahasiswa': 'admin.hapus_mahasiswa',
    'tambah_mahasiswa': 'admin.tambah_mahasiswa',
    'edit_matkul': 'admin.edit_matkul',
    'hapus_matkul': 'admin.hapus_matkul',
    'tambah_matkul': 'admin.tambah_matkul',
    'preview_report': 'admin.preview_report',
    'admin_pendaftaran': 'admin.admin_pendaftaran',
    'daftar_dosen': 'dosen.daftar_dosen',
    'dosen_nilai_dashboard': 'dosen.dosen_nilai_dashboard',
    'input_nilai': 'dosen.input_nilai',
    'daftar_mahasiswa': 'mahasiswa.daftar_mahasiswa',
    'daftar_krs_mahasiswa': 'mahasiswa.daftar_krs_mahasiswa',
    'manage_krs': 'mahasiswa.manage_krs',
    'bayar_krs': 'mahasiswa.bayar_krs',
    'invoice_krs': 'mahasiswa.invoice_krs',
    'hapus_krs_item': 'mahasiswa.hapus_krs_item',
    'tambah_krs_bulk': 'mahasiswa.tambah_krs_bulk',
    'cetak_krs': 'mahasiswa.cetak_krs',
    'lihat_khs': 'mahasiswa.lihat_khs',
    'cetak_khs': 'mahasiswa.cetak_khs',
    'transkrip_nilai': 'mahasiswa.transkrip_nilai',
    'daftar_matkul': 'admin.daftar_matkul',
    'login': 'auth.login',
    'logout': 'auth.logout',
    'register': 'auth.register',
    'pendaftaran_status': 'auth.pendaftaran_status',
    'reset_password': 'auth.reset_password',
    'index': 'general.index'
}

template_dir = 'c:/Documents/project/akademik_web/templates'
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for old, new in replacements.items():
                # Correct pattern: url_for('old' ... ) -> url_for('new' ... )
                # We use word boundary or characters like ( or ,
                # Pattern: url_for followed by ( then quote then old name then quote
                pattern = r"url_for\(\s*['\"]" + re.escape(old) + r"['\"]"
                replacement = "url_for('" + new + "'"
                content = re.sub(pattern, replacement, content)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
print('Fixed templates successfully.')
