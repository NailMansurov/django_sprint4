# Generated by Django 3.2.16 on 2024-06-04 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20240605_0338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_published',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='blogicum_images', verbose_name='Изображения'),
        ),
    ]