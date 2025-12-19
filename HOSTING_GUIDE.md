# Panduan Cepat Deployment ke Hosting

## Informasi Repository GitHub
- **URL**: https://github.com/sangyoga28/akademik_web
- **Commit Terbaru**: feat: Complete academic system with grading and KHS features
- **Branch**: main

---

## Pilihan Platform Hosting

Pilih salah satu platform berikut sesuai kebutuhan:

### 1. PythonAnywhere (Gratis & Mudah) ⭐ RECOMMENDED
**Cocok untuk**: Pemula, testing, demo
**Biaya**: Gratis (dengan batasan)
**Setup Time**: ~15 menit

**Langkah Singkat**:
1. Daftar di https://www.pythonanywhere.com
2. Buka Bash Console, jalankan:
   ```bash
   git clone https://github.com/sangyoga28/akademik_web.git
   cd akademik_web
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python reset_and_seed.py
   ```
3. Setup Web App di tab "Web" (lihat DEPLOYMENT.md untuk detail)
4. Akses di: `yourusername.pythonanywhere.com`

**Panduan Lengkap**: Lihat bagian "Deployment ke PythonAnywhere" di DEPLOYMENT.md

---

### 2. Railway (Modern & Auto-Deploy)
**Cocok untuk**: Production, auto-deploy dari Git
**Biaya**: $5/bulan (trial gratis)
**Setup Time**: ~5 menit

**Langkah Singkat**:
1. Login ke https://railway.app
2. New Project → Deploy from GitHub
3. Pilih repository `akademik_web`
4. Railway auto-deploy
5. Jalankan `python reset_and_seed.py` via Railway Shell

**Panduan Lengkap**: Lihat bagian "Deployment ke Railway" di DEPLOYMENT.md

---

### 3. VPS (Full Control)
**Cocok untuk**: Production, custom configuration
**Biaya**: Mulai dari $5/bulan (DigitalOcean, Vultr, dll)
**Setup Time**: ~30-60 menit

**Langkah Singkat**:
1. Setup Ubuntu VPS
2. Install Python, Nginx, Gunicorn
3. Clone repository
4. Setup systemd service
5. Konfigurasi Nginx reverse proxy

**Panduan Lengkap**: Lihat bagian "Deployment ke VPS" di DEPLOYMENT.md

---

### 4. Shared Hosting dengan cPanel
**Cocok untuk**: Jika sudah punya hosting
**Biaya**: Tergantung provider
**Setup Time**: ~20-30 menit

**Catatan**: Pastikan hosting support Python 3.8+

**Panduan Lengkap**: Lihat bagian "Deployment ke Shared Hosting" di DEPLOYMENT.md

---

## Checklist Deployment (Semua Platform)

### Pre-Deployment
- [ ] Pastikan punya akun di platform hosting pilihan
- [ ] Siapkan akses (SSH/FTP/Panel)
- [ ] Backup data lokal jika perlu

### Deployment
- [ ] Clone/Upload repository dari GitHub
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Inisialisasi database: `python reset_and_seed.py`
- [ ] Konfigurasi web server (sesuai platform)
- [ ] Test akses aplikasi

### Post-Deployment
- [ ] Test login sebagai Admin: `admin` / `admin123`
- [ ] Test login sebagai Dosen: `1234567890` / `1234567890`
- [ ] Test login sebagai Mahasiswa: `2023100001` / `2023100001`
- [ ] Test fitur CRUD (tambah/edit/hapus data)
- [ ] Test input nilai dosen
- [ ] Test KRS dan KHS mahasiswa
- [ ] Setup SSL/HTTPS (recommended)
- [ ] Ganti SECRET_KEY untuk production

---

## Kredensial Default

Setelah deployment dan seeding database:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Dosen | 1234567890 | 1234567890 |
| Mahasiswa | 2023100001 | 2023100001 |

> ⚠️ **PENTING**: Ganti password default setelah deployment!

---

## File yang Perlu Di-Upload

✅ **Upload**:
- app.py
- repository.py
- reset_and_seed.py
- requirements.txt
- templates/ (semua file)
- static/ (semua file)
- README.md
- DEPLOYMENT.md

❌ **JANGAN Upload**:
- akademik.db (akan dibuat otomatis)
- venv/ (virtual environment)
- __pycache__/
- *.pyc
- test_*.py, check_*.py, verify_*.py

---

## Troubleshooting Umum

### Database Error
```bash
# Jalankan ulang seeding
python reset_and_seed.py
```

### Module Not Found
```bash
# Install ulang dependencies
pip install -r requirements.txt
```

### Permission Denied
```bash
# Linux/VPS
chmod 755 akademik_web
chmod 644 akademik.db
```

### Port Already in Use
```python
# Edit app.py, ganti port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Ganti 8080 sesuai kebutuhan
```

---

## Langkah Selanjutnya

1. **Pilih Platform Hosting** dari opsi di atas
2. **Baca Panduan Lengkap** di DEPLOYMENT.md untuk platform pilihan
3. **Clone Repository** dari GitHub
4. **Ikuti Langkah Deployment** sesuai platform
5. **Test Aplikasi** dengan kredensial default
6. **Amankan Aplikasi** (ganti password, setup SSL)

---

## Butuh Bantuan?

- **Dokumentasi Lengkap**: Baca DEPLOYMENT.md
- **README**: Baca README.md untuk info aplikasi
- **GitHub Issues**: Buat issue di repository jika ada masalah

---

**Selamat Deployment! 🚀**

Jika ada pertanyaan atau kendala, silakan hubungi atau buat issue di GitHub repository.
