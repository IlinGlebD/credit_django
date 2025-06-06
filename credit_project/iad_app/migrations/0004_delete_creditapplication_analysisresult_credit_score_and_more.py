# Generated by Django 4.2.20 on 2025-05-26 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iad_app', '0003_creditapplication_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CreditApplication',
        ),
        migrations.AddField(
            model_name='analysisresult',
            name='credit_score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='analysisresult',
            name='suggested_rate',
            field=models.FloatField(default=0.0),
        ),
    ]
