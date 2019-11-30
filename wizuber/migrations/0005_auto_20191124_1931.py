# Generated by Django 2.2.6 on 2019-11-24 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wizuber', '0004_auto_20191124_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spiritartifact',
            name='spirit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='spirit_artifacts', to='wizuber.Spirit'),
        ),
        migrations.AlterField(
            model_name='student',
            name='teacher',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='wizuber.Wizard'),
        ),
        migrations.AlterField(
            model_name='wish',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='owned_wishes', to='wizuber.Wizard'),
        ),
    ]