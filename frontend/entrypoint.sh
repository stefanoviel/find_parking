#!/bin/sh

# Replace API_URL in all HTML files
find /usr/share/nginx/html -type f -name "*.html" -exec sed -i "s|window.API_URL|'${API_URL}'|g" {} \;

# Start nginx
exec "$@" 