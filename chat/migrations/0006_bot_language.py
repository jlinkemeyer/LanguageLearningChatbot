# Generated by Django 4.1.3 on 2022-12-09 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_chatsession_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='language',
            field=models.CharField(default='spanish', max_length=10),
        ),
    ]
