# Generated by Django 4.2 on 2023-08-17 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='logo_image',
            field=models.ImageField(upload_to='static/article-images'),
        ),
    ]