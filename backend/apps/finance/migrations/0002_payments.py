"""
Migration for Payment system
Add payment and invoice tables
"""

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.UUIDField(
                    primary_key=True,
                    default=uuid.uuid4,
                    editable=False
                )),
                ('amount', models.DecimalField(max_digits=12, decimal_places=2)),
                ('payment_type', models.CharField(
                    choices=[
                        ('school_fee', 'School Fee'),
                        ('acceptance', 'Acceptance Fee'),
                        ('hostel', 'Hostel Fee'),
                        ('transcript', 'Transcript Fee'),
                    ],
                    max_length=20
                )),
                ('gateway', models.CharField(
                    choices=[
                        ('paystack', 'Paystack'),
                        ('flutterwave', 'Flutterwave'),
                        ('bank_transfer', 'Bank Transfer'),
                    ],
                    max_length=20
                )),
                ('status', models.CharField(
                    choices=[
                        ('pending', 'Pending'),
                        ('success', 'Success'),
                        ('failed', 'Failed'),
                    ],
                    default='pending',
                    max_length=20
                )),
                ('transaction_ref', models.CharField(
                    max_length=50,
                    unique=True
                )),
                ('currency', models.CharField(
                    default='NGN',
                    max_length=10
                )),
                ('initiated_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'payment_transactions',
                'ordering': ['-initiated_at'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.UUIDField(
                    primary_key=True,
                    default=uuid.uuid4,
                    editable=False
                )),
                ('invoice_number', models.CharField(
                    max_length=50,
                    unique=True
                )),
                ('items', models.JSONField(default=list)),
                ('subtotal', models.DecimalField(max_digits=12, decimal_places=2)),
                ('discount', models.DecimalField(
                    default=0,
                    max_digits=12, decimal_places=2
                )),
                ('total', models.DecimalField(max_digits=12, decimal_places=2)),
                ('status', models.CharField(
                    choices=[
                        ('pending', 'Pending'),
                        ('paid', 'Paid'),
                    ],
                    default='pending',
                    max_length=20
                )),
                ('due_date', models.DateField()),
                ('amount_paid', models.DecimalField(
                    default=0,
                    max_digits=12, decimal_places=2
                )),
                ('balance', models.DecimalField(max_digits=12, decimal_places=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'invoices',
                'ordering': ['-created_at'],
            },
        ),
    ]