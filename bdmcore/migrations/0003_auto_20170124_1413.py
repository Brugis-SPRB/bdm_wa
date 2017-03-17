# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bdmcore', '0002_auto_20160916_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=30)),
                ('action', models.CharField(max_length=20)),
                ('initialstate', models.CharField(max_length=20)),
                ('context', models.CharField(max_length=20)),
                ('result', models.CharField(max_length=10)),
                ('info', models.CharField(max_length=200)),
                ('client', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'events',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='globalparams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('value', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'globalparams',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserTableStates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=50)),
                ('schema', models.CharField(max_length=30)),
                ('uname', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'user_tablestates',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('userrole', models.CharField(max_length=50)),
                ('userpswd', models.CharField(max_length=30)),
                ('slock', models.IntegerField()),
                ('usermail', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AlterModelOptions(
            name='tablestates',
            options={'managed': False},
        ),
    ]