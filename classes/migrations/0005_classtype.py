# Generated by Django 4.0.3 on 2022-04-22 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_alter_invitelink_current_class'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]