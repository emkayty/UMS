"""
Hostel Serializers
Serialization for hostel management API
"""

from rest_framework import serializers
from apps.institution.models import Hostel, HostelApplication


class HostelSerializer(serializers.ModelSerializer):
    """Serializer for Hostel model."""
    
    class Meta:
        model = Hostel
        fields = [
            'id', 'name', 'code', 'hostel_type', 'gender',
            'total_beds', 'available_beds', 'floors',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class HostelApplicationSerializer(serializers.ModelSerializer):
    """Serializer for HostelApplication."""
    
    class Meta:
        model = HostelApplication
        fields = [
            'id', 'student', 'hostel', 'session',
            'room_preference', 'status', 'applied_at',
            'processed_by', 'processed_at'
        ]
        read_only_fields = ['id', 'applied_at']


class HostelRoomSerializer(serializers.ModelSerializer):
    """Serializer for HostelRoom."""
    
    class Meta:
        model = Hostel  # Will add Room model reference
        fields = [
            'id', 'room_number', 'floor', 'room_type',
            'capacity', 'occupied', 'available',
            'price', 'amenities'
        ]


class HostelBedSerializer(serializers.ModelSerializer):
    """Serializer for HostelBed."""
    
    class Meta:
        model = Hostel  # Will add Bed model reference
        fields = [
            'id', 'bed_number', 'room', 'is_occupied',
            'student', 'check_in_date', 'check_out_date'
        ]