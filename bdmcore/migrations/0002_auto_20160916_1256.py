# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-16 10:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bdmcore', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='tablestates',
            table='tables_states',
        ),
        migrations.AlterModelTable(
            name='userrights',
            table='user_rights',
        ),
    ]
