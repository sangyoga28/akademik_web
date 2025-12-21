import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def debug_krs(nim_target=None):
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("DEBUG KRS LOGIC")
    
    # 1. Get Student
    if nim_target:
        cursor.execute("SELECT * FROM tbMahasiswa WHERE nim = ?", (nim_target,))
    else:
        cursor.execute("SELECT * FROM tbMahasiswa WHERE prodi = 'Manajemen' LIMIT 1")
    
    mhs = cursor.fetchone()
    if not mhs:
        print("No student found.")
        return
        
    print(f"Student: {mhs['nama']} ({mhs['nim']})")
    print(f"Prodi:   '{mhs['prodi']}'")
    
    semester_aktif = 1
    print(f"Semester Aktif: {semester_aktif}")
    
    # 2. Get All Matkul
    cursor.execute("SELECT * FROM tbMatakuliah")
    semua_matkul = cursor.fetchall()
    print(f"Total Matkul in DB: {len(semua_matkul)}")
    
    # 3. Apply Filter (Same as app.py)
    # Filter: mk['prodi'] == mhs['prodi'] OR mk['prodi'] == 'Umum' OR not mk['prodi']
    # AND mk['semester'] == semester_aktif
    
    matkul_tersedia = []
    skipped_prodi = 0
    skipped_sem = 0
    
    for mk in semua_matkul:
        # Check Prodi
        match_prodi = (mk['prodi'] == mhs['prodi'] or mk['prodi'] == 'Umum' or not mk['prodi'])
        if not match_prodi:
            skipped_prodi += 1
            continue
            
        # Check Semester
        # Note: In SQLite, data might be int or str. app.py forces int comparison.
        # Let's check type.
        mk_sem = mk['semester']
        try:
            mk_sem_int = int(mk_sem)
        except:
            mk_sem_int = -1
            
        if mk_sem_int != semester_aktif:
            skipped_sem += 1
            # print(f"  Skip {mk['kode_matkul']} Sem {mk_sem} != {semester_aktif}")
            continue
            
        matkul_tersedia.append(mk)
        
    print(f"\nFiltered Results:")
    print(f"  Skipped due to Prodi: {skipped_prodi}")
    print(f"  Skipped due to Sem:   {skipped_sem}")
    print(f"  AVAILABLE:            {len(matkul_tersedia)}")
    
    print("\nList Available:")
    total_sks = 0
    for mk in matkul_tersedia:
        print(f"  - {mk['kode_matkul']} {mk['nama_matkul']} ({mk['sks']} SKS) [Prodi: {mk['prodi']}]")
        total_sks += mk['sks']
        
    print(f"\nTotal SKS Available: {total_sks}")

    conn.close()

if __name__ == "__main__":
    debug_krs()
