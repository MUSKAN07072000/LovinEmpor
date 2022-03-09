# Generated by Django 4.0 on 2022-02-02 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_order_tel'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.CharField(max_length=100)),
                ('update_desc', models.CharField(max_length=1000000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]