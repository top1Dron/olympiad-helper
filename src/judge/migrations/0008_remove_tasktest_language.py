# Generated by Django 3.1.4 on 2021-01-16 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0007_auto_20210116_0217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktest',
            name='language',
        ),
    ]
