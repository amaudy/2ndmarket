# Fixtures Setup

## Overview
Fixtures are needed for:
- Initial development
- Testing
- Demo data
- Consistent development environment

## Fixture Files Location
```
apps/
├── categories/
│   └── fixtures/
│       └── categories.json     # Category hierarchy
├── listings/
│   └── fixtures/
│       ├── products.json       # Sample listings
│       └── images.json         # Sample images
├── accounts/
│   └── fixtures/
│       └── users.json          # Test users
└── reviews/
    └── fixtures/
        └── reviews.json        # Sample reviews
```

## Required Fixtures

### 1. Users (`users.json`)
```json
[
    {
        "model": "auth.user",
        "pk": 1,
        "fields": {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "hashed_password",
            "first_name": "John",
            "last_name": "Doe",
            "is_active": true,
            "date_joined": "2024-01-01T00:00:00Z"
        }
    }
]
```

### 2. User Profiles (`profiles.json`)
```json
[
    {
        "model": "profiles.userprofile",
        "pk": 1,
        "fields": {
            "user": 1,
            "phone_number": "+1234567890",
            "address": "123 Test St",
            "created_at": "2024-01-01T00:00:00Z"
        }
    }
]
```

### 3. Categories
Already defined in `fixtures_categories.json`

### 4. Products
Already defined in `fixtures_products.json`

### 5. Reviews (`reviews.json`)
```json
[
    {
        "model": "reviews.review",
        "pk": 1,
        "fields": {
            "user": 1,
            "listing": 1,
            "rating": 5,
            "content": "Great product, fast delivery!",
            "created_at": "2024-01-02T00:00:00Z"
        }
    }
]
```

## Loading Order
Fixtures must be loaded in the correct order to maintain data integrity:

1. Users
2. Profiles
3. Categories
4. Products
5. Reviews

## Loading Command
```bash
# Load all fixtures
python manage.py loaddata users profiles categories products reviews

# Load specific fixture
python manage.py loaddata categories
```

## Development Guidelines

### Creating Fixtures
- Export from existing data:
```bash
python manage.py dumpdata app_name.model_name --indent 2 > app_name/fixtures/file_name.json
```

### Fixture Data Guidelines
1. Keep data realistic but minimal
2. Include all required fields
3. Maintain referential integrity
4. Use consistent timestamps
5. Include variety of scenarios

### Testing with Fixtures
- Use in test classes:
```python
@pytest.mark.django_db
class TestListings:
    fixtures = ['users.json', 'categories.json', 'products.json']
```

### Fixture Maintenance
- Keep fixtures up to date with model changes
- Version control fixtures
- Document any special relationships
- Regular validation of fixture data

## Security Notes
- Never include real user data
- Use dummy emails (example.com domain)
- Hash any passwords
- Remove sensitive information 