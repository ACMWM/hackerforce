# Generated by Django 2.1.9 on 2019-07-02 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20190630_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='status',
        ),
        migrations.AlterField(
            model_name='contact',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='companies.Company'),
        ),
    ]
