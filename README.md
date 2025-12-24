# Class Scheduling Management System

A comprehensive FastAPI-based system for managing university class schedules, supporting manual schedule creation, automated generation, and conflict detection.

## Features

- 🎓 Multi-faculty/department support
- 👥 User role management (Admin, Dean, Department Representative)
- 📅 Term-based scheduling
- 🏫 Classroom management with capacity and feature tracking
- 👨‍🏫 Instructor availability management
- ⚠️ Real-time conflict detection
- 🤖 Auto-schedule generation with constraint satisfaction
- 📊 Analytics and reporting
- ✅ Approval workflow for schedules

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy (Async)
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic v2

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- pip or uv

## Installation

1. Clone repository

```bash
git clone <repository-url>
cd UniProj
```

2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
# or using uv
uv pip install -r requirements.txt
```

4. Setup environment variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database_name
SECRET_KEY=your-secret-key-min-32-characters-long
```

5. Initialize database

```bash
# Create database migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

6. Run application

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
UniProj/
├── app/
│   ├── api/              # API endpoints
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── router.py
│   ├── core/             # Core functionality
│   │   ├── security.py   # JWT, password hashing
│   │   ├── logging.py    # Logging configuration
│   │   └── constants.py  # Enums and constants
│   ├── db/               # Database configuration
│   │   ├── session.py    # Async session management
│   │   └── base.py       # Base for Alembic
│   ├── models/           # SQLAlchemy ORM models
│   ├── repositories/     # Data access layer
│   ├── schemas/          # Pydantic models
│   ├── services/         # Business logic
│   ├── utils/            # Utility functions
│   └── main.py           # Application entry point
├── alembic/              # Database migrations
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
└── README.md
```

## Usage Examples

### Authentication

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password"}'
```

### Create Faculty

```bash
curl -X POST "http://localhost:8000/api/v1/faculties" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"code": "ENG", "name": "Engineering Faculty"}'
```

### Create Schedule

```bash
curl -X POST "http://localhost:8000/api/v1/schedules" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"term_id": "uuid", "department_id": "uuid"}'
```

## Development

### Run tests

```bash
pytest
```

### Create migration

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Code formatting

```bash
black app/
isort app/
```

## Database Schema

The system includes the following main entities:

- **Faculties**: University faculties
- **Departments**: Departments within faculties
- **Terms**: Academic terms (Spring/Fall)
- **Users**: System users (Admin, Dean, Department Rep)
- **Instructors**: Course instructors
- **Courses**: Course definitions
- **Classrooms**: Available classrooms
- **Time Slots**: Available time slots for scheduling
- **Schedules**: Department schedules for terms
- **Schedule Assignments**: Course assignments to time slots

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Role-based access control (RBAC)
- Input validation using Pydantic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[License information]

