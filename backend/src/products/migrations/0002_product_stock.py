# Generated by Django 3.0.5 on 2020-04-14 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(db_index=True, null=True),
        ),
    ]
