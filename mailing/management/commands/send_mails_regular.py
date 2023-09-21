from django.core.management import BaseCommand
from mailing import services


class Command(BaseCommand):

    def handle(self, *args, **options):
        services.send_mails_regular()
