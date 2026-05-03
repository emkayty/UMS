"""
Migration for Hostel models
Add hostel management tables
"""

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institution', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.UUIDField(
                    primary_key=True,
                    default=uuid.uuid4,
                    editable=False
                )),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('hostel_type', models.CharField(
                    choices=[
                        ('male', 'Male'),
                        ('female', 'Female'),
                        ('mixed', 'Mixed'),
                    ],
                    default='male'
                )),
                ('gender', models.CharField(
                    choices=[
                        ('male', 'Male'),
                        ('female', 'Female'),
                    ],
                    default='male'
                )),
                ('total_beds', models.IntegerField(default=100)),
                ('available_beds', models.IntegerField(default=100)),
                ('floors', models.IntegerField(default=3)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'hostels',
            },
        ),
        migrations.CreateModel(
            name='HostelApplication',
            fields=[
                ('id', models.UUIDField(
                    primary_key=True,
                    default=uuid.uuid4,
                    editable=False
                )),
                ('session', models.ForeignKey(
                    on_delete=models.CASCADE,
                    related_name='hostel_applications',
                    to='academic.academicsession'
                )),
                ('room_preference', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(
                    choices=[
                        ('pending', 'Pending'),
                        ('approved', 'Approved'),
                        ('rejected', 'Rejected'),
                    ],
                    default='pending',
                    max_length=20
                )),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('processed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'hostel_applications',
            },
        ),
    ]