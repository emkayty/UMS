# 🚀 PRODUCTION DEPLOYMENT CHECKLIST

## Pre-Deployment Verification

### ✅ Backend
- [ ] All Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Database migrations applied (`python manage.py migrate`)
- [ ] Static files collected (`python manage.py collectstatic --noinput`)
- [ ] Environment variables configured
- [ ] DEBUG set to `False` in production
- [ ] ALLOWED_HOSTS configured
- [ ] Database connection verified (PostgreSQL)
- [ ] Redis connection verified

### ✅ Security
- [ ] SECRET_KEY generated and secure
- [ ] HTTPS/SSL configured
- [ ] CORS origins restricted
- [ ] Rate limiting enabled
- [ ] Admin URL changed from default (/admin/)
- [ ] All security middleware enabled

### ✅ Frontend
- [ ] Environment variables configured
- [ ] API_BASE_URL pointing to production
- [ ] Build successful (`npm run build`)
- [ ] Static files served via CDN (production)

### ✅ Mobile
- [ ] API endpoint configured
- [ ] Push notification credentials set
- [ ] Build successful (Expo/React Native)

---

## Environment Configuration

### Backend (.env)
```bash
# Required
DJANGO_SECRET_KEY=<secure-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@host:5432/ums
REDIS_URL=redis://localhost:6379/0

# Optional (with defaults)
EMAIL_HOST_USER=smtp-user
EMAIL_HOST_PASSWORD=smtp-password
SENTRY_DSN=https://key@sentry.io/project

# Nigerian Payment (Remita)
REMITA_MERCHANT_ID=
REMITA_API_KEY=
REMITA_ENV=test|live
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com
NEXT_PUBLIC_API_PREFIX=/api/v1
```

---

## Post-Deployment Verification

### Health Checks
```bash
# Backend health
curl https://api.yourdomain.com/health/ping/

# Database
python manage.py dbshell

# Celery
celery -A umsInspect worker -l info

# Redis
redis-cli ping
```

### Smoke Tests
- [ ] Login flow works
- [ ] Student profile loads
- [ ] Course registration works
- [ ] Payment initiates
- [ ] Results display
- [ ] File upload works

---

## Monitoring Setup

### Recommended Tools
| Tool | Purpose | Setup |
|------|--------|-------|
| Sentry | Error tracking | Set SENTRY_DSN in .env |
| Datadog | APM & metrics | Install agent |
| Prometheus | Metrics | Enable `/metrics` endpoint |
| CloudWatch | AWS logs | Configure in CloudFormation |
|PagerDuty | Alerting | Configure webhooks |

---

## Rollback Procedure

### Quick Rollback
```bash
# Revert to previous image
docker pull yourorg/ums:previous-tag
docker-compose up -d

# Or revert database (backup required)
python manage.py migrate app_name <migration_name>
```

### Database Rollback
```bash
# Only if absolutely necessary
python manage.py migrate app_name <previous_migration> --fake
```

---

## Deployment Timeline

| Phase | Time | Notes |
|-------|------|-------|
| Pre-check | 5 min | Verify all checks |
| Database backup | 5 min | Full backup |
| Migrate | 2 min | Apply migrations |
| Build | 5 min | Docker + push |
| Deploy | 3 min | Rolling update |
| Verify | 5 min | Smoke tests |
| **Total** | **~25 min** | |

---

*Checklist Version: 1.0.0*
*Updated: 2026-05-08*