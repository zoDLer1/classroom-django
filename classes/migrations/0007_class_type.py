# Generated by Django 4.0.3 on 2022-04-22 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_rename_type_classtype_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='classes.classtype'),
            preserve_default=False,
        ),
    ]
