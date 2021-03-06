# Generated by Django 3.1.4 on 2021-04-29 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('competitions', '0001_initial'), ('competitions', '0002_delete_competitionproblem'), ('competitions', '0003_competition_description'), ('competitions', '0004_auto_20210421_2111')]

    initial = True

    dependencies = [
        ('groups', '0001_squashed_0008_auto_20210429_1731'),
        # ('judge', '0001_squashed_0021_auto_20210429_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('group', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.group')),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
    ]
