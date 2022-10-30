# Generated by Django 4.1.2 on 2022-10-30 09:49

from django.db import migrations, models
import django.db.models.deletion
import systems.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('industry', '0001_initial'),
        ('location', '0001_initial'),
        ('technology', '0001_initial'),
        ('business', '0003_business_config_business_provider_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='secrets',
            field=systems.models.fields.EncryptedDataField(default={}, editable=False),
        ),
        migrations.AlterField(
            model_name='business',
            name='config',
            field=systems.models.fields.DictionaryField(default=dict),
        ),
        migrations.AlterField(
            model_name='business',
            name='industries',
            field=models.ManyToManyField(related_name='%(data_name)s', to='industry.industry'),
        ),
        migrations.AlterField(
            model_name='business',
            name='location',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(data_name)s', to='location.location'),
        ),
        migrations.AlterField(
            model_name='business',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='business',
            name='provider_type',
            field=models.CharField(default='base', max_length=128),
        ),
        migrations.AlterField(
            model_name='business',
            name='technologies',
            field=models.ManyToManyField(related_name='%(data_name)s', to='technology.technology'),
        ),
        migrations.AlterField(
            model_name='business',
            name='variables',
            field=systems.models.fields.DictionaryField(default=dict, editable=False),
        ),
    ]
