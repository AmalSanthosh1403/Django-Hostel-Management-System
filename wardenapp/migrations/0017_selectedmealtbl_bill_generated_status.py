# Generated by Django 5.0.6 on 2024-09-13 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardenapp', '0016_rename_bill_billtbl'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedmealtbl',
            name='bill_generated_status',
            field=models.BooleanField(default=False),
        ),
    ]
