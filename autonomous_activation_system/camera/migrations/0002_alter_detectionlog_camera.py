# Generated manually to fix missing related_name on DetectionLog.camera

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detectionlog',
            name='camera',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='detection_logs',
                to='camera.camera',
            ),
        ),
    ]
