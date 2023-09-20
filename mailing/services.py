from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from mailing.models import Mailing, Log


def change_status_to_started():
    datetime_now = timezone.now()
    mailing_list_created = Mailing.objects.filter(status='created')

    for mailing in mailing_list_created:
        if mailing.start_time < datetime_now:
            mailing.status = 'started'
            mailing.save()


def send_mailing(mailing, client):
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

            
def send_mails_regular():
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
                            if (datetime_now - last_try_date).days >= 0:
                                send_mailing(mailing=mailing, client=client)
                        case 'weekly':
                            if (datetime_now - last_try_date).days >= 7:
                                send_mailing(mailing=mailing, client=client)
                        case 'monthly':
                            if (datetime_now - last_try_date).days >= 30:
                                send_mailing(mailing=mailing, client=client)
                else:
                    send_mailing(mailing=mailing, client=client)

