from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from mailing import constants
from mailing.models import Mailing, Log


def change_status_to_started():
    datetime_now = timezone.now()
    mailing_list_created = Mailing.objects.filter(status=Mailing.STATUSES[0][0])

    for mailing in mailing_list_created:
        if mailing.start_time < datetime_now:
            mailing.status = Mailing.STATUSES[1][0]
            mailing.save()


def send_mailing(mailing, client):
    message = mailing.message

    try:
        result = send_mail(
            subject=message.subject,
            message=message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email]
        )
        if result:
            status = Log.STATUSES[0][0]
        else:
            status = Log.STATUSES[1][0]

    except Exception:
        status = Log.STATUSES[1][0]

    Log.objects.create(
        last_try=timezone.now(),
        status=status,
        client=client,
        mailing=mailing
    )

            
def send_mails_regular():
    datetime_now = timezone.now()
    mailing_list_started = Mailing.objects.filter(status=Mailing.STATUSES[1][0])

    for mailing in mailing_list_started:
        if mailing.end_time < datetime_now:
            mailing.status = Mailing.STATUSES[2][0]
        elif (mailing.start_time < datetime_now) and (mailing.end_time > datetime_now):
            for client in mailing.recipients.all():
                mailing_log = Log.objects.filter(
                    mailing=mailing,
                    client=client
                )
                if mailing_log.exists():
                    last_try_date = mailing_log.order_by('-last_try').first().last_try
                    timedelta = (datetime_now - last_try_date).days
                    frequency = constants.SCHEDULE.get(mailing.frequency)

                    if timedelta >= frequency:
                        send_mailing(mailing=mailing, client=client)

                else:
                    send_mailing(mailing=mailing, client=client)

