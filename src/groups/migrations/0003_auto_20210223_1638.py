# Generated by Django 3.1.4 on 2021-02-23 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20210208_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.group'),
        ),
        migrations.DeleteModel(
            name='GroupCompetition',
        ),
    ]