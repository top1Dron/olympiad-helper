# Generated by Django 3.1.4 on 2021-04-09 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0014_problem_competition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='number',
            field=models.SlugField(max_length=1000, unique=True),
        ),
    ]
