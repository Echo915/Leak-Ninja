# Generated by Django 4.2.4 on 2023-08-21 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_newdata_density'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pipedata',
            name='fluid_data',
        ),
        migrations.RemoveField(
            model_name='pipedata',
            name='unit',
        ),
        migrations.DeleteModel(
            name='NewData',
        ),
        migrations.DeleteModel(
            name='PipeData',
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
    ]
