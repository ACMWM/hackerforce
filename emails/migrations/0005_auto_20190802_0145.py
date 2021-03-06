# Generated by Django 2.2.3 on 2019-08-02 01:45

from django.db import migrations
import shared.forms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0004_auto_20190709_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='contacted_selection',
            field=shared.forms.fields.MultiSelectField(blank=True, choices=[('U', 'Uncontacted'), ('C1', 'Contacted 1x'), ('C2', 'Contacted 2x'), ('C3', 'Contacted 3x or more')], max_length=10),
        ),
        migrations.AlterField(
            model_name='email',
            name='primary_selection',
            field=shared.forms.fields.MultiSelectField(blank=True, choices=[('P', 'Primary'), ('NP', 'Not-Primary')], max_length=4),
        ),
        migrations.AlterField(
            model_name='email',
            name='size_selection',
            field=shared.forms.fields.MultiSelectField(blank=True, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], max_length=5),
        ),
    ]
