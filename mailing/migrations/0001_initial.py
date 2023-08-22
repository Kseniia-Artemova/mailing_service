# Generated by Django 4.2.4 on 2023-08-22 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=60, verbose_name='e-mail')),
                ('name', models.CharField(max_length=150, verbose_name='ФИО')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timedate', models.DateTimeField(verbose_name='Дата и время последней рассылки')),
                ('status', models.CharField(max_length=50, verbose_name='Статус попытки')),
                ('server_response', models.CharField(blank=True, max_length=3, null=True, verbose_name='Ответ сервера')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='No subject', max_length=100, verbose_name='Тема')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Тело письма')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timedate', models.DateTimeField(verbose_name='Дата и время рассылки')),
                ('frequency', models.CharField(max_length=50, verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('создана', 'Создана'), ('запущена', 'Запущена'), ('завершена', 'Завершена')], default='создана', max_length=10, verbose_name='Статус')),
                ('logs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.log', verbose_name='Логи')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.message', verbose_name='Сообщение')),
                ('recipients', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.client', verbose_name='Получатели')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
    ]
