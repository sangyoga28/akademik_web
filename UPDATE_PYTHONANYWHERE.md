# Panduan Update Hosting PythonAnywhere

Panduan ini menjelaskan cara melakukan update aplikasi di PythonAnywhere setelah melakukan perubahan di GitHub.

---

## Langkah-Langkah Update

### 1. Buka Bash Console di PythonAnywhere

1. Login ke [PythonAnywhere](https://www.pythonanywhere.com)
2. Klik tab **"Consoles"**
3. Klik **"Bash"** untuk membuka console baru (atau gunakan console yang sudah ada)

---

### 2. Navigasi ke Folder Project

```bash
cd akademik_web
```

---

### 3. Pull Update dari GitHub

```bash
git pull origin main
```

**Output yang diharapkan:**
```
remote: Enumerating objects: X, done.
remote: Counting objects: 100% (X/X), done.
remote: Compressing objects: 100% (X/X), done.
Unpacking objects: 100% (X/X), done.
From https://github.com/sangyoga28/akademik_web
 * branch            main       -> FETCH_HEAD
Updating abc1234..def5678
Fast-forward
 app.py           | XX +++---
 repository.py    | XX ++++--
 ...
```

---

### 4. Aktivasi Virtual Environment (Jika Belum Aktif)

```bash
source venv/bin/activate
```

**Indikator berhasil:** Prompt akan berubah menjadi `(venv) username@hostname:~/akademik_web$`

---

### 5. Update Dependencies (Jika Ada Perubahan di requirements.txt)

```bash
pip install -r requirements.txt --upgrade
```

**Catatan:** Langkah ini hanya perlu dilakukan jika ada perubahan di `requirements.txt`

---

### 6. Update Database (Jika Ada Perubahan Schema)

#### Opsi A: Jika Ada Perubahan Schema (Hati-hati, akan hapus data!)

```bash
# PERINGATAN: Ini akan menghapus semua data dan membuat database baru
python reset_and_seed.py
```

#### Opsi B: Jika Hanya Update Kode (Tanpa Perubahan Database)

Tidak perlu jalankan script apapun, langsung ke langkah berikutnya.

#### Opsi C: Jika Perlu Migrasi Data Manual

Jika ada perubahan schema tapi ingin mempertahankan data:
```bash
# Backup database dulu
cp akademik.db akademik_backup_$(date +%Y%m%d).db

# Lalu jalankan script migrasi jika ada
# python migrate_database.py
```

---

### 7. Reload Web App

Ada 2 cara untuk reload aplikasi:

#### Cara 1: Via Web Interface (Recommended)

1. Buka tab **"Web"** di PythonAnywhere dashboard
2. Scroll ke bagian **"Reload"**
3. Klik tombol hijau **"Reload yourusername.pythonanywhere.com"**

#### Cara 2: Via Bash Console

```bash
# Buat file touch untuk trigger reload
touch /var/www/yourusername_pythonanywhere_com_wsgi.py
```

**Ganti `yourusername` dengan username PythonAnywhere Anda**

---

### 8. Verifikasi Update

1. Buka aplikasi di browser: `https://yourusername.pythonanywhere.com`
2. Refresh halaman (Ctrl+F5 untuk hard refresh)
3. Test fitur yang diupdate
4. Login dan pastikan semua berfungsi normal

---

## Troubleshooting

### Problem: Git Pull Gagal - "Your local changes would be overwritten"

**Penyebab:** Ada perubahan lokal yang belum di-commit

**Solution:**
```bash
# Opsi 1: Simpan perubahan lokal (stash)
git stash
git pull origin main
git stash pop  # Kembalikan perubahan lokal

# Opsi 2: Buang perubahan lokal (HATI-HATI!)
git reset --hard HEAD
git pull origin main
```

---

### Problem: "Permission Denied" saat Git Pull

**Solution:**
```bash
# Pastikan Anda punya akses ke repository
# Jika repository private, setup SSH key atau HTTPS token

# Untuk HTTPS dengan token:
git remote set-url origin https://YOUR_TOKEN@github.com/sangyoga28/akademik_web.git
```

---

### Problem: Web App Tidak Reload

**Solution:**
```bash
# 1. Cek error log di PythonAnywhere
# Tab "Web" -> "Log files" -> "Error log"

# 2. Restart manual via console
touch /var/www/yourusername_pythonanywhere_com_wsgi.py

# 3. Jika masih gagal, restart dari Web tab
# Klik "Reload" button berkali-kali
```

---

### Problem: Import Error setelah Update

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Atau install satu per satu
pip uninstall flask werkzeug
pip install flask werkzeug
```

---

### Problem: Database Error setelah Update

**Penyebab:** Schema database berubah tapi database lama masih digunakan

**Solution:**
```bash
# Backup database lama
cp akademik.db akademik_backup.db

# Reset database dengan data baru
python reset_and_seed.py

# Jika perlu restore data tertentu, lakukan manual
```

---

### Problem: Static Files Tidak Update (CSS/JS Lama)

**Penyebab:** Browser cache atau PythonAnywhere cache

**Solution:**
```bash
# 1. Hard refresh di browser (Ctrl+Shift+R atau Cmd+Shift+R)

# 2. Clear cache di PythonAnywhere
# Tab "Web" -> scroll ke "Static files"
# Pastikan mapping benar: /static/ -> /home/username/akademik_web/static/

# 3. Force reload web app
# Tab "Web" -> klik "Reload"
```

---

## Checklist Update Cepat

Gunakan checklist ini untuk update rutin:

```bash
# 1. Masuk ke folder project
cd akademik_web

# 2. Pull update
git pull origin main

# 3. Aktivasi venv (jika belum)
source venv/bin/activate

# 4. Update dependencies (jika perlu)
pip install -r requirements.txt --upgrade

# 5. Update database (jika perlu)
# python reset_and_seed.py  # HATI-HATI: hapus data!

# 6. Reload web app
# Via Web tab: klik tombol "Reload"
```

---

## Update Otomatis dengan Script

Untuk memudahkan, buat script update otomatis:

### File: `update.sh`

```bash
#!/bin/bash

echo "========================================="
echo "Update Aplikasi Akademik"
echo "========================================="

# Navigasi ke folder project
cd ~/akademik_web

# Pull update dari GitHub
echo "Pulling updates from GitHub..."
git pull origin main

# Aktivasi virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Update dependencies
echo "Updating dependencies..."
pip install -r requirements.txt --upgrade

# Reload web app (touch WSGI file)
echo "Reloading web app..."
touch /var/www/$(whoami)_pythonanywhere_com_wsgi.py

echo "========================================="
echo "Update selesai!"
echo "Silakan cek aplikasi di browser."
echo "========================================="
```

### Cara Menggunakan Script:

```bash
# 1. Buat file script
nano update.sh

# 2. Copy paste script di atas, save (Ctrl+X, Y, Enter)

# 3. Beri permission execute
chmod +x update.sh

# 4. Jalankan script
./update.sh
```

---

## Best Practices

### 1. Selalu Backup Database Sebelum Update

```bash
# Buat backup otomatis
cp akademik.db backups/akademik_$(date +%Y%m%d_%H%M%S).db
```

### 2. Test di Local Dulu

Sebelum push ke GitHub dan update hosting:
1. Test perubahan di local
2. Pastikan tidak ada error
3. Test semua fitur yang berubah
4. Baru push ke GitHub

### 3. Gunakan Git Tag untuk Versi Penting

```bash
# Di local, setelah update penting
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Di PythonAnywhere, bisa checkout ke tag tertentu
git checkout v1.0.0
```

### 4. Monitor Error Log

Setelah update, selalu cek error log:
- Tab "Web" → "Log files" → "Error log"
- Tab "Web" → "Log files" → "Server log"

### 5. Dokumentasi Perubahan

Catat setiap update di file CHANGELOG.md:
```markdown
## [1.0.1] - 2025-12-20
### Added
- Fitur input nilai dosen
- KHS mahasiswa dengan IPS

### Fixed
- Bug pagination di daftar mahasiswa
```

---

## Monitoring dan Maintenance

### Cek Status Aplikasi

```bash
# Cek apakah aplikasi berjalan
curl -I https://yourusername.pythonanywhere.com

# Cek ukuran database
ls -lh akademik.db

# Cek disk usage
df -h
```

### Backup Berkala

```bash
# Setup cron job untuk backup otomatis
# Buka crontab
crontab -e

# Tambahkan line ini untuk backup setiap hari jam 2 pagi
0 2 * * * cp ~/akademik_web/akademik.db ~/backups/akademik_$(date +\%Y\%m\%d).db
```

---

## Kontak Support

Jika mengalami masalah:
1. Cek error log di PythonAnywhere
2. Baca dokumentasi: DEPLOYMENT.md
3. Cek GitHub Issues
4. Forum PythonAnywhere: https://www.pythonanywhere.com/forums/

---

**Happy Deploying! 🚀**
