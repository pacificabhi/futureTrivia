# Generated by Django 2.1.1 on 2018-10-18 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia', '0026_remove_triviaresult_total_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trivia',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]