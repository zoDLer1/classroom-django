# Generated by Django 4.0.3 on 2022-04-22 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_invitelink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitelink',
            name='current_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.class', unique=True),
        ),
    ]
