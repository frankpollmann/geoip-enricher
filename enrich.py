import os
import psycopg2
import geoip2.database

# Look for the downloaded .mmdb file
mmdb_file = next((f for f in os.listdir('.') if f.endswith('.mmdb')), None)
if not mmdb_file:
    raise FileNotFoundError("❌ GeoLite2 .mmdb file not found in working directory.")

reader = geoip2.database.Reader(mmdb_file)

# Connect to PostgreSQL using environment variables
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    port=os.environ.get('DB_PORT', 5432),
    database=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASS']
)
cur = conn.cursor()

# Create enrichment table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS cti_geo (
        ip TEXT PRIMARY KEY,
        country TEXT
    );
""")

# Select all CAPI-originated IPs
cur.execute("SELECT DISTINCT value FROM decisions WHERE origin = 'CAPI'")
ips = [row[0] for row in cur.fetchall()]

# Insert country for each IP
for ip in ips:
    try:
        country = reader.country(ip).country.iso_code
    except:
        country = 'Unknown'
    cur.execute("""
        INSERT INTO cti_geo (ip, country)
        VALUES (%s, %s)
        ON CONFLICT (ip) DO NOTHING;
    """, (ip, country))

# Commit and close
conn.commit()
cur.close()
conn.close()
reader.close()

print(f"✅ Enrichment complete for {len(ips)} IPs.")
