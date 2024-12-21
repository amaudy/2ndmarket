# Coding Standards

## Python Code Style

### General Python Guidelines
- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black default)
- Use snake_case for variables and functions
- Use PascalCase for classes
- Use UPPERCASE for constants

### Imports
```python
# Standard library imports
import json
from datetime import datetime

# Third-party imports
import stripe
from django.db import models
from django.conf import settings

# Local imports
from .models import UserProfile
from apps.listings.models import Product
```

### Django Models
```python
class ProductListing(models.Model):
    """
    Model representing a product listing in the marketplace.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product Listing'
        verbose_name_plural = 'Product Listings'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing-detail', kwargs={'pk': self.pk})
```

### Views
```python
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(LoginRequiredMixin, ListView):
    """
    Display all products in a paginated list.
    """
    model = ProductListing
    template_name = 'listings/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
```

## Templates

### Template Structure
```html
{% extends "base.html" %}
{% load static %}

{% block title %}Page Title{% endblock %}

{% block content %}
<div class="container mx-auto px-4">
    <h1 class="text-2xl font-bold mb-4">{{ page_title }}</h1>
    
    {% include "partials/product_card.html" with product=product %}
    
    {% if messages %}
        {% include "partials/messages.html" %}
    {% endif %}
</div>
{% endblock %}
```

### Tailwind CSS Guidelines
- Use utility classes provided by Tailwind
- Create components for reusable UI elements
- Follow mobile-first approach
- Use consistent spacing scale
- Maintain color scheme defined in tailwind.config.js

## Testing

### Test Structure
```python
import pytest
from django.test import Client
from django.urls import reverse

@pytest.mark.django_db
class TestProductListing:
    def test_create_listing(self, client: Client):
        """Test creating a new product listing."""
        url = reverse('listing-create')
        data = {
            'title': 'Test Product',
            'price': '99.99',
            'description': 'Test description'
        }
        response = client.post(url, data)
        assert response.status_code == 302
```

### Test Guidelines
- Write tests before implementing features (TDD)
- Use pytest fixtures for common setup
- Test both success and failure cases
- Mock external services (Stripe, email, etc.)
- Aim for 90%+ test coverage
- Use meaningful test names

## Documentation

### Docstrings
```python
def calculate_total_price(items, discount=None):
    """
    Calculate the total price of items with optional discount.

    Args:
        items (list): List of items with 'price' attribute
        discount (float, optional): Discount percentage. Defaults to None.

    Returns:
        float: Total price after discount

    Raises:
        ValueError: If discount is not between 0 and 100
    """
    pass
```

### Comments
- Use comments to explain "why", not "what"
- Keep comments up to date with code changes
- Use TODO comments for planned improvements

## Git Workflow

### Branch Naming
- feature/user-story-number/brief-description
- bugfix/issue-number/brief-description
- hotfix/brief-description

### Commit Messages
```
feat(listings): add image upload functionality

- Add multiple image upload support
- Implement image validation
- Add image preview functionality

Closes #123
```

### Pull Requests
- Use PR template
- Include tests
- Update documentation
- Link related issues
- Add screenshots for UI changes

## Security Guidelines

### General Security
- Never commit sensitive data
- Use environment variables for secrets
- Implement proper input validation
- Use Django's built-in security features

### Form Handling
```python
from django.core.exceptions import ValidationError

def clean_email(self):
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
        raise ValidationError('Email already exists')
    return email
```

## Performance Guidelines

### Database
- Use select_related() and prefetch_related()
- Create proper indexes
- Optimize queries
- Use pagination

### Caching
- Cache expensive queries
- Use template fragment caching
- Implement Redis for session storage

## Error Handling

### Exception Handling
```python
try:
    product.process_payment()
except stripe.error.CardError as e:
    logger.error(f"Payment failed: {str(e)}")
    raise PaymentError("Payment could not be processed")
except Exception as e:
    logger.exception("Unexpected error during payment")
    raise
```

## Code Review Checklist
- [ ] Follows coding standards
- [ ] Includes tests
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Proper error handling
- [ ] Performance considerations
- [ ] Mobile responsive (if UI)
- [ ] Accessibility requirements met 