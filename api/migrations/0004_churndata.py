# Generated by Django 3.2.8 on 2022-07-25 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_csvdata_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChurnData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=100)),
                ('imageFile', models.ImageField(upload_to='post_imags')),
            ],
        ),
    ]
