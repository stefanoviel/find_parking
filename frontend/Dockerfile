FROM nginx:alpine

# Remove the COPY command since we're using volumes
# COPY map.html /usr/share/nginx/html/index.html

# Rename your map.html to index.html in your local directory
# or add this nginx configuration to serve map.html as the index
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Nginx runs on port 80 by default
EXPOSE 80