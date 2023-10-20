from django.core.management import BaseCommand
from auth_app.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='maria36127@gmail.com',
            surname='Admin',
            name='Maria',
            phone=89999999999,
            is_staff=True,
            is_superuser=True
        )

        user.set_password('12345')
        user.save()
