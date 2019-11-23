# Generated by Django 2.2.6 on 2019-11-23 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('wizuber', '0006_baseartifact_candleartifact_pentacleartifact_spiritartifact'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseartifact',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='candleartifact',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='pentacleartifact',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='spiritartifact',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AddField(
            model_name='baseartifact',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_wizuber.baseartifact_set+', to='contenttypes.ContentType'),
        ),
    ]
