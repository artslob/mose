# Generated by Django 2.2.6 on 2019-11-23 16:26

from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wizuber.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='RightsSupport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('customer_perm', 'Global customer rights'), ('wizard_perm', 'Global wizard rights'), ('student_perm', 'Global student rights'), ('spirit_perm', 'Global spirit rights')),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WizuberUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='middle name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_wizuber.wizuberuser_set+', to='contenttypes.ContentType')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            managers=[
                ('objects', wizuber.models.PolymorphicUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaseArtifact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_wizuber.baseartifact_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('wizuberuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('balance', models.PositiveIntegerField(default=500)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('wizuber.wizuberuser',),
            managers=[
                ('objects', wizuber.models.PolymorphicUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Spirit',
            fields=[
                ('wizuberuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('grade', models.CharField(choices=[('IMP', 'Imp'), ('FOLIOT', 'Foliot'), ('DJINNI', 'Djinni'), ('AFRIT', 'Afrit'), ('MARID', 'Marid')], max_length=6)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('wizuber.wizuberuser',),
            managers=[
                ('objects', wizuber.models.PolymorphicUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Wizard',
            fields=[
                ('wizuberuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('balance', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('wizuber.wizuberuser',),
            managers=[
                ('objects', wizuber.models.PolymorphicUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('NEW', 'New'), ('ACTIVE', 'Active'), ('WORK', 'Work'), ('READY', 'Ready'), ('CLOSED', 'Closed'), ('CANCELED', 'Canceled')], default='NEW', max_length=8)),
                ('price', models.PositiveIntegerField(default=50, validators=[django.core.validators.MinValueValidator(limit_value=1)])),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_wishes', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_wishes', to='wizuber.Customer')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_wishes', to='wizuber.Wizard')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('wizuberuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('teacher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wizuber.Wizard')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('wizuber.wizuberuser',),
            managers=[
                ('objects', wizuber.models.PolymorphicUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SpiritArtifact',
            fields=[
                ('baseartifact_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wizuber.BaseArtifact')),
                ('spirit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='spirit_artifact', to='wizuber.Spirit')),
                ('wish', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='spirit_artifact', to='wizuber.Wish')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('wizuber.baseartifact',),
        ),
        migrations.AddField(
            model_name='spirit',
            name='master',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wizuber.Wizard'),
        ),
        migrations.CreateModel(
            name='PentacleArtifact',
            fields=[
                ('baseartifact_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wizuber.BaseArtifact')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('size', models.CharField(choices=[('LARGE', 'large'), ('MEDIUM', 'medium'), ('SMALL', 'small')], default='MEDIUM', max_length=6)),
                ('wish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pentacle_artifacts', to='wizuber.Wish')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('wizuber.baseartifact',),
        ),
        migrations.CreateModel(
            name='CandleArtifact',
            fields=[
                ('baseartifact_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wizuber.BaseArtifact')),
                ('size', models.CharField(choices=[('LARGE', 'large'), ('MEDIUM', 'medium'), ('SMALL', 'small')], default='MEDIUM', max_length=6)),
                ('material', models.CharField(choices=[('TALLOW', 'tallow'), ('BEESWAX', 'beeswax'), ('PARAFFIN', 'paraffin')], default='TALLOW', max_length=8)),
                ('wish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candle_artifacts', to='wizuber.Wish')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('wizuber.baseartifact',),
        ),
    ]
