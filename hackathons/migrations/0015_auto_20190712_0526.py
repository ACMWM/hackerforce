# Generated by Django 2.1.10 on 2019-07-12 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hackathons', '0014_auto_20190703_0453'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hackathon',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='lead',
            options={'ordering': ('contact__name', 'contact__company__name')},
        ),
        migrations.AlterModelOptions(
            name='perk',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='sponsorship',
            options={'ordering': ('company__name', 'hackathon__name')},
        ),
        migrations.AlterModelOptions(
            name='tier',
            options={'ordering': ('name',)},
        ),
    ]
