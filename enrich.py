import os
import psycopg2
import geoip2.database

mmdb_file = next(f for f in os.listdir('.') if f.endswith('.mmdb'))
reader = geoip2.database.Reader(mmdb_file)

conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    port=os.environ.get('DB_PORT', 5432),
    database=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS']
)
cur = conn.cursor()

cur.execute("SELECT DISTINCT value FROM decisions WHERE origin = 'CAPI'")
ips = [row[0] for row in cur.fetchall()]

cur.execute("""
    CREATE TABLE IF NOT EXISTS cti_geo (
        ip TEXT PRIMARY KEY,
        country TEXT
    )
""")

for ip in ips:
    try:
        country = reader.country(ip).country.iso_code
    except:
        country = 'Unknown'
    cur.execute("""
        INSERT INTO cti_geo (ip, country)
        VALUES (%s, %s)
        ON CONFLICT (ip) DO NOTHING
    """, (ip, country))

conn.commit()
cur.close()
conn.close()
reader.close()
