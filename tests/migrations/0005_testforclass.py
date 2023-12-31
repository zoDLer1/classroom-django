# Generated by Django 4.0.3 on 2022-04-17 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
        ('tests', '0004_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestForClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('current_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.class')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.test')),
            ],
        ),
    ]
