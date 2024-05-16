# Generated by Django 4.1.13 on 2024-05-15 23:23

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('identificacion', models.CharField(max_length=15, unique=True)),
                ('nombre_usuario', models.CharField(max_length=60)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AuthenticationCodes',
            fields=[
                ('codigo_url', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=6)),
                ('empleado_id', models.CharField(max_length=15)),
            ],
        ),
    ]
