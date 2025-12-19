# Panduan Deployment Sistem Informasi Akademik

Dokumen ini berisi panduan lengkap untuk deployment aplikasi Sistem Informasi Akademik ke berbagai platform hosting.

## Daftar Isi
- [Persiapan Umum](#persiapan-umum)
- [Deployment ke PythonAnywhere](#deployment-ke-pythonanywhere)
- [Deployment ke Railway](#deployment-ke-railway)
- [Deployment ke VPS (Ubuntu)](#deployment-ke-vps-ubuntu)
- [Deployment ke Shared Hosting (cPanel)](#deployment-ke-shared-hosting-cpanel)
- [Troubleshooting](#troubleshooting)

---

## Persiapan Umum

Sebelum deployment, pastikan:

1. **File yang Diperlukan**
   - Semua file aplikasi (app.py, repository.py, templates/, static/)
   - requirements.txt
   - reset_and_seed.py (untuk inisialisasi database)

2. **File yang TIDAK Perlu Di-upload**
   - `akademik.db` (database akan dibuat di hosting)
   - `venv/` (virtual environment)
   - `__pycache__/`
   - File test (`test_*.py`, `check_*.py`, `verify_*.py`)

3. **Konfigurasi Secret Key**
   
   Untuk production, ganti secret key di `app.py`:
   ```python
   # Ganti ini:
   app.secret_key = 'kunci_rahasia_akademik_anda_yang_sangat_panjang_dan_aman'
   
   # Dengan ini (generate random key):
   import os
   app.secret_key = os.environ.get('SECRET_KEY') or 'your-very-long-random-secret-key-here'
   ```

---

## Deployment ke PythonAnywhere

PythonAnywhere adalah platform hosting Python gratis yang mudah digunakan.

### Langkah-langkah:

1. **Buat Akun**
   - Daftar di [pythonanywhere.com](https://www.pythonanywhere.com)
   - Pilih plan gratis (Beginner)

2. **Upload Files**
   
   **Opsi A: Via Git (Recommended)**
   ```bash
   # Di PythonAnywhere Bash Console
   git clone https://github.com/sangyoga28/akademik_web.git
   cd akademik_web
   ```
   
   **Opsi B: Via Upload**
   - Buka tab "Files"
   - Upload semua file kecuali venv/ dan akademik.db

3. **Setup Virtual Environment**
   ```bash
   # Di Bash Console
   cd akademik_web
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Inisialisasi Database**
   ```bash
   python reset_and_seed.py
   ```

5. **Konfigurasi Web App**
   - Buka tab "Web"
   - Klik "Add a new web app"
   - Pilih "Manual configuration"
   - Pilih Python 3.10
   
   **WSGI Configuration File:**
   ```python
   import sys
   import os
   
   # Path ke project
   path = '/home/yourusername/akademik_web'
   if path not in sys.path:
       sys.path.append(path)
   
   # Activate virtual environment
   activate_this = '/home/yourusername/akademik_web/venv/bin/activate_this.py'
   with open(activate_this) as file_:
       exec(file_.read(), dict(__file__=activate_this))
   
   from app import app as application
   ```

6. **Reload Web App**
   - Klik tombol "Reload" di tab Web
   - Akses aplikasi di `yourusername.pythonanywhere.com`

---

## Deployment ke Railway

Railway adalah platform cloud modern dengan deployment otomatis dari Git.

### Langkah-langkah:

1. **Persiapan File**
   
   Buat file `Procfile` di root project:
   ```
   web: gunicorn app:app
   ```
   
   Update `requirements.txt`:
   ```
   Flask==3.0.0
   Werkzeug==3.0.1
   gunicorn==21.2.0
   ```

2. **Deploy via Railway**
   - Login ke [railway.app](https://railway.app)
   - Klik "New Project"
   - Pilih "Deploy from GitHub repo"
   - Pilih repository `akademik_web`
   - Railway akan auto-detect Python dan deploy

3. **Inisialisasi Database**
   
   Setelah deployment:
   - Buka "Settings" → "Variables"
   - Tambahkan environment variable jika perlu
   - Buka Railway Shell dan jalankan:
   ```bash
   python reset_and_seed.py
   ```

4. **Akses Aplikasi**
   - Railway akan memberikan URL public
   - Akses aplikasi di URL tersebut

---

## Deployment ke VPS (Ubuntu)

Untuk VPS dengan Ubuntu, menggunakan Nginx + Gunicorn.

### Prasyarat:
- VPS dengan Ubuntu 20.04+
- Akses SSH root/sudo
- Domain (opsional)

### Langkah-langkah:

1. **Update System**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Install Dependencies**
   ```bash
   sudo apt install python3-pip python3-venv nginx -y
   ```

3. **Clone Project**
   ```bash
   cd /var/www
   sudo git clone https://github.com/sangyoga28/akademik_web.git
   cd akademik_web
   ```

4. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. **Inisialisasi Database**
   ```bash
   python reset_and_seed.py
   ```

6. **Buat Systemd Service**
   
   File: `/etc/systemd/system/akademik.service`
   ```ini
   [Unit]
   Description=Gunicorn instance for Akademik Web
   After=network.target
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/akademik_web
   Environment="PATH=/var/www/akademik_web/venv/bin"
   ExecStart=/var/www/akademik_web/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable dan start service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start akademik
   sudo systemctl enable akademik
   ```

7. **Konfigurasi Nginx**
   
   File: `/etc/nginx/sites-available/akademik`
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;  # Ganti dengan domain Anda
   
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   
       location /static {
           alias /var/www/akademik_web/static;
       }
   }
   ```
   
   Enable site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/akademik /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

8. **Setup SSL (Opsional tapi Recommended)**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

---

## Deployment ke Shared Hosting (cPanel)

Untuk shared hosting dengan cPanel dan Python support.

### Prasyarat:
- Hosting dengan Python 3.8+ support
- Akses cPanel
- SSH access (opsional)

### Langkah-langkah:

1. **Upload Files via FTP/File Manager**
   - Login ke cPanel
   - Buka File Manager
   - Upload semua file ke `public_html/akademik` atau folder lain
   - Jangan upload `venv/` dan `akademik.db`

2. **Setup Python App (jika tersedia)**
   
   Di cPanel:
   - Cari "Setup Python App" atau "Python Selector"
   - Buat aplikasi baru:
     - Python version: 3.8+
     - Application root: `/home/username/public_html/akademik`
     - Application URL: `/akademik` atau custom
   - Klik "Create"

3. **Install Dependencies**
   
   Via SSH atau Terminal di cPanel:
   ```bash
   cd public_html/akademik
   source venv/bin/activate  # Path mungkin berbeda
   pip install -r requirements.txt
   ```

4. **Konfigurasi .htaccess**
   
   File: `public_html/akademik/.htaccess`
   ```apache
   PassengerAppRoot /home/username/public_html/akademik
   PassengerBaseURI /akademik
   PassengerPython /home/username/public_html/akademik/venv/bin/python
   
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteRule ^(.*)$ /akademik/$1 [QSA,L]
   ```

5. **Buat passenger_wsgi.py**
   
   File: `public_html/akademik/passenger_wsgi.py`
   ```python
   import sys
   import os
   
   # Add project directory to path
   sys.path.insert(0, os.path.dirname(__file__))
   
   from app import app as application
   ```

6. **Inisialisasi Database**
   ```bash
   cd public_html/akademik
   python reset_and_seed.py
   ```

7. **Restart Aplikasi**
   - Di cPanel Python App, klik "Restart"
   - Atau touch file: `touch tmp/restart.txt`

---

## Troubleshooting

### Database Issues

**Problem**: `sqlite3.OperationalError: unable to open database file`

**Solution**:
```bash
# Pastikan folder writable
chmod 755 /path/to/akademik_web
chmod 644 akademik.db  # Setelah database dibuat

# Atau jalankan ulang seeding
python reset_and_seed.py
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Pastikan virtual environment aktif
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install ulang dependencies
pip install -r requirements.txt
```

### Permission Denied

**Problem**: Permission denied saat akses file/database

**Solution**:
```bash
# VPS/Linux
sudo chown -R www-data:www-data /var/www/akademik_web
sudo chmod -R 755 /var/www/akademik_web

# Shared hosting
chmod 755 akademik_web
chmod 644 akademik.db
```

### Port Already in Use

**Problem**: `Address already in use` saat jalankan Flask

**Solution**:
```bash
# Cari process yang menggunakan port
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Kill process atau gunakan port lain
python app.py  # Akan auto-pilih port available
```

### Static Files Not Loading

**Problem**: CSS/JS tidak load di production

**Solution**:
1. Pastikan path static files benar di template:
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
   ```

2. Untuk Nginx, pastikan konfigurasi location /static benar

3. Clear browser cache

### Database Not Persisting

**Problem**: Data hilang setelah restart

**Solution**:
- Pastikan `akademik.db` ada di folder yang persistent
- Jangan gunakan `/tmp` untuk database
- Untuk Railway/Heroku, pertimbangkan upgrade ke PostgreSQL

---

## Checklist Deployment

- [ ] Upload semua file kecuali venv/ dan akademik.db
- [ ] Install dependencies dari requirements.txt
- [ ] Jalankan reset_and_seed.py untuk inisialisasi database
- [ ] Ganti SECRET_KEY untuk production
- [ ] Test login dengan kredensial default
- [ ] Test semua fitur utama (CRUD, KRS, Nilai, KHS)
- [ ] Setup SSL untuk production (HTTPS)
- [ ] Backup database secara berkala

---

## Keamanan Production

1. **Ganti Secret Key**
   ```python
   import secrets
   print(secrets.token_hex(32))  # Generate random key
   ```

2. **Disable Debug Mode**
   ```python
   if __name__ == '__main__':
       app.run(debug=False)  # Set False untuk production
   ```

3. **Gunakan Environment Variables**
   ```python
   import os
   app.secret_key = os.environ.get('SECRET_KEY')
   DATABASE_PATH = os.environ.get('DATABASE_PATH', 'akademik.db')
   ```

4. **Setup HTTPS**
   - Gunakan Let's Encrypt (gratis)
   - Atau SSL dari hosting provider

5. **Backup Database**
   ```bash
   # Backup otomatis dengan cron
   0 2 * * * cp /path/to/akademik.db /path/to/backup/akademik_$(date +\%Y\%m\%d).db
   ```

---

## Support

Jika mengalami masalah deployment:
1. Periksa log error aplikasi
2. Verifikasi semua dependencies ter-install
3. Pastikan Python version compatible (3.8+)
4. Buat issue di GitHub repository

**Selamat Deploy! 🚀**
