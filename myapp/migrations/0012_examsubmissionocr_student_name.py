# Generated by Django 5.0.4 on 2024-06-26 12:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0011_alter_examsubmission_score_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="examsubmissionocr",
            name="student_name",
            field=models.CharField(default="Anonymous", max_length=100),
        ),
    ]
