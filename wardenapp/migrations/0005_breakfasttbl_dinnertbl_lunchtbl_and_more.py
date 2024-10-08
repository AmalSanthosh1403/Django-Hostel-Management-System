# Generated by Django 5.0.6 on 2024-09-01 12:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentapp', '0003_rename_roomid_studentstbl_roomobj'),
        ('wardenapp', '0004_roomtbl_created_at_roomtbl_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Breakfasttbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dishname', models.CharField(max_length=255)),
                ('dishprice', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Dinnertbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dishname', models.CharField(max_length=255)),
                ('dishprice', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Lunchtbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dishname', models.CharField(max_length=255)),
                ('dishprice', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='roomtbl',
            old_name='hostel',
            new_name='hostelOBJ',
        ),
        migrations.RemoveField(
            model_name='roomtbl',
            name='wardenID',
        ),
        migrations.AddField(
            model_name='roomtbl',
            name='wardenOBJ',
            field=models.ManyToManyField(to='wardenapp.wardentbl'),
        ),
        migrations.AlterField(
            model_name='roomtbl',
            name='room_status',
            field=models.CharField(choices=[('Fully Occupied', 'Fully Occupied'), ('Partially Occupied', 'Partially Occupied'), ('Vacant', 'Vacant')], default='Vacant', max_length=100),
        ),
        migrations.AlterField(
            model_name='roomtbl',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Mealplantbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True, unique=True)),
                ('breakfastOBJS', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='breakfastobjs', to='wardenapp.breakfasttbl')),
                ('dinnerOBJS', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dinnerobjs', to='wardenapp.dinnertbl')),
                ('lunchOBJS', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lunchobjs', to='wardenapp.lunchtbl')),
            ],
        ),
        migrations.CreateModel(
            name='Selectedmealtbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breakfastOBJ', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='breakfastobj', to='wardenapp.breakfasttbl')),
                ('dinnerOBJ', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dinnerobj', to='wardenapp.dinnertbl')),
                ('lunchOBJ', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lunchobj', to='wardenapp.lunchtbl')),
                ('plannedmealOBJ', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='plannedmealobj', to='wardenapp.mealplantbl')),
                ('studentOBJ', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='selectedstudent', to='studentapp.studentstbl')),
            ],
        ),
    ]
