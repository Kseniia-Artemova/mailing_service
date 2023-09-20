from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone

from config import settings
from mailing.models import Log, Mailing


class Command(BaseCommand):

    def _send_mailing(self, mailing, client):
        message = mailing.message

        try:
            send_mail(
                subject=message.subject,
                message=message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email]
            )
            status = 'successful'
            print('успешно отправили')

        except Exception as error:
            print(error)
            print('error')
            status = 'error'

        Log.objects.create(
            last_try=timezone.now(),
            status=status,
            client=client,
            mailing=mailing
        )

    def handle(self, *args, **options):

        datetime_now = timezone.now()
        mailing_list_started = Mailing.objects.filter(status='started')

        for mailing in mailing_list_started:
            if mailing.end_time < datetime_now:
                mailing.status = 'finished'
            elif (mailing.start_time < datetime_now) and (mailing.end_time > datetime_now):
                for client in mailing.recipients.all():
                    mailing_log = Log.objects.filter(
                        mailing=mailing,
                        client=client
                    )
                    if mailing_log.exists():
                        last_try_date = mailing_log.order_by('-last_try').first().last_try

                        match mailing.frequency:
                            case 'daily':
                                if (datetime_now - last_try_date).days >= 1:
                                    self._send_mailing(mailing=mailing, client=client)
                            case 'weekly':
                                if (datetime_now - last_try_date).days >= 7:
                                    self._send_mailing(mailing=mailing, client=client)
                            case 'monthly':
                                if (datetime_now - last_try_date).month >= 1:
                                    self._send_mailing(mailing=mailing, client=client)
                    else:
                        self._send_mailing(mailing=mailing, client=client)