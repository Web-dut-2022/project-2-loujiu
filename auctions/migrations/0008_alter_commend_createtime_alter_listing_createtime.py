# Generated by Django 4.0.3 on 2022-04-23 14:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commend',
            name='createTime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created time'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='createTime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created time'),
        ),
    ]