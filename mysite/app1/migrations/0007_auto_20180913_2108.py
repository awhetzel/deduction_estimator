# Generated by Django 2.1.1 on 2018-09-13 21:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_auto_20180911_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dependent',
            name='age',
        ),
        migrations.AddField(
            model_name='dependent',
            name='birth_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dependent',
            name='percent_co_pays',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='percent_co_pays',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together={('first_name', 'last_name')},
        ),
    ]