# Generated by Django 4.1.2 on 2022-10-31 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('id', models.CharField(editable=False, max_length=64, primary_key=True, serialize=False)),
                ('city', models.CharField(default=None, max_length=256, null=True)),
                ('state', models.CharField(default=None, max_length=256, null=True)),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
                'db_table': 'built_in_location',
                'ordering': ['id'],
                'abstract': False,
                'unique_together': {('city', 'state')},
            },
        ),
    ]
