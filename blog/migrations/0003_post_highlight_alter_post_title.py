# Generated by Django 4.1.7 on 2023-04-08 09:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_alter_post_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="highlight",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(max_length=100),
        ),
    ]
