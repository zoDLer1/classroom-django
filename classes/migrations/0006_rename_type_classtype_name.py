# Generated by Django 4.0.3 on 2022-04-22 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0005_classtype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classtype',
            old_name='type',
            new_name='name',
        ),
    ]