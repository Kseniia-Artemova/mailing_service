from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Managers')
        if created:
            print('Группа "Managers" была успешно создана')
        else:
            print('Группа "Managers" уже существует')
