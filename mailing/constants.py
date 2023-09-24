from mailing.models import Mailing

# Расписание рассылок
SCHEDULE = {
    Mailing.FREQUENCY[0][0]: 1,
    Mailing.FREQUENCY[1][0]: 7,
    Mailing.FREQUENCY[2][0]: 30
}
