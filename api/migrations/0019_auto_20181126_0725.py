# Generated by Django 2.1 on 2018-11-26 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20181126_0718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='theemail',
            new_name='email',
        ),
    ]