# Multi-stage build for UMS (Django + Next.js)

# ============================================================
# STAGE 1: Backend (Python/Django)
# ============================================================
FROM python:3.10-slim as backend

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "unicore.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]


# ============================================================
# STAGE 2: Frontend (Node.js) - Optional
# ============================================================
FROM node:18-alpine as frontend

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend/package*.json ./
COPY frontend/package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]


# ============================================================
# FINAL STAGE: Production image
# ============================================================
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create working directories
RUN mkdir -p /var/www/ums /var/www/ums/staticfiles /var/www/ums/media

# Copy built artifacts from previous stages
COPY --from=backend /app /var/www/ums/backend
COPY --from=backend /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy frontend build (if built separately)
# COPY --from=frontend /app/.next /var/www/ums/frontend/.next

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=unicore.settings \
    DATABASE_URL=sqlite:///db.sqlite3

# Set working directory
WORKDIR /var/www/ums

# Copy startup script
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Start application
CMD ["/startup.sh"]