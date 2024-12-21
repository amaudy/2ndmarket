from django.contrib.auth.hashers import make_password

password = make_password('admin123!')
print(f"Admin password hash: {password}")

password = make_password('test123!')
print(f"Test user password hash: {password}") 