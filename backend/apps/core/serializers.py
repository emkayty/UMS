"""
Abstract Serializers
Standardized, Professional API Serializers
"""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils import timezone


# ============================================================
# BASE SERIALIZERS
# ============================================================

class BaseSerializer(serializers.ModelSerializer):
    """Abstract base serializer with common functionality."""
    
    class Meta:
        abstract = True
    
    # UUID field
    uuid = serializers.UUIDField(read_only=True)
    
    # Timestamp fields
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Common fields
    is_active = serializers.BooleanField(default=True)
    status = serializers.CharField(read_only=True)
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().update(instance, validated_data)


class ReadOnlySerializer(serializers.ModelSerializer):
    """Serializer with all fields read-only."""
    
    class Meta:
        abstract = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].read_only = True


class NestedSerializer(serializers.ModelSerializer):
    """Serializer with nested objects."""
    
    class Meta:
        abstract = True
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Convert UUID to string
        if 'uuid' in rep:
            rep['uuid'] = str(rep['uuid'])
        return rep


# ============================================================
# CHOICE SERIALIZERS
# ============================================================

class ChoiceField(serializers.ChoiceField):
    """Enhanced choice field."""
    
    def __init__(self, choices, **kwargs):
        self.choice_names = {c[0]: c[1] for c in choices}
        super().__init__(choices=choices, **kwargs)


# ============================================================
# VALIDATION SERIALIZERS
# ============================================================

class ValidateOnCreateSerializer(BaseSerializer):
    """Serializer that validates on create only."""
    
    class Meta:
        abstract = True
    
    def validate(self, attrs):
        # Skip validation on update
        if self.instance:
            return attrs
        return super().validate(attrs)


class ValidateOnUpdateSerializer(BaseSerializer):
    """Serializer that validates on update only."""
    
    class Meta:
        abstract = True
    
    def validate(self, attrs):
        # Skip validation on create
        if not self.instance:
            return attrs
        return super().validate(attrs)


# ============================================================
# FILTERS
# ============================================================

class BaseFilterSerializer(serializers.Serializer):
    """Base filter serializer."""
    
    search = serializers.CharField(required=False)
    status = serializers.ChoiceField(
        choices=['draft', 'pending', 'active', 'inactive', 'archived'],
        required=False
    )
    is_active = serializers.BooleanField(required=False)
    
    # Pagination
    page = serializers.IntegerField(default=1, min_value=1)
    page_size = serializers.IntegerField(default=20, min_value=1, max_value=100)
    
    # Ordering
    ordering = serializers.CharField(default='-created_at')


# ============================================================
# RESPONSE SERIALIZERS
# ============================================================

class PaginatedResponseSerializer(serializers.Serializer):
    """Standard paginated response."""
    
    def __init__(self, data=None, status_code=200, **kwargs):
        self.status_code = status_code
        super().__init__(data=data, **kwargs)
    
    def to_representation(self, data):
        return {
            'status_code': self.status_code,
            'results': data.get('results', []),
            'pagination': {
                'page': data.get('page', 1),
                'page_size': data.get('page_size', 20),
                'total_pages': data.get('total_pages', 1),
                'total_count': data.get('total_count', 0),
                'has_next': data.get('has_next', False),
                'has_prev': data.get('has_prev', False),
            }
        }


class ErrorResponseSerializer(serializers.Serializer):
    """Standard error response."""
    
    code = serializers.CharField()
    message = serializers.CharField()
    details = serializers.DictField(required=False)
    timestamp = serializers.DateTimeField(default=timezone.now)


class SuccessResponseSerializer(serializers.Serializer):
    """Standard success response."""
    
    message = serializers.CharField()
    data = serializers.DictField(required=False)


# ============================================================
# HELPER MIXINS
# ============================================================

class TimestampMixin:
    """Add timestamp functionality."""
    
    def get_timestamp(self, obj):
        return timezone.now().isoformat()


class StatusMixin:
    """Add status functionality."""
    
    def get_status_display(self, obj):
        return obj.get_status_display()


class UserMixin:
    """Add user info functionality."""
    
    def get_created_by(self, obj):
        if obj.created_by:
            return {
                'uuid': str(obj.created_by.uuid),
                'email': obj.created_by.email,
                'name': obj.created_by.get_full_name() or obj.created_by.username
            }
        return None
    
    def get_updated_by(self, obj):
        if obj.updated_by:
            return {
                'uuid': str(obj.updated_by.uuid),
                'email': obj.updated_by.email,
                'name': obj.updated_by.get_full_name() or obj.updated_by.username
            }
        return None


# ============================================================
# COMMON SERIALIZERS
# ============================================================

class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user info serializer."""
    
    class Meta:
        from apps.accounts.models import User
        model = User
        fields = ['uuid', 'email', 'first_name', 'last_name', 'is_active']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['uuid'] = str(rep['uuid'])
        return rep


class UserFullSerializer(UserBasicSerializer):
    """Full user info serializer."""
    
    class Meta(UserBasicSerializer.Meta):
        fields = ['uuid', 'email', 'first_name', 'last_name', 'phone', 
                 'is_active', 'is_staff', 'date_joined']


# ============================================================
# EXPORT SERIALIZERS
# ============================================================

class ExportSerializer(serializers.Serializer):
    """Export data serializer."""
    
    format = serializers.ChoiceField(
        choices=['csv', 'excel', 'json', 'pdf'],
        default='csv'
    )
    fields = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    include_headers = serializers.BooleanField(default=True)


# ============================================================
# ID SERIALIZER
# ============================================================

class UUIDSerializer(serializers.Serializer):
    """Serializer for UUID input."""
    
    uuid = serializers.UUIDField()
    
    def validate_uuid(self, value):
        return str(value)