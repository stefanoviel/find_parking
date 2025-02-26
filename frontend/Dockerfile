FROM nginx:mainline

# Install certbot and its nginx plugin
RUN apk add --no-cache certbot certbot-nginx

# Remove the COPY command since we're using volumes
# COPY map.html /usr/share/nginx/html/index.html

# Rename your map.html to index.html in your local directory
# or add this nginx configuration to serve map.html as the index
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Nginx runs on port 80 by default
EXPOSE 80 443

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]