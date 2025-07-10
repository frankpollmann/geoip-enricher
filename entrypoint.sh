#!/bin/bash

echo "📦 Downloading GeoLite2 database..."

DB_URL="https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key=${LICENSE_KEY}&suffix=tar.gz"

# Download and extract .mmdb, with error handling
if wget -qO - "$DB_URL" | tar xz --strip-components=1 --wildcards --no-anchored '*.mmdb' -C /app; then
  echo "✅ GeoLite2 downloaded successfully"
  echo "🚀 Starting enrichment..."
  python /app/enrich.py
else
  echo "❌ Failed to download GeoLite2. Check your LICENSE_KEY or network connection."
  exit 1
fi
