# Application Routes

## Authentication Routes
- `/login/` - User login
- `/register/` - User registration
- `/logout/` - User logout
- `/password-reset/` - Password reset request
- `/password-reset/confirm/<token>/` - Password reset confirmation

## Profile Routes
- `/profile/` - View own profile
- `/profile/edit/` - Edit profile
- `/profile/change-password/` - Change password

## Listing Routes
- `/` - Home page (all listings)
- `/listings/` - All listings (with filters)
- `/listings/create/` - Create new listing
- `/listings/<id>/` - View specific listing
- `/listings/<id>/edit/` - Edit listing
- `/listings/<id>/delete/` - Delete listing
- `/listings/my-listings/` - View own listings
- `/listings/category/<category_id>/` - View listings by category
- `/listings/search/` - Search listings

## Purchase Routes
- `/purchases/` - View all purchases
- `/purchases/<id>/` - View specific purchase
- `/purchases/<id>/receipt/` - Download purchase receipt
- `/purchases/<id>/tracking/` - View shipping tracking

## Review Routes
- `/listings/<id>/reviews/` - View all reviews for a listing
- `/listings/<id>/reviews/create/` - Create review
- `/listings/<id>/reviews/<review_id>/edit/` - Edit review
- `/listings/<id>/reviews/<review_id>/delete/` - Delete review

## Category Routes
- `/categories/` - View all categories
- `/categories/<id>/` - View specific category
- `/categories/<id>/subcategories/` - View subcategories
- `/categories/<id>/items/` - View category items

## Order Routes
- `/listings/<id>/buy/` - Initiate purchase
- `/orders/<id>/` - View order details
- `/orders/<id>/payment/` - Process payment
- `/orders/<id>/confirmation/` - Order confirmation

## API Routes (for AJAX calls)
- `/api/listings/filter/` - Filter listings
- `/api/listings/sort/` - Sort listings
- `/api/listings/<id>/like/` - Like/unlike listing
- `/api/categories/` - Get categories
- `/api/search/` - Search functionality

## Message Routes
- `/messages/` - View all messages
- `/messages/<order_id>/` - View messages for specific order
- `/messages/<order_id>/send/` - Send message

## Webhook Routes
- `/webhooks/stripe/` - Stripe payment webhooks 

## Testing Requirements

### Unit Tests
1. User Registration
   - Test successful registration with valid data
   - Test registration with existing email
   - Test registration with invalid password format
   - Test registration with missing required fields
   - Test email verification process
   - Test password hashing

2. User Login
   - Test successful login
   - Test login with incorrect password
   - Test login with non-existent user
   - Test login with unverified email
   - Test remember me functionality
   - Test session creation

3. Password Reset
   - Test password reset request
   - Test reset token validation
   - Test password update
   - Test expired token handling

4. Form Validation
   - Test all form field validations
   - Test custom validation rules
   - Test error message formatting

### Integration Tests
1. Authentication Flow
   - Test complete registration -> email verification -> login flow
   - Test password reset flow
   - Test session management
   - Test logout flow

2. Security
   - Test CSRF protection
   - Test rate limiting
   - Test password encryption
   - Test session security

### E2E Tests
1. User Flows
   - Complete registration process
   - Login process
   - Password reset process
   - Profile update process