# Generated by Django 2.0.1 on 2018-01-17 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='createtime',
            field=models.DateField(auto_now=True),
        ),
    ]