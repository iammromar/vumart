# Generated by Django 4.2 on 2023-11-28 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_remove_customuser_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
