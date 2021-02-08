# Generated by Django 3.1.5 on 2021-02-08 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Change_types',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(null=True)),
                ('znak', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Levels',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Objects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(null=True)),
                ('adress', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(null=True)),
                ('level_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Positions.levels')),
            ],
        ),
        migrations.CreateModel(
            name='Xyz',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('X', models.TextField(null=True)),
                ('y', models.IntegerField(null=True)),
                ('z', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.PositiveBigIntegerField(null=True)),
                ('name', models.TextField(null=True)),
                ('quantity', models.FloatField(null=True)),
                ('ediz', models.TextField(null=True)),
                ('photo1', models.ImageField(null=True, upload_to='')),
                ('photo2', models.ImageField(null=True, upload_to='')),
                ('groups_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Positions.groups')),
                ('mol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Positions.persons')),
                ('xyz_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Positions.xyz')),
            ],
        ),
        migrations.CreateModel(
            name='Change_qantity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time_oper', models.DateTimeField(null=True)),
                ('quantity', models.FloatField(null=True)),
                ('change_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Positions.change_types')),
                ('object_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Positions.objects')),
                ('person_id_contr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contr', to='Positions.persons')),
                ('person_id_mol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mol', to='Positions.persons')),
                ('position_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Positions.positions')),
            ],
        ),
    ]
