from ninja import Router, Schema
from typing import Optional, List
from django.shortcuts import get_object_or_404
import uuid

from apps.finance.models import FeeItem, StudentFee, Payment, Scholarship

router = Router(tags=['Finance'])


# === Schemas ===
class FeeItemSchema(Schema):
    id: str
    name: str
    amount: float
    is_compulsory: bool
    programme_id: Optional[str]
    session_id: Optional[str]
    level: Optional[int]


class StudentFeeSchema(Schema):
    id: str
    student_id: str
    fee_item: dict
    amount_due: float
    amount_paid: float
    status: str


class PaymentSchema(Schema):
    id: str
    student_id: str
    amount: float
    payment_ref: str
    gateway: str
    status: str
    paid_at: Optional[str]


# === Finance Schemas ===
class FeeItemCreateSchema(Schema):
    name: str
    amount: float
    is_compulsory: bool = True
    programme_id: Optional[str] = None
    session_id: Optional[str] = None
    level: Optional[int] = None
    description: str = ""


class FeeItemUpdateSchema(Schema):
    name: Optional[str] = None
    amount: Optional[float] = None
    is_compulsory: Optional[bool] = None
    description: Optional[str] = None


class PaymentInitSchema(Schema):
    student_id: str
    amount: float
    fee_item_id: str


class ScholarshipCreateSchema(Schema):
    name: str
    amount: float
    criteria: dict = {}


class PaymentSchema(Schema):
    id: str
    student_id: str
    amount: float
    payment_ref: str
    gateway: str
    status: str
    paid_at: Optional[str]


# === Fee Item CRUD ===
@router.get('/fees', response=List[FeeItemSchema])
def list_fee_items(request, programme_id: str = None, session_id: str = None, level: int = None):
    """List fee items with optional filters."""
    qs = FeeItem.objects.all()
    if programme_id:
        qs = qs.filter(programme_id=programme_id)
    if session_id:
        qs = qs.filter(session_id=session_id)
    if level:
        qs = qs.filter(level=level)
    return qs[:100]  # Limit results


@router.post('/fees', response=FeeItemSchema)
def create_fee_item(request, data: FeeItemCreateSchema):
    """Create fee item (bursar only)."""
    # Validate amount
    if data.amount <= 0:
        from rest_framework.response import Response
        from rest_framework import status
        return Response({'error': 'Amount must be positive'}, status=status.HTTP_400_BAD_REQUEST)
    
    fee = FeeItem.objects.create(
        name=data.name,
        amount=data.amount,
        is_compulsory=data.is_compulsory,
        programme_id=data.programme_id,
        session_id=data.session_id,
        level=data.level,
        description=data.description
    )
    return fee


@router.get('/fees/{id}', response=FeeItemSchema)
def get_fee_item(request, id: str):
    """Get fee item by ID."""
    return get_object_or_404(FeeItem, id=id)


@router.put('/fees/{id}', response=FeeItemSchema)
def update_fee_item(request, id: str, data: FeeItemUpdateSchema):
    """Update fee item (bursar only)."""
    fee = get_object_or_404(FeeItem, id=id)
    
    if data.name is not None:
        fee.name = data.name
    if data.amount is not None:
        fee.amount = data.amount
    if data.is_compulsory is not None:
        fee.is_compulsory = data.is_compulsory
    if data.description is not None:
        fee.description = data.description
    
    fee.save()
    return fee


@router.delete('/fees/{id}')
def delete_fee_item(request, id: str):
    """Delete fee item (bursar only)."""
    fee = get_object_or_404(FeeItem, id=id)
    fee.delete()
    return {'success': True, 'message': 'Fee item deleted'}


# === Student Fees ===
@router.get('/student-fees/{student_id}')
def get_student_fees(request, student_id: str):
    """Get student fee records."""
    fees = StudentFee.objects.filter(student_id=student_id)
    
    return [
        {
            'fee_item': f.fee_item.name,
            'amount_due': float(f.amount_due),
            'amount_paid': float(f.amount_paid),
            'balance': float(f.amount_due - f.amount_paid),
            'status': f.status
        }
        for f in fees
    ]


@router.post('/generate-invoices')
def generate_invoices(request, data: dict):
    """Generate invoices for students."""
    from apps.student.models import StudentProfile
    
    fee_item_id = data.get('fee_item_id')
    fee_item = get_object_or_404(FeeItem, id=fee_item_id)
    
    # Get target students
    programme_id = data.get('programme_id')
    level = data.get('level')
    
    students = StudentProfile.objects.all()
    if programme_id:
        students = students.filter(programme_id=programme_id)
    if level:
        students = students.filter(current_level=level)
    
    invoices = []
    for student in students:
        sf, created = StudentFee.objects.get_or_create(
            student=student,
            fee_item=fee_item,
            defaults={'amount_due': fee_item.amount}
        )
        if created:
            invoices.append(str(sf.id))
    
    return {'success': True, 'generated': len(invoices)}


