# Generated by Django 4.2.4 on 2023-08-21 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0003_remove_pipedata_fluid_data_remove_pipedata_unit_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50, unique=True)),
                ('density', models.CharField(max_length=10)),
                ('data', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PipeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diameter', models.CharField(max_length=10)),
                ('length', models.CharField(max_length=10)),
                ('fluid_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.newdata')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.unit')),
            ],
        ),
    ]
