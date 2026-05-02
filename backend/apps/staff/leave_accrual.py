"""
Leave Accrual Service.
Calculates and manages staff leave accrual.
"""
from datetime import date, timedelta
from decimal import Decimal
from django.utils import timezone
from apps.staff.models import LeaveBalance, LeaveAccrualConfig, LeaveRequest


class LeaveAccrualService:
    """Service for managing leave accrual."""
    
    # Default leave types
    LEAVE_TYPES = {
        'annual': {'days': 21, 'frequency': 'monthly'},
        'sick': {'days': 14, 'frequency': 'monthly'},
        'study': {'days': 10, 'frequency': 'yearly'},
        'maternity': {'days': 84, 'frequency': 'yearly'},
        'paternity': {'days': 14, 'frequency': 'yearly'},
    }
    
    @classmethod
    def initialize_leave_balances(cls, staff_profile):
        """Initialize leave balances for new staff."""
        balances = []
        for leave_type, config in cls.LEAVE_TYPES.items():
            balance, created = LeaveBalance.objects.get_or_create(
                staff=staff_profile,
                leave_type=leave_type,
                defaults={
                    'total_days': 0,
                    'used_days': 0,
                    'year': date.today().year
                }
            )
            balances.append(balance)
        return balances
    
    @classmethod
    def calculate_accrual(cls, staff_profile, year=None):
        """Calculate and update leave accrual for a period."""
        if year is None:
            year = date.today().year
        
        accrued = {}
        
        # Calculate based on config or defaults
        for leave_type, config in cls.LEAVE_TYPES.items():
            period_days = config['days']
            frequency = config['frequency']
            
            if frequency == 'monthly':
                # Accrue monthly (1/12 of annual)
                earned = period_days / 12
            elif frequency == 'quarterly':
                earned = period_days / 4
            else:  # yearly
                earned = period_days
            
            accrued[leave_type] = round(earned, 2)
            
            # Update balance
            balance, _ = LeaveBalance.objects.get_or_create(
                staff=staff_profile,
                leave_type=leave_type,
                defaults={
                    'total_days': 0,
                    'used_days': 0,
                    'year': year
                }
            )
            
            # Add accrued days, respecting carry-over max
            config = LeaveAccrualConfig.objects.filter(
                leave_type=leave_type, is_active=True
            ).first()
            
            max_carry = config.max_carry_over if config else 5
            new_total = min(balance.total_days + earned, period_days + max_carry)
            balance.total_days = round(new_total, 2)
            balance.year = year
            balance.save()
        
        return accrued
    
    @classmethod
    def get_available_days(cls, staff_profile, leave_type):
        """Get available leave days for a type."""
        try:
            balance = LeaveBalance.objects.get(
                staff=staff_profile,
                leave_type=leave_type
            )
            return balance.total_days - balance.used_days
        except LeaveBalance.DoesNotExist:
            return 0
    
    @classmethod
    def can_take_leave(cls, staff_profile, leave_type, days):
        """Check if staff can take requested leave."""
        available = cls.get_available_days(staff_profile, leave_type)
        return available >= days
    
    @classmethod
    def record_leave_taken(cls, leave_request):
        """Record leave taken and update balance."""
        balance = LeaveBalance.objects.filter(
            staff=leave_request.staff,
            leave_type=leave_request.leave_type
        ).first()
        
        if balance:
            balance.used_days += leave_request.duration_days()
            balance.save()
            return True
        return False
    
    @classmethod
    def get_leave_summary(cls, staff_profile):
        """Get summary of all leave balances."""
        balances = LeaveBalance.objects.filter(staff=staff_profile)
        summary = {}
        
        for balance in balances:
            summary[balance.leave_type] = {
                'total': balance.total_days,
                'used': balance.used_days,
                'available': balance.total_days - balance.used_days,
                'year': balance.year
            }
        
        # Add any missing leave types
        for leave_type in cls.LEAVE_TYPES:
            if leave_type not in summary:
                summary[leave_type] = {
                    'total': 0, 'used': 0, 'available': 0, 
                    'year': date.today().year
                }
        
        return summary
