# Generated by Django 4.2 on 2023-11-26 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_remove_customuser_conpany_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='company_name',
        ),
    ]
