from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Generate password hashes for fixtures'

    def handle(self, *args, **kwargs):
        admin_hash = make_password('admin123!')
        test_hash = make_password('test123!')
        
        self.stdout.write(self.style.SUCCESS(f'Admin password hash:'))
        self.stdout.write(admin_hash)
        self.stdout.write('\n')
        self.stdout.write(self.style.SUCCESS(f'Test user password hash:'))
        self.stdout.write(test_hash) 