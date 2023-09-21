from django.core.management import BaseCommand
from django.utils import timezone
from mailing.models import Mailing
from mailing import services


class Command(BaseCommand):

    def handle(self, *args, **options):
        services.change_status_to_started()
