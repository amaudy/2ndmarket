# Development Setup Guide

## System Requirements

### Core Technologies
- Python 3.12
- Django 5.1.4
- SQLite3 (Development)
- Docker & Docker Compose

### Required Python Packages
```txt
# Web Framework
Django==5.1.4
python-dotenv==1.0.0

# Image Processing
Pillow==10.1.0

# Forms & Validation
django-crispy-forms==2.1
crispy-tailwind==0.5.0

# Authentication
django-allauth==0.59.0

# Payment Processing
stripe==7.10.0

# Testing
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0

# Development Tools
django-debug-toolbar==4.2.0
black==23.11.0
flake8==6.1.0
```

## Environment Setup

### 1. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

### 2. Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install Tailwind CSS
npm install -D tailwindcss
npx tailwindcss init
```

### 3. Environment Variables
Create `.env` file in project root:
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Stripe Settings
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret

# File Storage Settings
MEDIA_URL=/media/
MEDIA_ROOT=media
```

### 4. Database Setup
```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Load initial data
python manage.py loaddata categories
python manage.py loaddata test_products
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

## Development Server

### Start Development Server
```bash
# Start Django server
python manage.py runserver

# In another terminal, start Tailwind CSS
npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch
```

## Testing Setup

### Run Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_listings.py
```

## Development Tools

### Code Formatting
```bash
# Format Python code
black .

# Check code style
flake8
```

## Project Structure
```
project_root/
├── config/                 # Project settings
├── apps/                  
│   ├── accounts/          # User authentication
│   ├── listings/          # Listing management
│   ├── categories/        # Category management
│   ├── orders/            # Order & payment
│   ├── reviews/           # Review system
│   └── profiles/          # User profiles
├── static/
│   ├── css/              # Compiled CSS
│   ├── js/               # JavaScript files
│   └── images/           # Static images
├── media/                 # User uploaded files
├── templates/             # HTML templates
└── tests/                # Test files
```

## Git Setup

### Branch Strategy
- `main` - Production code
- `develop` - Development code
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Production fixes

### Commit Message Format
```
type(scope): subject

body

footer
```
Types: feat, fix, docs, style, refactor, test, chore

## Additional Setup

### VS Code Extensions
- Python
- Django
- Tailwind CSS IntelliSense
- SQLite Viewer
- Git Lens

### Browser Extensions
- Django Debug Toolbar
- React Developer Tools (if using React)

## Troubleshooting

### Common Issues
1. Database migrations conflicts
   - Solution: Remove migrations and recreate

2. Static files not loading
   - Check STATIC_URL and STATICFILES_DIRS settings
   - Run collectstatic

3. Environment variables not loading
   - Check .env file location
   - Verify python-dotenv setup

### Support Resources
- Django Documentation
- Project Wiki
- Team Communication Channel 

## Docker Setup
```bash
# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Static Files
```
static/
├── css/
│   └── custom.css       # Custom styles only
├── js/
│   ├── components/      # JavaScript modules
│   └── utils/          # Utility functions
```