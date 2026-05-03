"""
Student Serializers
Main student module serializers
"""

from rest_framework import serializers
from apps.student.models import StudentProfile
from apps.student.guardian import Guardian, NextOfKin
from apps.student.parent_portal import ParentAccount, ParentNotification
from apps.student.transcript import TranscriptRequest


class GuardianSerializer(serializers.ModelSerializer):
    """Serializer for guardian information."""
    
    class Meta:
        model = Guardian
        fields = [
            'id', 'relation', 'first_name', 'last_name',
            'email', 'phone', 'alt_phone',
            'address', 'occupation', 'is_emergency_contact'
        ]


class NextOfKinSerializer(serializers.ModelSerializer):
    """Serializer for next of kin."""
    
    class Meta:
        model = NextOfKin
        fields = [
            'id', 'first_name', 'last_name', 'relation',
            'phone', 'email', 'address', 'is_emergency'
        ]


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for student profiles."""
    guardians = GuardianSerializer(many=True, read_only=True)
    next_of_kin = NextOfKinSerializer(many=True, read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'matric_number', 'surname', 'first_name',
            'other_names', 'gender', 'date_of_birth',
            'nationality', 'state_of_origin', 'lga',
            'programme', 'department', 'level', 'status',
            'admission_year', 'graduation_year',
            'guardians', 'next_of_kin',
            'phone', 'email', 'address'
        ]


class ParentAccountSerializer(serializers.ModelSerializer):
    """Serializer for parent accounts."""
    
    class Meta:
        model = ParentAccount
        fields = [
            'id', 'user', 'relation',
            'can_view_results', 'can_view_attendance',
            'can_view_fees', 'can_receive_alerts',
            'status', 'approved_at'
        ]


class ParentNotificationSerializer(serializers.ModelSerializer):
    """Serializer for parent notifications."""
    
    class Meta:
        model = ParentNotification
        fields = [
            'id', 'parent', 'student', 'notification_type',
            'title', 'message', 'sent_via_email',
            'sent_via_sms', 'is_read'
        ]


class TranscriptRequestSerializer(serializers.ModelSerializer):
    """Serializer for transcript requests."""
    
    class Meta:
        model = TranscriptRequest
        fields = [
            'id', 'student', 'transcript_type', 'delivery_method',
            'copies', 'recipient_name', 'recipient_institution',
            'recipient_address', 'recipient_email',
            'status', 'amount', 'payment_status',
            'created_at'
        ]