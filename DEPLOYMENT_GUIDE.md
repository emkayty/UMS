## Quick Install

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python manage.py migrate
python manage.py runserver
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/v1/health/health/` | Liveness check |
| `/api/v1/health/ping/` | Simple ping |
| `/api/v1/health/ready/` | Readiness check |
| `/api/v1/auth/login/` | Login |
| `/api/v1/auth/logout/` | Logout |
| `/api/v1/auth/me/` | Current user |
| `/api/v1/auth/refresh/` | Token refresh |
| `/api/v1/students/` | Student API |
| `/api/v1/staff/` | Staff API |
| `/api/v1/academic/` | Academic API |
| `/api/v1/fees/` | Finance API |
| `/api/v1/learning/` | Learning API |
| `/api/v1/announcements/` | Communications |

## Environment Variables

```
DEBUG=False
SECRET_KEY=<your-secret-key>
JWT_SECRET_KEY=<your-jwt-secret>
POSTGRES_HOST=localhost
POSTGRES_DB=ums
POSTGRES_USER=ums
POSTGRES_PASSWORD=<secure-password>
REDIS_URL=redis://localhost:6379/0
CORS_ALLOWED_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com
SENTRY_DSN=<optional-sentry-dsn>
``"

# ✅ Deployment Complete!

