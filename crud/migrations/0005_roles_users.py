# Generated by Django 4.2.6 on 2023-11-13 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0004_alter_roles_rol_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles_Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_roles', to='crud.roles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_roles', to='crud.users')),
            ],
        ),
    ]
