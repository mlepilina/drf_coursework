# Generated by Django 4.2.6 on 2023-10-25 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_habitsconnection_pleasant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitsconnection',
            name='pleasant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_pleasants', to='main_app.habit', verbose_name='приятная привычка'),
        ),
        migrations.AlterField(
            model_name='habitsconnection',
            name='useful',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_usefuls', to='main_app.habit', verbose_name='полезная привычка'),
        ),
    ]
