# Generated by Django 3.1.1 on 2021-03-22 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Positions', '0003_auto_20210307_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='persons',
            name='office_position',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='persons',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]