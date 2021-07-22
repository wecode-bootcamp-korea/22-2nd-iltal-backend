# Generated by Django 3.2.5 on 2021-07-22 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kakao_id', models.BigIntegerField(null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('profile_url', models.CharField(max_length=2000, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nickname', models.CharField(max_length=200)),
                ('profile_url', models.CharField(max_length=2000)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', unique=True)),
            ],
            options={
                'db_table': 'hosts',
            },
        ),
    ]
