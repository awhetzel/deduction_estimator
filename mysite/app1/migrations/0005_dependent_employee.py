# Generated by Django 2.1 on 2018-09-06 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_dependent'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependent',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.Employee'),
            preserve_default=False,
        ),
    ]