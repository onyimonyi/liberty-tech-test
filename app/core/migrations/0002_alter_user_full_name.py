# Generated by Django 3.2 on 2022-04-27 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(default='timezone.now', max_length=255),
            preserve_default=False,
        ),
    ]