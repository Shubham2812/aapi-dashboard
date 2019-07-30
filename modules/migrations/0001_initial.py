# Generated by Django 2.2.3 on 2019-07-25 10:51

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=400)),
                ('attr_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('data_repo', models.CharField(default='', max_length=200)),
                ('java_class', models.CharField(default='', max_length=400)),
                ('cti', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None), size=None)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modules.Module')),
            ],
        ),
    ]