"""
Student Admission Serializers
Online application and admission serializers
"""

from rest_framework import serializers
from apps.student.admission import (
    OnlineApplication, OLevelResult, PostUtmeResult, AdmissionLetter
)


class OLevelResultSerializer(serializers.ModelSerializer):
    """Serializer for O-Level results."""
    
    class Meta:
        model = OLevelResult
        fields = [
            'id', 'exam_type', 'exam_year', 'exam_number',
            'subjects', 'is_verified'
        ]


class OnlineApplicationSerializer(serializers.ModelSerializer):
    """Serializer for online applications."""
    olevel_results = OLevelResultSerializer(many=True, read_only=True)
    
    class Meta:
        model = OnlineApplication
        fields = [
            'id', 'application_number', 'session',
            'first_name', 'last_name', 'other_names',
            'email', 'phone', 'date_of_birth', 'gender',
            'nationality', 'state_of_origin',
            'jamb_number', 'jamb_score', 'jamb_year',
            'first_choice', 'second_choice',
            'status', 'payment_status', 'screening_score',
            'olevel_results', 'submitted_at'
        ]
        read_only_fields = [
            'id', 'application_number', 'submitted_at'
        ]


class PostUtmeResultSerializer(serializers.ModelSerializer):
    """Serializer for Post-UTME results."""
    
    class Meta:
        model = PostUtmeResult
        fields = [
            'id', 'application', 'score', 'total',
            'percentile', 'exam_date', 'venue'
        ]


class AdmissionLetterSerializer(serializers.ModelSerializer):
    """Serializer for admission letters."""
    
    class Meta:
        model = AdmissionLetter
        fields = [
            'id', 'application', 'admitted_programme',
            'admission_number', 'admission_session',
            'admission_level', 'is_accepted', 'acceptance_deadline',
            'acceptance_fee', 'acceptance_fee_paid',
            'letter_sent', 'pdf_file'
        ]