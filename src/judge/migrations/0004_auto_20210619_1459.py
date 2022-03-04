# Generated by Django 3.1.4 on 2021-06-19 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0003_auto_20210605_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='classification',
            field=models.CharField(choices=[('CB', 'Combinatorics'), ('BS', 'Breadth-first-search'), ('2S', '2-set'), ('AS', 'Algorithms on strings'), ('BG', 'Beginners'), ('SB', 'Binary-search'), ('DS', 'Depth-first-search')], max_length=2),
        ),
        migrations.AlterField(
            model_name='problem',
            name='classification_en',
            field=models.CharField(choices=[('CB', 'Combinatorics'), ('BS', 'Breadth-first-search'), ('2S', '2-set'), ('AS', 'Algorithms on strings'), ('BG', 'Beginners'), ('SB', 'Binary-search'), ('DS', 'Depth-first-search')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='classification_uk',
            field=models.CharField(choices=[('CB', 'Combinatorics'), ('BS', 'Breadth-first-search'), ('2S', '2-set'), ('AS', 'Algorithms on strings'), ('BG', 'Beginners'), ('SB', 'Binary-search'), ('DS', 'Depth-first-search')], max_length=2, null=True),
        ),
    ]
