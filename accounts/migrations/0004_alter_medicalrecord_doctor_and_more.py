# Generated by Django 5.1 on 2024-09-02 21:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_appointment_doctor_alter_appointment_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalrecord',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records_as_doctor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records_as_patient', to=settings.AUTH_USER_MODEL),
        ),
    ]
