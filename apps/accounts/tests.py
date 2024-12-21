import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestAuthentication:
    def test_signup_view(self, client):
        response = client.get(reverse('account_signup'))
        assert response.status_code == 200

    def test_login_view(self, client):
        response = client.get(reverse('account_login'))
        assert response.status_code == 200

    def test_user_signup(self, client):
        data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = client.post(reverse('account_signup'), data)
        assert response.status_code == 302
        assert User.objects.filter(email='test@example.com').exists()

    def test_user_login(self, client):
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        data = {
            'login': 'test@example.com',
            'password': 'testpass123',
        }
        response = client.post(reverse('account_login'), data)
        assert response.status_code == 302 