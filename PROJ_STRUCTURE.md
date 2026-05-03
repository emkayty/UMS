# 🎓 UMS - ORGANIZED PROJECT STRUCTURE
# Modular, Systemized, Professional Architecture

---

## 📁 ORGANIZED STRUCTURE

```
UMS/
├── backend/
│   ├── unicore/              # Django Project Settings
│   │   ├── __init__.py
│   │   ├── settings.py        # Base settings
│   │   ├── settings_production.py  # Production config
│   │   ├── urls.py         # URL routing
│   │   ├── wsgi.py        # WSGI
│   │   ├── asgi.py        # ASGI
│   │   └── exceptions.py   # Global exceptions
│   │
│   ├── apps/                # Django Apps
│   │   ├── core/          # Core utilities (15 modules)
│   │   │   ├── __init__.py
│   │   │   ├── api.py      # Core API
│   │   │   ├── base.py    # Base classes ⭐ NEW
│   │   │   ├── serializers.py  # Serializers ⭐ NEW
│   │   │   ├── viewsets.py  # Viewsets ⭐ NEW
│   │   │   ├── models.py  # Core models
│   │   │   ├── managers.py  # Query managers
│   │   │   ├── utils.py   # Utilities
│   │   │   ├── validators.py  # Validators
│   │   │   ├── signals.py  # Django signals
│   │   │   ├── audit.py  # Audit logging
│   │   │   ├── rate_limit.py  # Rate limiting
│   │   │   ├── health.py    # Health checks
│   │   │   ├── monitoring.py  # Monitoring
│   │   │   ├── enterprise.py  # Enterprise logic
│   │   │   ├── enterprise_api.py  # Enterprise API
│   │   │   ├── tests.py  # Tests
│   │   │   └── tests_full.py  # Comprehensive tests
│   │   │
│   │   ├── accounts/       # User management
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   ├── models.py
│   │   │   ├── two_factor.py  # 2FA ⭐ NEW
│   │   │   ├── authentication.py
│   │   │   └── lifecycle_*.py
│   │   │
│   │   ├── academic/       # Academic management
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── models.py
│   │   │
│   │   ├── student/       # Student management
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── models.py
│   │   │
│   │   ├── staff/        # Staff management
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── models.py
│   │   │
│   │   ├── institution/   # Institution settings
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── models.py
│   │   │
│   │   ├── finance/      # Finance & fees
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── models.py
│   │   │
│   │   ├── learning/     # Courses & learning
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── models.py
│   │   │
│   │   ├── communication/  # Messages & notifications
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── models.py
│   │   │
│   │   ├── reports/      # Reports & analytics
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── models.py
│   │   │
│   │   ├── lifecycle/    # Attendance & events
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── models.py
│   │   │
│   │   └── offline/      # Offline sync
│   │       ├── __init__.py
│   │       ├── api.py
│   │       └── models.py
│   │
│   ├── conftest.py      # Pytest config
│   ├── manage.py
│   ├── pytest.ini
│   └── requirements.txt
│
├── frontend/             # Next.js Frontend
│   ├── src/
│   │   ├── app/       # App router
│   │   │   ├── (dashboard)/
│   │   │   │   └── page.tsx
│   │   │   └── setup/
│   │   │       └── page.tsx
│   │   ├── components/  # UI components
│   │   │   ├── UX.tsx
│   │   │   ├── index.tsx
│   │   │   └── ...
│   │   └── config/     # Config
│   └── package.json
│
├── mobile/              # React Native/Expo
│   ├── src/            # Screens
│   ├── App.tsx         # Main app
│   └── app.json        # Config
│
├── .github/            # CI/CD
│   └── workflows/
│       └── ci-cd.yml
│
├── docker-compose.yml
├── README.md
└── PROJ_STRUCTURE.md   # This file

```

---

## 🎯 CORE MODULES REORGANIZED

### Core App (15 Modules)

| Module | Purpose | Status |
|--------|---------|-------|
| `base.py` | **NEW** - Base classes & constants | ✅ |
| `serializers.py` | **NEW** - Abstract serializers | ✅ |
| `viewsets.py` | **NEW** - Abstract viewsets | ✅ |
| `models.py` | Core models | ✅ |
| `managers.py` | Query managers | ✅ |
| `utils.py` | Utilities | ✅ |
| `validators.py` | Validators | ✅ |
| `signals.py` | Django signals | ✅ |
| `audit.py` | Audit logging | ✅ |
| `rate_limit.py` | Rate limiting | ✅ |
| `health.py` | Health checks | ✅ |
| `monitoring.py` | Monitoring | ✅ |
| `api.py` | Core API | ✅ |
| `enterprise.py` | Enterprise | ✅ |
| `enterprise_api.py` | Enterprise API | ✅ |

---

## ✨ NEW STANDARDIZED MODULES

### 1. base.py (NEW)
- Base managers (UUID, SoftDelete, Base)
- Base models (UUIDModel, TimestampModel, SoftDeleteModel, StatusModel, BaseModel)
- Validators (Nigerian phone, state, year, age)
- Constants (Nigerian states, grading scales)
- Helper functions (generate_enrollment, generate_invoice, format_currency, calculate_gpa)

### 2. serializers.py (NEW)
- BaseSerializer
- ReadOnlySerializer
- NestedSerializer
- ChoiceField enhancements
- Validation serializers
- Filter serializers (pagination, ordering)
- Response serializers (paginated, error, success)
- Helper mixins (Timestamp, Status, User)
- Export serializer

### 3. viewsets.py (NEW)
- BaseViewSet (with common functionality)
- ReadOnlyViewSet
- CreateViewSet
- UpdateViewSet
- DeleteViewSet (soft delete)
- BasePagination
- BaseFilterSet
- Permission classes (IsOwnerOrReadOnly, IsStaffOrReadOnly, IsAdminOrReadOnly)
- Action mixins (activate, deactivate, archive, restore, export)
- Logging mixin

---

## 📋 STANDARD PATTERNS

### Models
```python
from apps.core.base import BaseModel, BaseModelWithStatus

class MyModel(BaseModelWithStatus):
    name = models.CharField(max_length=100)
    # Inherits: uuid, created_at, updated_at, is_active, is_public, created_by, updated_by
```

### Serializers
```python
from apps.core.serializers import BaseSerializer

class MyModelSerializer(BaseSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

### Viewsets
```python
from apps.core.viewsets import BaseViewSet, BaseActionMixin

class MyModelViewSet(BaseActionMixin, BaseViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    select_related = ['created_by']
```

---

## 🔗 RELATIONSHIPS

```
BaseModel (inherit chain)
    ├── UUIDModel
    │   └── uuid (UUID)
    ├── TimestampModel
    │   ├── created_at
    │   └── updated_at
    └── BaseModel
        ├── is_active
        ├── is_public
        ├── created_by (FK → User)
        └── updated_by (FK → User)

BaseModelWithStatus inherits:
    └── StatusModel
        └── status (DRAFT/PENDING/ACTIVE/INACTIVE/ARCHIVED)
```

---

*Generated: 2026-05-02*
*Status: ORGANIZED & STANDARDIZED*