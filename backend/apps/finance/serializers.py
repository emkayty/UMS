"""
Finance Serializers
Payment and invoice serializers
"""

from rest_framework import serializers
from apps.finance.payments import (
    PaymentTransaction, Invoice, Refund, BankAccount, ManualPayment
)
from apps.finance.models import FeeType, Invoice as FeeInvoice


class BankAccountSerializer(serializers.ModelSerializer):
    """Serializer for bank accounts."""
    
    class Meta:
        model = BankAccount
        fields = [
            'id', 'bank_name', 'account_number', 'account_name',
            'account_type', 'is_active', 'is_default'
        ]


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """Serializer for payment transactions."""
    
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'user', 'amount', 'payment_type',
            'gateway', 'gateway_ref', 'status',
            'transaction_ref', 'invoice_number',
            'channel', 'currency',
            'initiated_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'transaction_ref', 'initiated_at'
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for student invoices."""
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'student', 'invoice_number', 'session',
            'items', 'subtotal', 'discount', 'total',
            'status', 'due_date', 'amount_paid', 'balance',
            'created_at'
        ]
        read_only_fields = ['id', 'invoice_number']


class RefundSerializer(serializers.ModelSerializer):
    """Serializer for refund requests."""
    
    class Meta:
        model = Refund
        fields = [
            'id', 'transaction', 'amount', 'reason',
            'status', 'requested_at', 'approved_at',
            'processed_at', 'rejection_reason'
        ]


class ManualPaymentSerializer(serializers.ModelSerializer):
    """Serializer for manual payments."""
    
    class Meta:
        model = ManualPayment
        fields = [
            'id', 'student', 'amount', 'bank_account',
            'sender_name', 'sender_account', 'sender_bank',
            'transfer_date', 'utr', 'status',
            'proof', 'verified_by', 'verified_at'
        ]


class FeeTypeSerializer(serializers.ModelSerializer):
    """Serializer for fee types."""
    
    class Meta:
        model = FeeType
        fields = [
            'id', 'name', 'code', 'fee_type',
            'amount', 'category', 'is_active'
        ]