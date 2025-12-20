# Panduan Update PythonAnywhere Console

## Setelah Git Push Berhasil

Ikuti langkah-langkah berikut di **PythonAnywhere Bash Console**:

### 1. Masuk ke Directory Project
```bash
cd ~/akademik_web
```

### 2. Pull Perubahan dari GitHub
```bash
git pull origin main
```

### 3. Jalankan Script untuk Menambahkan Data Teknik Sipil
```bash
python3 add_teknik_sipil.py
```

### 4. (Opsional) Verifikasi Database
```bash
python3 verify_final_database.py
```

### 5. Reload Web App
Setelah semua script selesai dijalankan, reload web app Anda:
```bash
# Cara 1: Menggunakan API (ganti USERNAME dengan username Anda)
touch /var/www/USERNAME_pythonanywhere_com_wsgi.py

# Cara 2: Atau reload melalui Web Tab di dashboard PythonAnywhere
# Klik tombol "Reload" di halaman Web
```

---

## Urutan Lengkap (Copy-Paste)

```bash
# 1. Masuk ke directory
cd ~/akademik_web

# 2. Pull perubahan
git pull origin main

# 3. Jalankan script Teknik Sipil
python3 add_teknik_sipil.py

# 4. Verifikasi (opsional)
python3 verify_final_database.py

# 5. Reload web app (ganti USERNAME dengan username Anda)
touch /var/www/USERNAME_pythonanywhere_com_wsgi.py
```

---

## Catatan Penting

### ⚠️ Jika Database Sudah Ada Data Teknik Sipil
Jika Anda sudah pernah menjalankan script sebelumnya dan ingin menambahkan data lagi, script akan:
- Skip mata kuliah yang sudah ada
- Skip dosen yang sudah assigned
- Hanya menambahkan data baru yang belum ada

### ✓ Yang Ditambahkan oleh Script
- **60 mata kuliah** Teknik Sipil (TS101 - TS801)
- **47 dosen** dengan nama Indonesia yang realistis
- **40 mahasiswa** tersebar di 8 semester
- Semua user account (password = NIM/NIP)

### 🔍 Verifikasi Hasil
Setelah menjalankan script, Anda akan melihat output seperti:
```
======================================================================
TEKNIK SIPIL PROGRAM ADDED SUCCESSFULLY!
======================================================================
[+] 60 courses added
[+] 47 lecturers added
[+] 40 students added
[+] All users have accounts (password = NIM/NIP)
======================================================================
```

### 📊 Cek Database
Untuk melihat statistik lengkap database:
```bash
python3 verify_final_database.py
```

Output akan menampilkan:
- Total courses: 253
- Total lecturers: 219
- Total students: 55
- SKS distribution per prodi per semester

---

## Troubleshooting

### Jika Git Pull Gagal
```bash
# Reset local changes jika ada konflik
git reset --hard origin/main
git pull origin main
```

### Jika Script Error
```bash
# Cek versi Python
python3 --version

# Pastikan di directory yang benar
pwd
# Output harus: /home/USERNAME/akademik_web
```

### Jika Web App Tidak Update
1. Buka dashboard PythonAnywhere
2. Klik tab **Web**
3. Klik tombol **Reload** (hijau)
4. Tunggu beberapa detik
5. Refresh browser Anda

---

## Login Credentials Baru

### Mahasiswa Teknik Sipil (Contoh)
- Username: `2023100016` (NIM)
- Password: `2023100016` (sama dengan NIM)

### Dosen Teknik Sipil (Contoh)
- Username: `1991100173` (NIP)
- Password: `1991100173` (sama dengan NIP)

---

## Selesai!

Setelah semua langkah di atas, aplikasi Anda sudah ter-update dengan:
✓ Program Studi Teknik Sipil
✓ 60 mata kuliah (24 SKS per semester)
✓ 47 dosen
✓ 40 mahasiswa

Database siap digunakan untuk operasional akademik!
