# Generated by Django 4.1.2 on 2022-10-31 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='industry',
            options={'ordering': ['id'], 'verbose_name': 'industry', 'verbose_name_plural': 'industries'},
        ),
    ]
