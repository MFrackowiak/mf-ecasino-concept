# Generated by Django 2.0.4 on 2018-04-21 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0001_initial'),
        ('bonus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='awardedbonus',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='player.Player'),
        ),
    ]
