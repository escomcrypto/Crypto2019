# Generated by Django 2.2.1 on 2019-05-31 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paintingrequest',
            name='signatureP',
            field=models.TextField(),
        ),
    ]
