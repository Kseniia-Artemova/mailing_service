from django.db import models

# Create your models here.


class Client(models.Model):
    email = models.EmailField(max_length=60, verbose_name='e-mail')
    name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return f"{self.name} {self.email}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(default='No subject', max_length=100, verbose_name='Тема')
    body = models.TextField(null=True, blank=True, verbose_name='Тело письма')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Log(models.Model):
    timedate = models.DateTimeField(verbose_name='Дата и время последней рассылки')
    status = models.CharField(max_length=50, verbose_name='Статус попытки')
    server_response = models.CharField(null=True, blank=True, max_length=3, verbose_name='Ответ сервера')

    def __str__(self):
        return f'{self.timedate}: {self.server_response}, {self.status}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('создана', 'Создана'),
        ('запущена', 'Запущена'),
        ('завершена', 'Завершена'),
    ]

    timedate = models.DateTimeField(verbose_name='Дата и время рассылки')
    frequency = models.CharField(max_length=50, verbose_name='Периодичность')
    status = models.CharField(default='создана', choices=STATUS_CHOICES, max_length=10, verbose_name='Статус')
    recipients = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Получатели')
    message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Сообщение')
    logs = models.ForeignKey(Log, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Логи')

    def __str__(self):
        return f'{self.timedate} - {self.message}: {self.status} ({self.frequency})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
