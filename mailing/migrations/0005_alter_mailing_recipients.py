# Generated by Django 4.2.4 on 2023-08-25 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_remove_mailing_recipients_mailing_recipients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='recipients',
            field=models.ManyToManyField(blank=True, to='mailing.client', verbose_name='Получатели'),
        ),
    ]
