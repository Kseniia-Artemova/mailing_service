from django.core.management import BaseCommand
from django.utils import timezone
from mailing.models import Mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        datetime_now = timezone.now()
        mailing_list_created = Mailing.objects.filter(status='created')

        for mailing in mailing_list_created:
            if mailing.start_time < datetime_now:
                mailing.status = 'started'
                mailing.save()
                print('сменили статус')
