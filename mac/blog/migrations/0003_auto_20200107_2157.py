# Generated by Django 3.0.1 on 2020-01-07 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200107_2154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='content_head3',
            new_name='content_head1',
        ),
    ]
