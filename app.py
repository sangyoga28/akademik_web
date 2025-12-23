from flask import Flask, session
import repository as repo
from routes import auth_bp, admin_bp, dosen_bp, mahasiswa_bp, general_bp

# ----------------- SETUP APLIKASI -----------------

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_akademik_anda_yang_sangat_panjang_dan_aman' 

# ----------------- REGISTER BLUEPRINT -----------------

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(dosen_bp)
app.register_blueprint(mahasiswa_bp)
app.register_blueprint(general_bp)

# ----------------- CONTEXT PROCESSOR -----------------

@app.context_processor
def inject_totals():
    if session.get('logged_in') and session.get('role') == 'Admin Sistem':
        try:
            conn = repo.get_db() # Use repo's get_db connection or general.get_db
            # Note: Context processor runs disjointly from route scope usually, but g context is active.
            # Using repo.get_db() is safer if we ensure connection closing.
            # Or use explicit try-except without relying on 'g' if outside request context? 
            # Flask context processor runs IN request context.
            # However, repo.get_db() checks g._database.
            
            # To be safe and consistent with previous app.py logic:
            count = repo.hitung_pendaftaran_pending(conn)
            return dict(nav_total_pending=count)
        except:
            pass
    return dict(nav_total_pending=0)

@app.teardown_appcontext
def close_connection(exception):
    repo.close_connection(exception)

# ----------------- INIT DB -----------------

with app.app_context():
    conn = repo.get_db()
    repo.buat_tabel(conn)

if __name__ == '__main__':
    app.run(debug=True, port=5000)