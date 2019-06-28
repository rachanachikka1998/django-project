# Generated by Django 2.2.2 on 2019-06-28 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fbposts', '0002_auto_20190627_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fbposts.Post'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fbposts.Comment'),
        ),
    ]
