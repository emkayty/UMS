# UniCore - University Operating System

A production-ready, white-label university web portal built with Django 5.1 + Next.js 15.

## ✨ Features

- **7 Role-Based Dashboards**: Student, Lecturer, HOD, Dean, Registrar, Bursar, Admin
- **Complete Academic Workflow**: Admission → Registration → Results → Graduation
- **Finance Module**: Fees, Payments, Scholarships, Payroll
- **Learning Management**: Materials, Quizzes, Assignments, Attendance (QR)
- **Nigerian Standards**: NUC, JAMB, NYSC, WAEC compliance
- **Global Standards**: GDPR/NDPR, WCAG 2.1 AA, Bologna/ECTS
- **Modern UI/UX**: Dark mode, animations, glassmorphism

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 16+
- Redis (optional)

### Backend Setup
```bash
cd backend
cp .env.example .env  # Edit with your values
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker (Alternative)
```bash
docker-compose up -d
```

## 📁 Project Structure

```
backend/
├── apps/
│   ├── accounts/      # Authentication
│   ├── academic/     # Faculty, Department, Programme, Course
│   ├── student/     # Student lifecycle
│   ├── staff/       # Staff management
│   ├── learning/   # Materials, Quizzes, Attendance
│   ├── finance/    # Fees, Payments
│   └── communication/ # Announcements, SMS
frontend/
├── src/
│   ├── app/        # Next.js pages
│   ├── components/ # UI components
│   └── lib/        # Utilities
mobile/
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Enable debug mode | False |
| SECRET_KEY | Django secret key | Required |
| POSTGRES_* | Database config | Required |
| JWT_SECRET_KEY | JWT signing key | Required |

## 📱 Mobile App

```bash
cd mobile
npm install
expo start
```

## 🧪 Testing

```bash
# Backend
pytest

# Frontend
npm test
```

## 🔐 Security

- JWT authentication
- CORS + CSRF protection
- Password validators
- Audit logging

## 📄 License

MIT License
