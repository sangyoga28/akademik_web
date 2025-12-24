# Sistem Informasi Akademik

Aplikasi web untuk manajemen data akademik kampus yang dibangun dengan Flask. Sistem ini mendukung manajemen mahasiswa, dosen, mata kuliah, KRS (Kartu Rencana Studi), penilaian, dan KHS (Kartu Hasil Studi).

## Fitur Utama

### 🔐 Multi-Role Authentication
- **Admin Sistem**: Manajemen data master (mahasiswa, dosen, mata kuliah)
- **Dosen**: Input dan manajemen nilai mahasiswa
- **Mahasiswa**: Pengisian KRS, pembayaran, dan melihat KHS

### 📚 Manajemen Akademik
- **Data Master**: CRUD untuk mahasiswa, dosen, dan mata kuliah
- **KRS**: Pengisian KRS dengan validasi SKS maksimal (24 SKS)
- **Pembayaran**: Sistem pembayaran berbasis SKS (Rp 150.000/SKS)
- **Penilaian**: Input nilai dengan konversi otomatis (angka → huruf)
- **KHS**: Tampilan transkrip nilai dengan perhitungan IPS

### 🎯 Fitur Tambahan
- Pagination untuk semua list data
- Search/filter untuk data mahasiswa, dosen, dan mata kuliah
- Role-based access control
- Auto-generate akun login untuk mahasiswa dan dosen
- Cetak KHS dan invoice pembayaran

## Teknologi

- **Backend**: Flask 3.0.0
- **Database**: SQLite3
- **Frontend**: HTML, CSS, Bootstrap 5
- **Security**: Werkzeug password hashing

## Instalasi Lokal

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/sangyoga28/akademik_web.git
   cd akademik_web
   ```

2. **Buat Virtual Environment (Opsional tapi Disarankan)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inisialisasi Database**
   ```bash
   python reset_and_seed.py
   ```
   
   Script ini akan:
   - Membuat tabel database
   - Mengisi data sample (admin, dosen, mahasiswa, mata kuliah)
   - Membuat akun login untuk semua user

5. **Jalankan Aplikasi**
   ```bash
   python app.py
   ```
   
   Aplikasi akan berjalan di `http://127.0.0.1:5000`

## Kredensial Default

Setelah menjalankan `reset_and_seed.py`, gunakan kredensial berikut untuk login:

### Admin
- **Username**: `admin`
- **Password**: `admin123`

### Dosen
- **Username**: `1234567890` (NIP)
- **Password**: `1234567890`

### Mahasiswa
- **Username**: `2023100001` (NIM - Ahmad Fauzi)
- **Password**: `2023100001`

> **Note**: Password default untuk mahasiswa dan dosen adalah NIM/NIP mereka masing-masing.

## Struktur Project

```
akademik_web/
├── app.py                      # Main Flask application
├── repository.py               # Database operations
├── reset_and_seed.py          # Database seeding script
├── requirements.txt           # Python dependencies
├── akademik.db               # SQLite database (auto-generated)
├── templates/                # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── home.html
│   ├── mahasiswa.html
│   ├── dosen.html
│   ├── matkul.html
│   ├── krs_manage.html
│   ├── khs.html
│   ├── input_nilai.html
│   └── ...
└── static/                   # Static files
    └── css/
        └── style.css
```

## Database Schema

### Tabel Utama
- **tbMahasiswa**: Data biodata mahasiswa
- **tbDosen**: Data dosen pengajar
- **tbMatakuliah**: Data mata kuliah
- **tbUser**: Akun login (admin, dosen, mahasiswa)
- **tbKRS**: Kartu Rencana Studi dan nilai
- **tbPembayaran**: Data pembayaran SKS

## Deployment

Untuk panduan deployment ke berbagai platform hosting, lihat [DEPLOYMENT.md](DEPLOYMENT.md).

Platform yang didukung:
- Shared Hosting (cPanel)
- VPS (dengan Gunicorn/Nginx)
- PythonAnywhere
- Railway
- Heroku

## Penggunaan

### Sebagai Admin
1. Login dengan kredensial admin
2. Kelola data mahasiswa, dosen, dan mata kuliah
3. Lihat statistik sistem di dashboard

### Sebagai Dosen
1. Login dengan NIP
2. Pilih mata kuliah yang diampu
3. Input nilai untuk mahasiswa yang mengambil mata kuliah tersebut
4. Nilai otomatis dikonversi (85-100: A, 75-84: B, dst.)

### Sebagai Mahasiswa
1. Login dengan NIM
2. Isi KRS dengan memilih mata kuliah sesuai prodi dan semester
3. Bayar tagihan SKS
4. Lihat KHS setelah dosen menginput nilai

## Konversi Nilai

Sistem menggunakan konversi nilai berikut:
- **A**: 85 - 100
- **B**: 75 - 84
- **C**: 60 - 74
- **D**: 50 - 59
- **E**: < 50

## Kontribusi

Jika ingin berkontribusi:
1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## Lisensi

Project ini dibuat untuk keperluan pembelajaran dan pengembangan sistem informasi akademik.

## Kontak

Untuk pertanyaan atau saran, silakan buat issue di repository ini.

---

**Dibuat Oleh Sangyoga**
