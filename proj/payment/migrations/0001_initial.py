# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-23 14:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_name', models.CharField(max_length=35)),
                ('status_bit', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DebCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardno', models.IntegerField()),
                ('cvv', models.IntegerField()),
                ('pin', models.IntegerField(null=True)),
                ('exp', models.DateField()),
                ('name', models.CharField(max_length=35)),
                ('pay_service', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='NetBankAcc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=25)),
                ('psswd', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='txn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.DecimalField(decimal_places=3, max_digits=15)),
                ('cardno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.DebCard')),
                ('cur_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Customer')),
            ],
        ),
    ]
