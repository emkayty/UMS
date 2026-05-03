"""
Migration for Online Admissions
Add online application system
"""

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('academic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineApplication',
            fields=[
                ('id', models.UUIDField(
                    primary_key=True,
                    default=uuid.uuid4,
                    editable=False
                )),
                ('application_number', models.CharField(
                    max_length=20,
                    unique=True
                )),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('other_names', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(
                    choices=[
                        ('male', 'Male'),
                        ('female', 'Female'),
                    ],
                    max_length=10
                )),
                ('nationality', models.CharField(
                    default='Nigerian',
                    max_length=50
                )),
                ('state_of_origin', models.CharField(blank=True, max_length=50)),
                ('jamb_number', models.CharField(blank=True, max_length=20)),
                ('jamb_score', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(
                    choices=[
                        ('draft', 'Draft'),
                        ('submitted', 'Submitted'),
                        ('screening', 'Screening'),
                        ('accepted', 'Accepted'),
                        ('rejected', 'Rejected'),
                    ],
                    default='draft',
                    max_length=20
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'online_applications',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AdmissionLetter',
            fields=[
                ('id', models.UUIDField(
                    primary_key=True,
                    default=uuid.uuid4,
                    editable=False
                )),
                ('admission_number', models.CharField(
                    max_length=20,
                    unique=True
                )),
                ('is_accepted', models.BooleanField(default=False)),
                ('acceptance_fee', models.DecimalField(
                    max_digits=12,
                    decimal_places=2
                )),
                ('acceptance_fee_paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'admission_letters',
            },
        ),
    ]