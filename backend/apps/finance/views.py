"""
Finance API Views
Payment and invoice endpoints
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.finance.models import FeeType
from apps.finance.serializers import (
    PaymentTransactionSerializer, InvoiceSerializer,
    RefundSerializer, BankAccountSerializer
)
from apps.finance.payments import PaymentTransaction, Invoice


class PaymentViewSet(viewsets.ModelViewSet):
    """API endpoints for payments."""
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    
    @action(detail=False, methods=['post'])
    def initiate(self, request):
        """Initiate new payment."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Verify payment status."""
        ref = request.data.get('transaction_ref')
        try:
            txn = PaymentTransaction.objects.get(transaction_ref=ref)
            serializer = self.get_serializer(txn)
            return Response(serializer.data)
        except PaymentTransaction.DoesNotExist:
            return Response(
                {'error': 'Transaction not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class InvoiceViewSet(viewsets.ModelViewSet):
    """API endpoints for invoices."""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get student's invoices."""
        student_id = request.query_params.get('student_id')
        invoices = Invoice.objects.filter(student_id=student_id)
        serializer = self.get_serializer(invoices, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def make_payment(self, request, pk=None):
        """Make payment for invoice."""
        invoice = self.get_object()
        # Process payment
        return Response({'status': 'Payment processed'})


class FeeTypeViewSet(viewsets.ModelViewSet):
    """API endpoints for fee types."""
    queryset = FeeType.objects.all()
    serializer_class = FeeTypeSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        active = self.request.query_params.get('active')
        if active == 'true':
            queryset = queryset.filter(is_active=True)
        return queryset


class BankAccountViewSet(viewsets.ModelViewSet):
    """API endpoints for bank accounts."""
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer