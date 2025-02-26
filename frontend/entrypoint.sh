#!/bin/sh

# Replace API_URL in all HTML files
find /usr/share/nginx/html -type f -name "*.html" -exec sed -i "s|window.API_URL|'${API_URL}'|g" {} \;

# Your domain name
DOMAIN="myparking.online/"

# Check if certificates already exist
if [ ! -f /etc/letsencrypt/live/$DOMAIN/fullchain.pem ]; then
    # Get certificates for the first time
    certbot --nginx \
            --non-interactive \
            --agree-tos \
            --email viel.stefano01@gmail.com \
            -d $DOMAIN \
            --redirect

    # Set up auto-renewal
    (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
fi

# Start nginx
exec "$@" 