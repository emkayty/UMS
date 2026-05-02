#!/bin/bash

# UniCore Provisioning Script
# Usage: ./provision.sh <slug> <domain> <admin_email> [admin_password]

set -e

SLUG="${1:-}"
DOMAIN="${2:-}"
ADMIN_EMAIL="${3:-}"
ADMIN_PASSWORD="${4:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}UniCore Provisioning Script${NC}"
echo "================================"

# Validate input
if [ -z "$SLUG" ]; then
    echo -e "${RED}Error: Institution slug is required${NC}"
    echo "Usage: ./provision.sh <slug> <domain> <admin_email> [admin_password]"
    exit 1
fi

if [ -z "$DOMAIN" ]; then
    echo -e "${RED}Error: Domain is required${NC}"
    exit 1
fi

if [ -z "$ADMIN_EMAIL" ]; then
    echo -e "${RED}Error: Admin email is required${NC}"
    exit 1
fi

# Generate password if not provided
if [ -z "$ADMIN_PASSWORD" ]; then
    ADMIN_PASSWORD=$(openssl rand -base64 12 | tr -d '=' | head -c 16)
    echo -e "${YELLOW}Generated admin password: $ADMIN_PASSWORD${NC}"
fi

# Generate secrets
DB_PASSWORD=$(openssl rand -base64 24 | tr -d '=' | head -c 32)
DJANGO_SECRET=$(openssl rand -base64 32 | tr -d '=')
JWT_SECRET=$(openssl rand -base64 32 | tr -d '=')

echo ""
echo "Creating instance: $SLUG"
echo "Domain: $DOMAIN"
echo ""

# Create environment file
cat > .env << EOF
# Database
POSTGRES_DB=unicore_${SLUG}
POSTGRES_USER=unicore_${SLUG}
POSTGRES_PASSWORD=${DB_PASSWORD}
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Django
DJANGO_SECRET_KEY=${DJANGO_SECRET}
JWT_SECRET_KEY=${JWT_SECRET}
DJANGO_DEBUG=False
ALLOWED_HOSTS=${DOMAIN},localhost,127.0.0.1

# Institution
INSTITUTION_SLUG=${SLUG}
INSTITUTION_DOMAIN=${DOMAIN}
EOF

echo -e "${GREEN}✓ Environment file created${NC}"

# Create PostgreSQL database
echo "Creating database..."
PGPASSWORD="$DB_PASSWORD" psql -h localhost -U postgres -c "CREATE USER unicore_${SLUG} WITH PASSWORD '${DB_PASSWORD}';" 2>/dev/null || true
PGPASSWORD="$DB_PASSWORD" psql -h localhost -U postgres -c "CREATE DATABASE unicore_${SLUG} OWNER unicore_${SLUG};" 2>/dev/null || true
PGPASSWORD="$DB_PASSWORD" psql -h localhost -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE unicore_${SLUG} TO unicore_${SLUG};" 2>/dev/null || true

echo -e "${GREEN}✓ PostgreSQL database created${NC}"

# Create instance directory
mkdir -p instances/${SLUG}
cp -r backend/* instances/${SLUG}/backend/ || mkdir -p instances/${SLUG}/backend
cp -r frontend/* instances/${SLUG}/frontend/ || mkdir -p instances/${SLUG}/frontend
cp docker-compose.yml instances/${SLUG}/
cp .env instances/${SLUG}/

echo -e "${GREEN}✓ Instance files copied${NC}"

# Build and start containers
cd instances/${SLUG}
docker compose up -d --build

echo -e "${GREEN}✓ Containers started${NC}"

# Run migrations
echo "Running migrations..."
docker compose exec -T backend python manage.py migrate --noinput || true

# Collect static files
docker compose exec -T backend python manage.py collectstatic --noinput || true

# Create superuser
echo "Creating admin user..."
docker compose exec -T backend python manage.py createsuperuser --noinput \
    --email="$ADMIN_EMAIL" \
    --skip-checks || true

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Provisioning Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Institution: $SLUG"
echo "Domain: $DOMAIN"
echo "Admin URL: https://${DOMAIN}/admin"
echo "API URL: https://${DOMAIN}/api/v1"
echo ""
echo "Admin credentials:"
echo "  Email: $ADMIN_EMAIL"
echo "  Password: $ADMIN_PASSWORD"
echo ""
echo "Next steps:"
echo "1. Run the setup wizard at https://${DOMAIN}/setup"
echo "2. Configure your institution details"
echo "3. Start using UniCore!"
echo ""