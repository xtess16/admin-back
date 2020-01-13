from django.core.management import BaseCommand

from apps.users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            admin = User.objects.create_superuser(email="admin@mail.ru", password='1234')
            admin.is_active = True
            admin.is_staff = True
            admin.save()
            self.stdout.write('Created superuser')
        else:
            self.stdout.write('Superuser was already created!')