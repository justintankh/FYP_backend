# Generated by Django 4.0.1 on 2022-01-28 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20220121_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perishable',
            name='categories',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='perishable',
            name='categories_score',
            field=models.CharField(default='', max_length=5000),
        ),
        migrations.AlterField(
            model_name='perishable',
            name='img_url',
            field=models.CharField(max_length=1000),
        ),
    ]
