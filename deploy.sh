#!/bin/bash
# Production Deployment Script
# For Ubuntu/Debian servers

set -e

echo "🎓 UMS Production Deployment"
echo "=============================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root (use sudo)"
    exit 1
fi

# Update system
print_status "Updating system packages..."
apt update -y
apt upgrade -y

# Install required packages
print_status "Installing required packages..."
apt install -y python3 python3-pip python3-venv git curl wget nginx postgresql postgresql-contrib libpq-dev

# Create project directory
print_status "Creating project directory..."
mkdir -p /var/www/ums
cd /var/www/ums

# Clone or update repository
if [ -d ".git" ]; then
    print_status "Updating existing installation..."
    git pull
else
    print_status "Cloning repository..."
    git clone https://github.com/emkayty/UMS.git .
fi

# Create virtual environment
print_status "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# Database setup
print_status "Setting up PostgreSQL..."
systemctl start postgresql
systemctl enable postgresql

# Create database and user
sudo -u postgres psql -c "CREATE DATABASE ums;" 2>/dev/null || true
sudo -u postgres psql -c "CREATE USER ums_user WITH PASSWORD 'change_password';" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ums TO ums_user;" 2>/dev/null || true
sudo -u postgres psql -c "ALTER USER ums_user CREATEDB;" 2>/dev/null || true

# Set environment variables
print_status "Configuring environment..."
cat > .env << EOF
DJANGO_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(50))')
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://ums_user:change_password@localhost:5432/ums
EOF

# Run migrations
print_status "Running database migrations..."
cd backend
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser (optional)
print_warning "Creating admin user..."
python manage.py createsuperuser

# Setup systemd service
print_status "Setting up systemd service..."
cat > /etc/systemd/system/ums.service << EOF
[Unit]
Description=UMS Django Application
After=network.target postgresql.service

[Service]
Type=spawning
User=www-data
Group=www-data
WorkingDirectory=/var/www/ums/backend
Environment=/var/www/ums/venv/bin/activate
ExecStart=/var/www/ums/venv/bin/gunicorn unicore.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
systemctl daemon-reload
systemctl enable ums
systemctl start ums

# Setup Nginx
print_status "Setting up Nginx..."
cat > /etc/nginx/sites-available/ums << EOF
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/ums/staticfiles/;
    }

    location /media/ {
        alias /var/www/ums/backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable Nginx configuration
ln -sf /etc/nginx/sites-available/ums /etc/nginx/sites-enabled/
nginx -t

# Restart Nginx
systemctl restart nginx
systemctl enable nginx

print_status "=========================="
print_status "Deployment complete!"
print_status ""
print_status "API: http://yourdomain.com"
print_status "Admin: http://yourdomain.com/admin"
print_status ""
print_warning "Remember to:"
print_warning "1. Update ALLOWED_HOSTS in .env"
print_warning "2. Configure domain in Nginx"
print_warning "3. Set up SSL certificate (letsencrypt)"
print_warning "=========================="