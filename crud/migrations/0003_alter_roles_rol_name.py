# Generated by Django 4.2.6 on 2023-10-23 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_alter_users_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roles',
            name='rol_name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
