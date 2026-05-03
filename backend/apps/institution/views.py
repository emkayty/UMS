"""
API Views for new modules
Views exposing serializers via API endpoints
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Hostel
from apps.institution.models import Hostel, HostelApplication
from apps.institution.serializers import (
    HostelSerializer, HostelApplicationSerializer
)


class HostelViewSet(viewsets.ModelViewSet):
    """API endpoints for Hostel management."""
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    
    @action(detail=True, methods=['get'])
    def available(self, request):
        """Get available hostels."""
        hostels = Hostel.objects.filter(available_beds__gt=0, is_active=True)
        serializer = self.get_serializer(hostels, many=True)
        return Response(serializer.data)


class HostelApplicationViewSet(viewsets.ModelViewSet):
    """API endpoints for hostel applications."""
    queryset = HostelApplication.objects.all()
    serializer_class = HostelApplicationSerializer
    
    @action(detail=False, methods=['post'])
    def apply(self, request):
        """Apply for hostel accommodation."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)