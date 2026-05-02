# 🖥️ UniCore Local Setup (MacBook Air)

## Quick Start (5 minutes)

### 1. Clone & Navigate
```bash
cd ~/Downloads
git clone https://github.com/emkayty/UMS.git
cd UMS
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Follow prompts for email/password

# Start server
python manage.py runserver
```

Server runs at: **http://localhost:8000**

### 3. Frontend Setup (New Terminal)
```bash
cd UMS/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: **http://localhost:3000**

---

## Quick Test (Verify It's Working)

### In Browser:
1. Open http://localhost:8000/admin → Login with superuser
2. Open http://localhost:3000 → Login page

### API Test:
```bash
curl http://localhost:8000/api/v1/health/
```

---

## If You Get Errors

### "command not found: python3"
```bash
# Use python instead
python manage.py runserver
```

### Port Already in Use
```bash
# Kill existing processes
lsof -i :8000 | grep Python | awk '{print $2}' | xargs kill
# Or use different port
python manage.py runserver 8001
```

### Database Error
```bash
# Already edited settings.py to use SQLite (no setup needed)
python manage.py migrate
```

---

## What's Included

| Component | URL | Credentials |
|-----------|-----|-------------|
| Admin Panel | localhost:8000/admin | superuser |
| API Docs | localhost:8000/api | - |
| Frontend | localhost:3000 | auto-login |

## Stop Server
```bash
# Press Ctrl+C in terminal
```
