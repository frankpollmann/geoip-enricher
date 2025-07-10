#!/bin/bash

DB_URL="https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key=${LICENSE_KEY}&suffix=tar.gz"

wget -qO - "$DB_URL" | tar xz --strip-components=1 --wildcards --no-anchored '*.mmdb' -C /app

python /app/enrich.py