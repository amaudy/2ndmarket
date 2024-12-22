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
            'image_0': self.image,
            'status': 'active',
            'is_available': True
        }
        
        print("\nTest Debug:")
        print(f"Data being sent: {data}")
        
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

    def test_delete_listing(self, client):
        client.login(username='testuser', password='testpass123')
        
        # Create a test listing
        listing = ProductListing.objects.create(
            title='Test Listing',
            description='Test Description',
            price='99.99',
            condition='new',
            category=self.sub_category,
            seller=self.user,
            status='active'
        )
        
        url = reverse('listings:delete', kwargs={'pk': listing.pk})
        response = client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        assert response.status_code == 302
        assert not ProductListing.objects.filter(pk=listing.pk).exists()

    def test_delete_listing_unauthorized(self, client):
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        client.login(username='otheruser', password='otherpass123')
        
        # Create a listing owned by the first user
        listing = ProductListing.objects.create(
            title='Test Listing',
            description='Test Description',
            price='99.99',
            condition='new',
            category=self.sub_category,
            seller=self.user,  # Original test user
            status='active'
        )
        
        url = reverse('listings:delete', kwargs={'pk': listing.pk})
        response = client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        assert response.status_code == 403
        assert ProductListing.objects.filter(pk=listing.pk).exists() 

    def test_listing_detail_view(self, client):
        # Create a test listing
        listing = ProductListing.objects.create(
            title='Test Listing',
            description='Test Description',
            price='99.99',
            condition='new',
            category=self.sub_category,
            seller=self.user,
            status='active'
        )
        
        url = reverse('listings:detail', kwargs={'pk': listing.pk})
        response = client.get(url)
        
        assert response.status_code == 200
        assert listing.title in str(response.content)
        assert listing.description in str(response.content)
        assert str(listing.price) in str(response.content)
        assert listing.get_condition_display() in str(response.content)
        assert listing.seller.username in str(response.content) 

    def test_edit_listing(self, client):
        client.login(username='testuser', password='testpass123')
        
        # Create a test listing
        listing = ProductListing.objects.create(
            title='Test Listing',
            description='Test Description',
            price='99.99',
            condition='new',
            category=self.sub_category,
            seller=self.user,
            status='active'
        )
        
        # Print initial state
        print("\nInitial listing state:")
        print(f"Title: {listing.title}")
        print(f"Description: {listing.description}")
        print(f"Price: {listing.price}")
        print(f"Condition: {listing.condition}")
        
        url = reverse('listings:edit', kwargs={'pk': listing.pk})
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'price': '199.99',
            'condition': 'used',
            'category': self.sub_category.id,
            'status': 'active',
            'seller': self.user.id,  # Include seller ID
            'is_available': True,    # Include availability
        }
        
        # Print the data we're sending
        print("\nData being sent:")
        print(data)
        
        response = client.post(url, data, follow=True)
        listing.refresh_from_db()
        
        # Print response details
        print("\nResponse details:")
        print(f"Status code: {response.status_code}")
        if hasattr(response.context, 'form'):
            print(f"Form errors: {response.context['form'].errors}")
        
        # Print final state
        print("\nFinal listing state:")
        print(f"Title: {listing.title}")
        print(f"Description: {listing.description}")
        print(f"Price: {listing.price}")
        print(f"Condition: {listing.condition}")
        
        # Assertions
        assert response.status_code == 200
        assert listing.title == data['title'], f"Title not updated. Expected: {data['title']}, Got: {listing.title}"
        assert listing.description == data['description']
        assert str(listing.price) == data['price']
        assert listing.condition == data['condition']
        assert listing.seller == self.user

    def test_edit_listing_unauthorized(self, client):
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        client.login(username='otheruser', password='otherpass123')
        
        # Create a listing owned by the first user
        listing = ProductListing.objects.create(
            title='Test Listing',
            description='Test Description',
            price='99.99',
            condition='new',
            category=self.sub_category,
            seller=self.user,  # Original test user
            status='active'
        )
        
        url = reverse('listings:edit', kwargs={'pk': listing.pk})
        response = client.get(url)
        
        assert response.status_code == 404  # Should not find listings owned by other users

    def test_delete_listing_image(self, client):
        client.login(username='testuser', password='testpass123')
        
        # Create a test listing with image
        listing = ProductListing.objects.create(
            title='Test Listing',
            description='Test Description',
            price='99.99',
            condition='new',
            category=self.sub_category,
            seller=self.user,
            status='active'
        )
        
        image = ListingImage.objects.create(
            listing=listing,
            image=self.image,
            display_order=0,
            is_primary=True
        )
        
        url = reverse('listings:delete_image', kwargs={'pk': image.pk})
        response = client.post(url)
        
        assert response.status_code == 200
        assert not ListingImage.objects.filter(pk=image.pk).exists()

    def test_delete_listing_image_unauthorized(self, client):
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        client.login(username='otheruser', password='otherpass123')
        
        # Create a listing with image owned by the first user
        listing = ProductListing.objects.create(
            title='Test Listing',
            description='Test Description',
            price='99.99',
            condition='new',
            category=self.sub_category,
            seller=self.user,  # Original test user
            status='active'
        )
        
        image = ListingImage.objects.create(
            listing=listing,
            image=self.image,
            display_order=0,
            is_primary=True
        )
        
        url = reverse('listings:delete_image', kwargs={'pk': image.pk})
        response = client.post(url)
        
        assert response.status_code == 403
        assert ListingImage.objects.filter(pk=image.pk).exists()