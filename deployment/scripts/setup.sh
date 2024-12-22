#!/bin/bash

ENVIRONMENT=$1
DJANGO_SECRET_KEY=$2

# Update system
apt-get update
apt-get upgrade -y

# Install required packages
apt-get install -y python3-pip python3-venv nginx supervisor git

# Create app user
useradd -m -s /bin/bash market2hand

# Create directories
mkdir -p /var/www/market2hand
mkdir -p /var/log/market2hand
chown -R market2hand:market2hand /var/www/market2hand /var/log/market2hand

# Clone repository
git clone https://github.com/yourusername/market2hand.git /var/www/market2hand
chown -R market2hand:market2hand /var/www/market2hand

# Setup Python virtual environment
sudo -u market2hand python3 -m venv /var/www/market2hand/venv

# Install requirements
sudo -u market2hand /var/www/market2hand/venv/bin/pip install -r /var/www/market2hand/requirements.txt
sudo -u market2hand /var/www/market2hand/venv/bin/pip install gunicorn

# Setup environment variables
cat > /var/www/market2hand/.env <<EOL
DJANGO_SETTINGS_MODULE=market2hand.settings
DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
DEBUG=0
ALLOWED_HOSTS=*
EOL

# Copy configurations
cp /tmp/configs/nginx.conf /etc/nginx/sites-available/market2hand
cp /tmp/configs/supervisor.conf /etc/supervisor/conf.d/market2hand.conf

# Enable Nginx site
ln -sf /etc/nginx/sites-available/market2hand /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Collect static files
sudo -u market2hand /var/www/market2hand/venv/bin/python manage.py collectstatic --noinput

# Apply migrations
sudo -u market2hand /var/www/market2hand/venv/bin/python manage.py migrate

# Restart services
systemctl restart nginx
supervisorctl reread
supervisorctl update
supervisorctl restart market2hand 