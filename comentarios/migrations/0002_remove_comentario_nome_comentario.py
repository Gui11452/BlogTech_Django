# Generated by Django 4.1.2 on 2022-10-23 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comentarios', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='nome_comentario',
        ),
    ]
