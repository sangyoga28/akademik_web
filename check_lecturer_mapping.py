import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "akademik.db")

def check_mapping():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all courses
    cursor.execute("SELECT kode_matkul, nama_matkul FROM tbMatakuliah")
    courses = cursor.fetchall()
    
    # Get all lecturers and their courses
    cursor.execute("SELECT nip, nama, matkul_ajar FROM tbDosen")
    lecturers = cursor.fetchall()
    
    taught_courses = [l['matkul_ajar'] for l in lecturers]
    
    print(f"Total Courses: {len(courses)}")
    print(f"Total Lecturers: {len(lecturers)}")
    
    missing = []
    for c in courses:
        if c['nama_matkul'] not in taught_courses:
            missing.append(c['nama_matkul'])
            
    print(f"\nCourses without lecturers ({len(missing)}):")
    for m in missing:
        print(f"- {m}")
        
    conn.close()
    return missing

if __name__ == "__main__":
    check_mapping()
