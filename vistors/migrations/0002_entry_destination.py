# Generated by Django 3.1.6 on 2021-02-08 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vistors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='destination',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
