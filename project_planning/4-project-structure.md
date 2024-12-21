# Project Structure

## Root Directory Structure
```
marketplace/                  # Project root
├── config/                  # Project configuration
├── apps/                    # Django applications
├── static/                  # Static files
├── media/                   # User uploaded files
├── templates/               # HTML templates
├── tests/                   # Test files
├── requirements/            # Requirements files
├── docs/                    # Documentation
└── scripts/                 # Utility scripts
```

## Detailed Structure

### Configuration
```
config/
├── __init__.py
├── settings/
│   ├── __init__.py
│   ├── base.py             # Base settings
│   ├── local.py            # Development settings
│   ├── production.py       # Production settings
│   └── test.py             # Test settings
├── urls.py                 # Main URL configuration
├── wsgi.py                 # WSGI configuration
└── asgi.py                 # ASGI configuration
```

### Applications
```
apps/
├── accounts/               # User authentication
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── listings/              # Product listings
│   ├── migrations/
│   ├── templates/
│   │   └── listings/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── categories/           # Category management
│   ├── migrations/
│   ├── fixtures/
│   │   └── initial_categories.json
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   └── views.py
│
├── orders/              # Order management
│   ├── migrations/
│   ├── templates/
│   │   └── orders/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── reviews/            # Review system
│   ├── migrations/
│   ├── templates/
│   │   └── reviews/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   └── views.py
│
└── profiles/          # User profiles
    ├── migrations/
    ├── templates/
    │   └── profiles/
    ├── __init__.py
    ├── admin.py
    ├── models.py
    └── views.py
```

### Templates
```
templates/
├── base.html                # Base template
├── partials/               # Reusable components
│   ├── header.html
│   ├── footer.html
│   ├── messages.html
│   └── pagination.html
├── components/            # Tailwind components
│   ├── buttons.html
│   ├── cards.html
│   └── forms.html
└── layouts/              # Page layouts
    ├── main.html
    └── sidebar.html
```

### Static Files
```
static/
├── css/
│   ├── src/
│   │   └── input.css    # Tailwind source
│   └── dist/
│       └── output.css   # Compiled CSS
├── js/
│   ├── components/      # JavaScript modules
│   └── utils/           # Utility functions
├── images/
│   ├── logos/
│   └── icons/
└── vendors/            # Third-party assets
```

### Tests
```
tests/
├── conftest.py         # Pytest configuration
├── factories/          # Test factories
├── integration/        # Integration tests
└── unit/              # Unit tests
    ├── test_listings/
    ├── test_orders/
    └── test_users/
```

### Requirements
```
requirements/
├── base.txt           # Base requirements
├── local.txt         # Development requirements
├── production.txt    # Production requirements
└── test.txt         # Test requirements
```

## Key Files

### Django App Structure
Each Django app should follow this structure:
```python
app_name/
├── __init__.py
├── admin.py          # Admin interface
├── apps.py           # App configuration
├── forms.py          # Forms
├── models.py         # Database models
├── serializers.py    # API serializers (if needed)
├── services.py       # Business logic
├── urls.py           # URL patterns
└── views.py          # View logic
```

### Configuration Files
```
marketplace/
├── .env              # Environment variables
├── .gitignore       # Git ignore rules
├── pytest.ini       # Pytest configuration
├── setup.cfg        # Development tool configs
└── manage.py        # Django management script
```

## Naming Conventions

### Files and Directories
- Use lowercase with underscores for Python files
- Use lowercase with hyphens for templates
- Use PascalCase for class-based components

### URL Patterns
- Use lowercase with hyphens
- Be descriptive and RESTful
- Include version in API endpoints

Example:
```python
# urls.py
urlpatterns = [
    path('listings/', views.ListingList.as_view(), name='listing-list'),
    path('listings/<int:pk>/', views.ListingDetail.as_view(), name='listing-detail'),
    path('api/v1/listings/', api_views.ListingAPIView.as_view(), name='api-listing-list'),
]
```

## Development Guidelines

### Application Organization
- Keep apps focused and modular
- Use services.py for complex business logic
- Keep views thin, models fat
- Use mixins for shared functionality

### Template Organization
- Use template inheritance
- Create reusable components
- Keep logic out of templates
- Use template tags for complex logic

### Static Files
- Use proper asset versioning
- Optimize images
- Minify production assets
- Use CDN in production

### Testing
- Organize tests by type and functionality
- Use fixtures and factories
- Follow AAA pattern (Arrange, Act, Assert)
- Test business logic thoroughly 