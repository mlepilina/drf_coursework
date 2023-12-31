# Generated by Django 4.2.6 on 2023-10-25 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_notice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habitsconnection',
            name='pleasant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_pleasants', to='main_app.habit', verbose_name='приятная'),
        ),
        migrations.AlterField(
            model_name='habitsconnection',
            name='useful',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_usefuls', to='main_app.habit', verbose_name='полезная'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='habit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='main_app.habit', verbose_name='привычка'),
        ),
    ]
