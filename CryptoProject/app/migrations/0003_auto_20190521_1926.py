# Generated by Django 2.2 on 2019-05-22 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20190521_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paintingrequest',
            name='dateRequest',
            field=models.DateTimeField(),
        ),
    ]
