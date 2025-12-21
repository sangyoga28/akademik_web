"""
Script Verifikasi Lengkap Integrasi Sistem Akademik
Memastikan semua fitur terhubung dinamis dengan database
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def test_database_connection():
    """Test 1: Koneksi Database"""
    print("\n" + "="*70)
    print("TEST 1: KONEKSI DATABASE")
    print("="*70)
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Cek semua tabel
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"[OK] Database terhubung. Tabel tersedia: {len(tables)}")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"     - {table}: {count} records")
        
        conn.close()
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def test_prodi_consistency():
    """Test 2: Konsistensi Prodi"""
    print("\n" + "="*70)
    print("TEST 2: KONSISTENSI PRODI")
    print("="*70)
    
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Prodi di mahasiswa
    cursor.execute("SELECT DISTINCT prodi FROM tbMahasiswa WHERE prodi IS NOT NULL ORDER BY prodi")
    prodi_mhs = [row[0] for row in cursor.fetchall()]
    
    # Prodi di mata kuliah
    cursor.execute("SELECT DISTINCT prodi FROM tbMatakuliah WHERE prodi != 'Umum' ORDER BY prodi")
    prodi_mk = [row[0] for row in cursor.fetchall()]
    
    print(f"Prodi Mahasiswa: {prodi_mhs}")
    print(f"Prodi Matakuliah: {prodi_mk}")
    
    # Cek konsistensi
    all_consistent = True
    for prodi in prodi_mhs:
        if prodi not in prodi_mk:
            print(f"[ERROR] Prodi '{prodi}' ada di mahasiswa tapi tidak ada mata kuliahnya!")
            all_consistent = False
        else:
            cursor.execute("SELECT COUNT(*) FROM tbMatakuliah WHERE prodi = ?", (prodi,))
            count = cursor.fetchone()[0]
            print(f"[OK] Prodi '{prodi}': {count} mata kuliah tersedia")
    
    conn.close()
    return all_consistent

def test_mahasiswa_prodi_integration():
    """Test 3: Integrasi Mahasiswa-Prodi-Matakuliah"""
    print("\n" + "="*70)
    print("TEST 3: INTEGRASI MAHASISWA-PRODI-MATAKULIAH")
    print("="*70)
    
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Ambil sample mahasiswa
    cursor.execute("SELECT nim, nama, prodi FROM tbMahasiswa LIMIT 5")
    mahasiswa_list = cursor.fetchall()
    
    all_ok = True
    for mhs in mahasiswa_list:
        # Cek apakah ada mata kuliah untuk prodi mahasiswa ini
        cursor.execute("""
            SELECT COUNT(*) FROM tbMatakuliah 
            WHERE prodi = ? OR prodi = 'Umum'
        """, (mhs['prodi'],))
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"[OK] {mhs['nama']} ({mhs['prodi']}): {count} mata kuliah tersedia")
        else:
            print(f"[ERROR] {mhs['nama']} ({mhs['prodi']}): TIDAK ADA mata kuliah!")
            all_ok = False
    
    conn.close()
    return all_ok

def test_dosen_matkul_integration():
    """Test 4: Integrasi Dosen-Matakuliah"""
    print("\n" + "="*70)
    print("TEST 4: INTEGRASI DOSEN-MATAKULIAH")
    print("="*70)
    
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Ambil semua dosen
    cursor.execute("SELECT nip, nama, matkul_ajar FROM tbDosen")
    dosen_list = cursor.fetchall()
    
    print(f"Total dosen: {len(dosen_list)}")
    
    all_ok = True
    for dosen in dosen_list:
        if dosen['matkul_ajar']:
            # Cek apakah mata kuliah yang diampu ada di database
            cursor.execute("""
                SELECT nama_matkul, prodi, semester 
                FROM tbMatakuliah 
                WHERE nama_matkul = ?
            """, (dosen['matkul_ajar'],))
            matkul = cursor.fetchone()
            
            if matkul:
                print(f"[OK] {dosen['nama']}: mengampu {matkul['nama_matkul']} ({matkul['prodi']} Sem {matkul['semester']})")
            else:
                print(f"[WARNING] {dosen['nama']}: mata kuliah '{dosen['matkul_ajar']}' tidak ditemukan di database")
                all_ok = False
    
    conn.close()
    return all_ok

def test_krs_integration():
    """Test 5: Integrasi KRS-Mahasiswa-Matakuliah"""
    print("\n" + "="*70)
    print("TEST 5: INTEGRASI KRS-MAHASISWA-MATAKULIAH")
    print("="*70)
    
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Cek KRS yang ada
    cursor.execute("""
        SELECT k.nim, m.nama, k.kode_matkul, mk.nama_matkul, mk.sks
        FROM tbKRS k
        JOIN tbMahasiswa m ON k.nim = m.nim
        JOIN tbMatakuliah mk ON k.kode_matkul = mk.kode_matkul
        LIMIT 10
    """)
    krs_list = cursor.fetchall()
    
    if len(krs_list) > 0:
        print(f"[OK] Ditemukan {len(krs_list)} KRS (sample):")
        for krs in krs_list[:5]:
            print(f"     - {krs['nama']} mengambil {krs['nama_matkul']} ({krs['sks']} SKS)")
        return True
    else:
        print("[INFO] Belum ada data KRS")
        return True
    
    conn.close()

def test_pembayaran_integration():
    """Test 6: Integrasi Pembayaran-KRS"""
    print("\n" + "="*70)
    print("TEST 6: INTEGRASI PEMBAYARAN-KRS")
    print("="*70)
    
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Cek pembayaran
    cursor.execute("""
        SELECT p.nim, m.nama, p.semester, p.total_sks, p.total_bayar, p.status
        FROM tbPembayaran p
        JOIN tbMahasiswa m ON p.nim = m.nim
        LIMIT 10
    """)
    pembayaran_list = cursor.fetchall()
    
    if len(pembayaran_list) > 0:
        print(f"[OK] Ditemukan {len(pembayaran_list)} pembayaran (sample):")
        for bayar in pembayaran_list[:5]:
            print(f"     - {bayar['nama']} Sem {bayar['semester']}: {bayar['total_sks']} SKS = Rp {bayar['total_bayar']:,} ({bayar['status']})")
        return True
    else:
        print("[INFO] Belum ada data pembayaran")
        return True
    
    conn.close()

def test_helper_functions():
    """Test 7: Fungsi Helper Repository"""
    print("\n" + "="*70)
    print("TEST 7: FUNGSI HELPER REPOSITORY")
    print("="*70)
    
    try:
        import repository as repo
        
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        
        # Test ambil_daftar_prodi
        prodi_list = repo.ambil_daftar_prodi(conn)
        print(f"[OK] ambil_daftar_prodi(): {len(prodi_list)} prodi")
        print(f"     {prodi_list}")
        
        # Test ambil_daftar_fakultas
        fakultas_list = repo.ambil_daftar_fakultas(conn)
        print(f"[OK] ambil_daftar_fakultas(): {len(fakultas_list)} fakultas")
        print(f"     {fakultas_list}")
        
        # Test ambil_semua_matkul_untuk_dosen
        matkul_list = repo.ambil_semua_matkul_untuk_dosen(conn)
        print(f"[OK] ambil_semua_matkul_untuk_dosen(): {len(matkul_list)} mata kuliah")
        
        # Test ambil_matkul_by_prodi_semester
        if len(prodi_list) > 0:
            sample_prodi = prodi_list[0]
            matkul_prodi = repo.ambil_matkul_by_prodi_semester(conn, sample_prodi, 1)
            print(f"[OK] ambil_matkul_by_prodi_semester('{sample_prodi}', 1): {len(matkul_prodi)} mata kuliah")
        
        conn.close()
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def test_dropdown_data_availability():
    """Test 8: Ketersediaan Data untuk Dropdown"""
    print("\n" + "="*70)
    print("TEST 8: KETERSEDIAAN DATA UNTUK DROPDOWN")
    print("="*70)
    
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    all_ok = True
    
    # Test 1: Dropdown Fakultas
    cursor.execute("SELECT DISTINCT fakultas FROM tbMahasiswa WHERE fakultas IS NOT NULL")
    fakultas = cursor.fetchall()
    if len(fakultas) > 0:
        print(f"[OK] Dropdown Fakultas: {len(fakultas)} pilihan tersedia")
    else:
        print("[WARNING] Dropdown Fakultas: Akan menggunakan default")
    
    # Test 2: Dropdown Prodi
    cursor.execute("SELECT DISTINCT prodi FROM tbMatakuliah WHERE prodi != 'Umum'")
    prodi = cursor.fetchall()
    if len(prodi) >= 4:
        print(f"[OK] Dropdown Prodi: {len(prodi)} pilihan tersedia")
    else:
        print(f"[ERROR] Dropdown Prodi: Hanya {len(prodi)} pilihan (minimal 4)")
        all_ok = False
    
    # Test 3: Dropdown Mata Kuliah untuk Dosen
    cursor.execute("SELECT COUNT(*) FROM tbMatakuliah WHERE prodi != 'Umum'")
    matkul_count = cursor.fetchone()[0]
    if matkul_count > 0:
        print(f"[OK] Dropdown Mata Kuliah (Dosen): {matkul_count} pilihan tersedia")
    else:
        print("[ERROR] Dropdown Mata Kuliah (Dosen): KOSONG!")
        all_ok = False
    
    # Test 4: Dropdown Mata Kuliah untuk KRS per Prodi
    cursor.execute("SELECT DISTINCT prodi FROM tbMatakuliah WHERE prodi != 'Umum'")
    prodi_list = [row[0] for row in cursor.fetchall()]
    
    for prodi in prodi_list:
        cursor.execute("""
            SELECT COUNT(*) FROM tbMatakuliah 
            WHERE (prodi = ? OR prodi = 'Umum') AND semester = 1
        """, (prodi,))
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"[OK] Dropdown KRS ({prodi} Sem 1): {count} pilihan tersedia")
        else:
            print(f"[ERROR] Dropdown KRS ({prodi} Sem 1): KOSONG!")
            all_ok = False
    
    conn.close()
    return all_ok

# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    print("\n")
    print("+" + "="*68 + "+")
    print("|" + " "*15 + "VERIFIKASI INTEGRASI SISTEM AKADEMIK" + " "*17 + "|")
    print("+" + "="*68 + "+")
    
    results = []
    
    # Jalankan semua test
    results.append(("Database Connection", test_database_connection()))
    results.append(("Konsistensi Prodi", test_prodi_consistency()))
    results.append(("Mahasiswa-Prodi-Matakuliah", test_mahasiswa_prodi_integration()))
    results.append(("Dosen-Matakuliah", test_dosen_matkul_integration()))
    results.append(("KRS Integration", test_krs_integration()))
    results.append(("Pembayaran Integration", test_pembayaran_integration()))
    results.append(("Helper Functions", test_helper_functions()))
    results.append(("Dropdown Data", test_dropdown_data_availability()))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY HASIL VERIFIKASI")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    print("\n" + "="*70)
    print(f"HASIL AKHIR: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] Semua fitur terintegrasi dengan sempurna!")
        print("Sistem siap digunakan.")
    else:
        print(f"\n[WARNING] {total - passed} test(s) gagal. Perlu perbaikan.")
    
    print("="*70 + "\n")
