# Generated by Django 5.0.6 on 2024-09-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wardenapp', '0012_selectedmealtbl_breakfastobj_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedmealtbl',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]