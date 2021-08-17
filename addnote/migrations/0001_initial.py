# Generated by Django 3.1.3 on 2021-08-16 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('sttText', models.TextField()),
                ('note_description', models.TextField()),
                ('reg_date', models.DateTimeField()),
                ('audio', models.ImageField(upload_to='audio')),
                ('vis_js_nodes', models.TextField()),
                ('vis_js_edges', models.TextField()),
            ],
        ),
    ]
