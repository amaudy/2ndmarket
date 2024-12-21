import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from apps.listings.models import ProductListing, ListingImage
from apps.categories.models import MainCategory, SubCategory

@pytest.mark.django_db
class TestCreateListing:
    def setup_method(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test category
        self.main_category = MainCategory.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.sub_category = SubCategory.objects.create(
            main_category=self.main_category,
            name='Test Subcategory',
            slug='test-subcategory'
        )
        
        # Create test image
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Add some test image content
            content_type='image/jpeg'
        )

    def test_create_listing_view_requires_login(self, client):
        url = reverse('listings:create')
        response = client.get(url)
        assert response.status_code == 302
        assert '/accounts/login/' in response.url

    def test_create_listing_view_logged_in(self, client):
        client.login(username='testuser', password='testpass123')
        url = reverse('listings:create')
        response = client.get(url)
        assert response.status_code == 200
        assert 'Create New Listing' in str(response.content)

    def test_create_listing_successful(self, client):
        client.login(username='testuser', password='testpass123')
        url = reverse('listings:create')
        
        data = {
            'title': 'Test Listing',
            'description': 'Test Description',
            'price': '99.99',
            'condition': 'new',
            'category': self.sub_category.id,
            'image_0': self.image
        }
        
        response = client.post(url, data, follow=True)
        assert response.status_code == 200
        assert ProductListing.objects.count() == 1
        listing = ProductListing.objects.first()
        assert listing.title == 'Test Listing'
        assert listing.seller == self.user
        assert listing.status == 'active'

    def test_create_listing_with_multiple_images(self, client):
        client.login(username='testuser', password='testpass123')
        url = reverse('listings:create')
        
        # Create multiple test images
        images = {
            'image_0': SimpleUploadedFile('test1.jpg', b'', content_type='image/jpeg'),
            'image_1': SimpleUploadedFile('test2.jpg', b'', content_type='image/jpeg'),
            'image_2': SimpleUploadedFile('test3.jpg', b'', content_type='image/jpeg'),
        }
        
        data = {
            'title': 'Test Listing',
            'description': 'Test Description',
            'price': '99.99',
            'condition': 'new',
            'category': self.sub_category.id,
            **images
        }
        
        response = client.post(url, data, follow=True)
        assert response.status_code == 200
        assert ProductListing.objects.count() == 1
        listing = ProductListing.objects.first()
        assert listing.images.count() == 3
        assert listing.images.filter(is_primary=True).count() == 1

    def test_create_listing_validation(self, client):
        client.login(username='testuser', password='testpass123')
        url = reverse('listings:create')
        
        # Test with missing required fields
        data = {
            'title': '',  # Required field missing
            'price': 'invalid',  # Invalid price
            'condition': 'invalid',  # Invalid choice
        }
        
        response = client.post(url, data)
        assert response.status_code == 200  # Returns form with errors
        assert ProductListing.objects.count() == 0
        assert 'This field is required' in str(response.content)

    def test_create_listing_price_validation(self, client):
        client.login(username='testuser', password='testpass123')
        url = reverse('listings:create')
        
        data = {
            'title': 'Test Listing',
            'description': 'Test Description',
            'price': '-10.00',  # Negative price
            'condition': 'new',
            'category': self.sub_category.id,
        }
        
        response = client.post(url, data)
        assert response.status_code == 200
        assert ProductListing.objects.count() == 0
        form = response.context['form']
        assert 'Ensure this value is greater than or equal to 0' in form.errors['price']

    def test_my_listings_view(self, client):
        client.login(username='testuser', password='testpass123')
        
        # Create some test listings
        listing1 = ProductListing.objects.create(
            title='Listing 1',
            description='Description 1',
            price='99.99',
            condition='new',
            category=self.sub_category,
            seller=self.user,
            status='active'
        )
        
        listing2 = ProductListing.objects.create(
            title='Listing 2',
            description='Description 2',
            price='199.99',
            condition='used',
            category=self.sub_category,
            seller=self.user,
            status='active'
        )
        
        url = reverse('listings:my-listings')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'Listing 1' in str(response.content)
        assert 'Listing 2' in str(response.content)
        assert '99.99' in str(response.content)
        assert '199.99' in str(response.content) 