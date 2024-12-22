import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from apps.listings.models import ProductListing, ListingImage, Order
from apps.categories.models import MainCategory, SubCategory
from django.utils.http import urlencode
from decimal import Decimal

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
            'status': 'active',
            'is_available': True,
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
            'status': 'active',
            'is_available': True
        }
        
        response = client.post(url, data)
        assert response.status_code == 200
        assert ProductListing.objects.count() == 0
        form = response.context['form']
        assert 'Price cannot be negative' in form.errors['price']

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

@pytest.mark.django_db
class TestOrders:
    @pytest.fixture(autouse=True)
    def setup_users(self):
        # Create seller
        self.seller = User.objects.create_user(
            username='seller',
            password='testpass123',
            email='seller@example.com'
        )
        
        # Create buyer
        self.buyer = User.objects.create_user(
            username='buyer',
            password='testpass123',
            email='buyer@example.com'
        )
        return self.buyer, self.seller

    @pytest.fixture(autouse=True)
    def setup_listing(self, setup_users):
        # Create main category and subcategory
        main_category = MainCategory.objects.create(name='Electronics')
        self.category = SubCategory.objects.create(
            name='Phones',
            main_category=main_category
        )
        
        # Create listing
        self.listing = ProductListing.objects.create(
            title='iPhone 14',
            description='Great condition',
            price=Decimal('999.99'),
            condition='like_new',
            category=self.category,
            seller=self.seller,
            status='active',
            is_available=True
        )
        return self.listing

    def test_create_order_success(self, client, setup_listing):
        # Login as buyer
        client.login(username='buyer', password='testpass123')
        
        # Prepare order data
        data = {
            'shipping_address': '123 Test St, Test City, 12345'
        }
        
        # Print debug info
        print("\nTest Debug:")
        print(f"Listing ID: {self.listing.pk}")
        print(f"Data: {data}")
        
        # Create order
        response = client.post(
            reverse('listings:buy', kwargs={'pk': self.listing.pk}),
            data=urlencode(data),
            content_type='application/x-www-form-urlencoded'
        )
        
        # Print response info
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        
        assert response.status_code == 200
        assert response.json()['status'] == 'success'
        
        # Check order was created
        order = Order.objects.first()
        assert order is not None
        assert order.buyer == self.buyer
        assert order.listing == self.listing
        assert order.amount == Decimal('999.99')
        assert order.status == 'paid'
        assert order.shipping_address == data['shipping_address']
        
        # Check listing was updated
        self.listing.refresh_from_db()
        assert self.listing.status == 'sold'
        assert not self.listing.is_available

    def test_cannot_buy_own_listing(self, client, setup_listing):
        # Login as seller
        client.login(username='seller', password='testpass123')
        
        data = {
            'shipping_address': '123 Test St, Test City, 12345'
        }
        
        response = client.post(
            reverse('listings:buy', kwargs={'pk': self.listing.pk}),
            data=data
        )
        
        assert response.status_code == 400
        assert 'Cannot buy your own listing' in response.json()['error']
        assert Order.objects.count() == 0

    def test_cannot_buy_unavailable_listing(self, client, setup_listing):
        # Login as buyer
        client.login(username='buyer', password='testpass123')
        
        # Make listing unavailable
        self.listing.is_available = False
        self.listing.save()
        
        data = {
            'shipping_address': '123 Test St, Test City, 12345'
        }
        
        response = client.post(
            reverse('listings:buy', kwargs={'pk': self.listing.pk}),
            data=data
        )
        
        assert response.status_code == 400
        assert 'Item not available' in response.json()['error']
        assert Order.objects.count() == 0

    def test_cannot_buy_without_login(self, client, setup_listing):
        data = {
            'shipping_address': '123 Test St, Test City, 12345'
        }
        
        response = client.post(
            reverse('listings:buy', kwargs={'pk': self.listing.pk}),
            data=data
        )
        
        assert response.status_code == 302  # Redirects to login
        assert Order.objects.count() == 0

    def test_cannot_buy_sold_listing(self, client, setup_listing):
        # Login as buyer
        client.login(username='buyer', password='testpass123')
        
        # Mark listing as sold
        self.listing.status = 'sold'
        self.listing.save()
        
        data = {
            'shipping_address': '123 Test St, Test City, 12345'
        }
        
        response = client.post(
            reverse('listings:buy', kwargs={'pk': self.listing.pk}),
            data=data
        )
        
        assert response.status_code == 400
        assert 'Item not available' in response.json()['error']
        assert Order.objects.count() == 0

    def test_shipping_address_required(self, client, setup_listing):
        # Login as buyer
        client.login(username='buyer', password='testpass123')
        
        # Try to create order without shipping address
        response = client.post(
            reverse('listings:buy', kwargs={'pk': self.listing.pk}),
            data={}
        )
        
        assert response.status_code == 400
        assert Order.objects.count() == 0

@pytest.mark.django_db
class TestPurchases:
    @pytest.fixture(autouse=True)
    def setup_users(self):
        self.buyer = User.objects.create_user(
            username='buyer',
            password='testpass123',
            email='buyer@example.com'
        )
        self.seller = User.objects.create_user(
            username='seller',
            password='testpass123',
            email='seller@example.com'
        )
        return self.buyer, self.seller

    @pytest.fixture
    def setup_orders(self, setup_users):
        # Create categories
        main_category = MainCategory.objects.create(name='Electronics')
        category = SubCategory.objects.create(
            name='Phones',
            main_category=main_category
        )
        
        # Create listings and orders
        listings_data = [
            {
                'title': 'iPhone 14',
                'price': Decimal('999.99'),
                'status': 'sold',
                'order_status': 'delivered'
            },
            {
                'title': 'Samsung S23',
                'price': Decimal('899.99'),
                'status': 'sold',
                'order_status': 'shipped'
            },
            {
                'title': 'Google Pixel 7',
                'price': Decimal('799.99'),
                'status': 'sold',
                'order_status': 'paid'
            }
        ]
        
        self.orders = []
        for data in listings_data:
            listing = ProductListing.objects.create(
                title=data['title'],
                description='Test description',
                price=data['price'],
                condition='like_new',
                category=category,
                seller=self.seller,
                status=data['status'],
                is_available=False
            )
            
            order = Order.objects.create(
                listing=listing,
                buyer=self.buyer,
                amount=data['price'],
                status=data['order_status'],
                shipping_address='123 Test St'
            )
            self.orders.append(order)
        
        return self.orders

    def test_view_purchases_requires_login(self, client):
        url = reverse('listings:my-purchases')
        response = client.get(url)
        assert response.status_code == 302
        assert '/accounts/login/' in response.url

    def test_view_purchases_success(self, client, setup_orders):
        client.login(username='buyer', password='testpass123')
        url = reverse('listings:my-purchases')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'My Purchases' in str(response.content)
        
        # Check all orders are displayed
        for order in self.orders:
            assert order.listing.title in str(response.content)
            assert str(order.amount) in str(response.content)
            assert order.get_status_display() in str(response.content)

    def test_view_purchases_empty(self, client, setup_users):
        client.login(username='buyer', password='testpass123')
        url = reverse('listings:my-purchases')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'No purchases yet' in str(response.content)

    def test_view_purchases_pagination(self, client, setup_orders):
        # Create additional orders to test pagination
        main_category = MainCategory.objects.get(name='Electronics')
        category = SubCategory.objects.get(name='Phones')
        
        # Create 12 more orders (total 15)
        for i in range(12):
            listing = ProductListing.objects.create(
                title=f'Test Listing {i}',
                description='Test description',
                price=Decimal('99.99'),
                condition='like_new',
                category=category,
                seller=self.seller,
                status='sold',
                is_available=False
            )
            
            Order.objects.create(
                listing=listing,
                buyer=self.buyer,
                amount=Decimal('99.99'),
                status='paid',
                shipping_address='123 Test St'
            )
        
        client.login(username='buyer', password='testpass123')
        
        # Test first page
        response = client.get(reverse('listings:my-purchases'))
        assert response.status_code == 200
        assert len(response.context['orders']) == 10  # Items per page
        
        # Test second page
        response = client.get(reverse('listings:my-purchases') + '?page=2')
        assert response.status_code == 200
        assert len(response.context['orders']) == 5  # Remaining items