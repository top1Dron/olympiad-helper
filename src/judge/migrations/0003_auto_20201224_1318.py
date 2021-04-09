# Generated by Django 3.1.4 on 2020-12-24 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0002_auto_20201223_1516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktest',
            name='memory_limit',
        ),
        migrations.RemoveField(
            model_name='tasktest',
            name='time_limit',
        ),
        migrations.AddField(
            model_name='task',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='task',
            name='memory_limit',
            field=models.CharField(default='128', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='time_limit',
            field=models.CharField(default='1', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasksamples',
            name='sample_output',
            field=models.TextField(default='', verbose_name='Sample output #'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='programminglanguage',
            name='name',
            field=models.TextField(verbose_name='Programming language'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description_photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='task',
            name='number',
            field=models.SlugField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='special_warning',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Warning'),
        ),
        migrations.AlterField(
            model_name='tasksamples',
            name='sample_input',
            field=models.TextField(verbose_name='Sample input #'),
        ),
    ]