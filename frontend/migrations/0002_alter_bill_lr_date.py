# Generated by Django 4.2.3 on 2023-07-24 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='lr_date',
            field=models.DateField(blank=True),
        ),
    ]
