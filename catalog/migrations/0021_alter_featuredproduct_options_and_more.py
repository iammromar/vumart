# Generated by Django 4.2.3 on 2023-10-10 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_product_short_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='featuredproduct',
            options={'verbose_name': 'Seçilmiş Məhsul', 'verbose_name_plural': 'Seçilmiş Məhsullar'},
        ),
        migrations.AlterModelOptions(
            name='newproduct',
            options={'verbose_name': 'Yeni Məhsul', 'verbose_name_plural': 'Yeni Məhsullar'},
        ),
    ]
