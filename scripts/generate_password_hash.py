from django.contrib.auth.hashers import make_password

# Generate hash for admin123!
admin_hash = make_password('admin123!')
print(f"Admin password hash: {admin_hash}")

# Generate hash for test123!
test_hash = make_password('test123!')
print(f"Test user password hash: {test_hash}") 