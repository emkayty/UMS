"""
Migration for ProgrammeType
Add programme type choices
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='programme_type',
            field=models.CharField(
                choices=[
                    ('nd', 'National Diploma (ND)'),
                    ('hnd', 'Higher National Diploma (HND)'),
                    ('bsc', 'Bachelor of Science (BSc)'),
                    ('msc', 'Master of Science (MSc)'),
                    ('phd', 'Doctor of Philosophy (PhD)'),
                    ('aa', 'Associate of Arts (AA)'),
                    ('as', 'Associate of Science (AS)'),
                    ('bs', 'Bachelor of Science (BS)'),
                    ('mba', 'Master of Business Administration (MBA)'),
                ],
                max_length=10,
                default='bsc'
            ),
        ),
    ]