# === Payment APIs ===
@router.post('/payments/initialize', response=dict)
def initialize_payment(request, data: dict):
    """Initialize payment with gateway."""
    from apps.institution.models import Settings
    
    settings = Settings.get_instance()
    student_id = data.get('student_id')
    amount = data.get('amount')
    fee_item_ids = data.get('fee_item_ids', [])
    
    # Create payment record
    payment_ref = f"PN{uuid.uuid4().hex[:12].upper()}"
    payment = Payment.objects.create(
        student_id=student_id,
        amount=amount,
        payment_ref=payment_ref,
        gateway=settings.payment_gateway
    )
    
    # Generate payment link based on gateway
    if settings.payment_gateway == 'paystack':
        payment_link = f"https://api.paystack.co/payment/{payment_ref}"
    else:
        payment_link = f"https://api.flutterwave.com/v3/payments/{payment_ref}"
    
    return {
        'success': True,
        'payment_ref': payment_ref,
        'payment_link': payment_link,
        'amount': float(amount)
    }


@router.get('/payments/verify')
def verify_payment(request, reference: str):
    """Verify payment with gateway."""
    payment = get_object_or_404(Payment, payment_ref=reference)
    
    # In production, verify with gateway API
    # For now, mark as success
    payment.status = 'success'
    payment.paid_at = datetime.now()
    payment.save()
    
    # Update student fee
    student_fees = StudentFee.objects.filter(student=payment.student)
    for sf in student_fees:
        sf.amount_paid += payment.amount
        if sf.amount_paid >= sf.amount_due:
            sf.status = 'paid'
        else:
            sf.status = 'partial'
        sf.save()
    
    return {'success': True, 'status': payment.status}


@router.get('/payments/history', response=List[PaymentSchema])
def get_payment_history(request, student_id: str = None):
    """Get payment history."""
    qs = Payment.objects.all()
    if student_id:
        qs = qs.filter(student_id=student_id)
    return qs


@router.get('/payments/log')
def get_payment_log(request, start_date: str = None, end_date: str = None):
    """Get payment log with filters."""
    qs = Payment.objects.all()
    if start_date:
        qs = qs.filter(created_at__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__lte=end_date)
    
    total_amount = sum(float(p.amount) for p in qs if p.status == 'success')
    
    return {
        'payments': [
            {
                'student': p.student.matric_number or str(p.student.id),
                'amount': float(p.amount),
                'status': p.status,
                'date': p.created_at.isoformat()
            }
            for p in qs[:100]
        ],
        'total_amount': total_amount,
        'count': len(qs)
    }


# === Scholarship APIs ===
@router.post('/scholarships')
def allocate_scholarship(request, data: dict):
    """Allocate scholarship to student."""
    scholarship = Scholarship.objects.create(
        student_id=data.get('student_id'),
        name=data.get('name'),
        amount=data.get('amount'),
        awarded_by=data.get('awarded_by'),
        session_id=data.get('session_id')
    )
    return {'success': True}


@router.get('/scholarships')
def list_scholarships(request, session_id: str = None):
    """List scholarships."""
    qs = Scholarship.objects.all()
    if session_id:
        qs = qs.filter(session_id=session_id)
    return [
        {
            'student': s.student.matric_number,
            'name': s.name,
            'amount': float(s.amount),
            'session': s.session.name
        }
        for s in qs
    ]


# === Debt Management ===
@router.get('/debtors')
def get_debtors(request, programme_id: str = None):
    """Get students with outstanding debts."""
    from apps.student.models import StudentProfile
    
    # Find students with partial/pending fees
    student_fees = StudentFee.objects.filter(
        status__in=['pending', 'partial']
    ).select_related('student')
    
    debtors = {}
    for sf in student_fees:
        if sf.amount_due - sf.amount_paid > 0:
            sid = str(sf.student.id)
            if sid not in debtors:
                debtors[sid] = {
                    'student': sf.student.matric_number,
                    'total_due': 0,
                    'total_paid': 0
                }
            debtors[sid]['total_due'] += float(sf.amount_due)
            debtors[sid]['total_paid'] += float(sf.amount_paid)
    
    return [
        {**d, 'balance': d['total_due'] - d['total_paid']}
        for d in debtors.values()
    ]


# === Reports ===
@router.get('/reports/income-statement')
def income_statement(request, session_id: str = None):
    """Generate income statement."""
    qs = Payment.objects.filter(status='success')
    if session_id:
        qs = qs.filter(session_id=session_id)
    
    total = sum(float(p.amount) for p in qs)
    
    return {
        'total_income': total,
        'payment_count': len(qs)
    }


from datetime import datetime