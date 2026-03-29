# CitizenService — Django Capstone Project

A RESTful backend API for a digital government service request platform.
Citizens can submit and track requests; officers review and process them.

---

## Tech Stack

- Python 3.11 / Django 4.2
- Django REST Framework (ViewSets, serializers, pagination, filtering)
- JWT Authentication — djangorestframework-simplejwt
- Role-Based Access Control (RBAC) — citizen, officer, admin roles
- SQLite (development) — easily swappable for PostgreSQL
- Gunicorn — production WSGI server
- Docker + docker-compose

---

## Project Structure
```
citizenservice/   → project settings and root URL config
users/            → custom user model, registration, profile, RBAC permissions
services/         → service request and category models, CRUD API
common/           → shared utility functions
```

---

## API Endpoints

### Authentication
| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/auth/register/ | Register a new user |
| GET/PATCH | /api/auth/profile/ | View or update your profile |
| POST | /api/token/ | Login — returns JWT access + refresh token |
| POST | /api/token/refresh/ | Get a new access token |

### Service Requests
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/requests/ | List requests (filtered by role) |
| POST | /api/requests/ | Submit a new request (citizens) |
| GET | /api/requests/{id}/ | Retrieve a single request |
| PATCH | /api/requests/{id}/ | Update a request |
| DELETE | /api/requests/{id}/ | Delete a request |
| GET | /api/requests/my/ | Your own requests |

### Categories
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/categories/ | List all service categories |
| GET | /api/categories/{id}/ | Retrieve one category |

### Filtering & Pagination
```
GET /api/requests/?status=pending
GET /api/requests/?priority=high
GET /api/requests/?status=in_review&priority=medium
GET /api/requests/?search=birth+certificate
GET /api/requests/?ordering=-created_at
GET /api/requests/?page=2
```

---

## Setup (Local Development)
```bash
# 1. Clone the repository
git clone https://github.com/IbrahimAce/django-capstone-citizenservice
cd django-capstone-citizenservice

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env and set a real SECRET_KEY

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver
```

---

## Key Design Decisions

**Modular apps** — `users`, `services`, and `common` are separate Django apps
rather than a single monolithic structure, demonstrating clean architecture
and separation of concerns.

**DRF ViewSets** — `ModelViewSet` with `DefaultRouter` automatically generates
all CRUD endpoints, reducing boilerplate while keeping the code readable.

**Custom RBAC** — `users/permissions.py` defines `IsCitizen`, `IsOfficer`,
`IsOfficerOrAdmin`, and `IsAdminRole` permission classes. The `get_queryset()`
method in `ServiceRequestViewSet` enforces data isolation: citizens only see
their own requests.

**ORM Optimisation** — `select_related('citizen', 'assigned_officer', 'category')`
is used on every queryset that accesses related fields, avoiding the N+1 query
problem and keeping database load minimal.

**Two serializers for one model** — `ServiceRequestCreateSerializer` (for POST)
and `ServiceRequestSerializer` (for GET) are kept separate. This prevents
citizens from setting fields like `status` or `notes` during creation — a
deliberate security design rather than using conditional logic in one serializer.

**Local cache now, Redis later** — Django's `LocMemCache` is used for this
submission to meet the deadline. The Redis configuration is stubbed in
`settings.py` with TODO comments for the April 16 version.

**Celery stubbed** — Background task infrastructure (Celery + Redis broker)
is commented out in both `settings.py` and `docker-compose.yml`, ready to
be activated in the April 16 production version.

---

## Planned for April 16 Version

- Celery + Redis for async background tasks (email notifications on status changes)
- Redis as the shared cache backend (replacing LocMemCache)
- Full docker-compose with web + redis + celery worker services
- PostgreSQL database for production deployment

---

## Author

Ibrahim Karanja — BSc Computer Science, Dedan Kimathi University of Technology  
GitHub: [IbrahimAce](https://github.com/IbrahimAce)
