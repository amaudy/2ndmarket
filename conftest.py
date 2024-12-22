import pytest
from django.core.management import call_command

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # Load any initial data you need (fixtures)
        call_command('loaddata', 'apps/categories/fixtures/categories.json')

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Make the database available to all tests without explicitly marking them.
    """
    pass

@pytest.fixture
def client_with_user(client, django_user_model):
    """
    Returns an authenticated client with a test user.
    """
    user = django_user_model.objects.create_user(username='testuser', password='testpass123')
    client.login(username='testuser', password='testpass123')
    return client, user 