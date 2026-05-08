# 🎓 UMS - University Management System

Enterprise-grade University Management System built with Django, Django Ninja, Next.js, and React Native.

## ✨ Features

- **Academic Management** - Faculties, Departments, Programmes, Courses
- **Student Management** - Admissions, Registrations, Results, Attendance
- **Staff Management** - Profiles, Leave, Appraisals
- **Finance** - Fees, Payments, Scholarships, Payroll
- **Learning** - Materials, Assignments, Quizzes
- **Communication** - Announcements, Notifications
- **Reports** - Analytics, Audit Logs

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│  Frontend (Next.js 15) :3000               │
├─────────────────────────────────────────────┤
│  API (Django + Ninja) :8000                │
│  ├── accounts    ├── academic   ├── student │
│  ├── staff       ├── finance    ├── learning│
│  └── ...                                      │
├─────────────────────────────────────────────┤
│  PostgreSQL + Redis + Celery                │
└─────────────────────────────────────────────┘
```

## 🚀 Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

## 📦 Docker

```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.yml up -d --build
```

## 🔐 Authentication

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password"}'

# Response
{
  "success": true,
  "access": "eyJ...",
  "refresh": "eyJ...",
  "user": {...}
}
```

## 📚 API Documentation

See [API_REFERENCE.md](API_REFERENCE.md) for complete API documentation.

## 🛠️ Technology Stack

| Component | Technology |
|------------|------------|
| Backend | Django 5.x + Django Ninja |
| Frontend | Next.js 15 + React |
| Mobile | React Native (Expo) |
| Database | PostgreSQL |
| Cache | Redis |
| Tasks | Celery |
| Deploy | Docker + Kubernetes |

## 📁 Project Structure

```
UMS/
├── backend/          # Django backend
│   ├── apps/       # Django apps
│   ├── unicore/     # Core configuration
│   └── tests/      # Tests
├── frontend/        # Next.js frontend
├── mobile/         # React Native app
├── k8s/           # Kubernetes manifests
├── docker-compose.yml
└── Dockerfile
```

## 🔧 Environment Variables

```env
DEBUG=False
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
POSTGRES_HOST=localhost
POSTGRES_DB=ums
POSTGRES_USER=ums
POSTGRES_PASSWORD=password
REDIS_URL=redis://localhost:6379/0
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

## 📋 Available Commands

```bash
# Backend
python manage.py migrate          # Run migrations
python manage.py createsuperuser # Create admin
python manage.py runserver       # Dev server

# Docker
docker-compose up              # Start all
docker-compose down           # Stop all
docker-compose logs -f       # View logs

# Tests
pytest                        # Run tests
```

## ✅ Production Checklist

- [ ] Set DEBUG=False
- [ ] Configure CORS_ALLOWED_ORIGINS
- [ ] Set strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Configure PostgreSQL (not SQLite)
- [ ] Configure Redis
- [ ] Set up Sentry for error tracking
- [ ] Configure SSL/HTTPS
- [ ] Set Allowed_Hosts

## 📄 License

MIT License

## 👥 Credits

Built with Django, Django Ninja, Next.js, and React Native.
