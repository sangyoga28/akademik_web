import sqlite3

conn = sqlite3.connect('akademik.db')
cur = conn.cursor()

# Get all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()

print('=' * 80)
print('DAFTAR TABEL DALAM DATABASE')
print('=' * 80)
for table in tables:
    print(f"- {table[0]}")

print('\n' + '=' * 80)
print('STRUKTUR TABEL')
print('=' * 80)

for table in tables:
    table_name = table[0]
    print(f"\n{table_name}:")
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = cur.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")

conn.close()
