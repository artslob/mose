# Generated by Django 2.2.6 on 2019-11-24 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wizuber', '0003_auto_20191124_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spiritartifact',
            name='spirit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spirit_artifacts', to='wizuber.Spirit'),
        ),
    ]