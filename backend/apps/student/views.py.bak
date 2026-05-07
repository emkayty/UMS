"""
Student API Views
Student management endpoints
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.student.models import StudentProfile
from apps.student.serializers import (
    StudentProfileSerializer, GuardianSerializer,
    NextOfKinSerializer, ParentNotificationSerializer
)
from apps.student.admission import OnlineApplication
from apps.student.admission_serializers import (
    OnlineApplicationSerializer, AdmissionLetterSerializer
)
from apps.student.transcript import TranscriptRequest


class StudentProfileViewSet(viewsets.ModelViewSet):
    """API endpoints for student profiles."""
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    
    @action(detail=False, methods=['get'])
    def by_matric(self, request):
        """Get student by matric number."""
        matric = request.query_params.get('matric_number')
        try:
            student = StudentProfile.objects.get(matric_number=matric)
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response(
                {'error': 'Student not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def guardians(self, request, pk=None):
        """Get student's guardians."""
        student = self.get_object()
        guardians = student.guardians.all()
        serializer = GuardianSerializer(guardians, many=True)
        return Response(serializer.data)


class OnlineApplicationViewSet(viewsets.ModelViewSet):
    """API endpoints for online applications."""
    queryset = OnlineApplication.objects.all()
    serializer_class = OnlineApplicationSerializer
    
    @action(detail=False, methods=['post'])
    def submit(self, request):
        """Submit new application."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def status_check(self, request):
        """Check application status."""
        app_number = request.query_params.get('application_number')
        email = request.query_params.get('email')
        try:
            app = OnlineApplication.objects.get(
                application_number=app_number,
                email=email
            )
            serializer = self.get_serializer(app)
            return Response(serializer.data)
        except OnlineApplication.DoesNotExist:
            return Response(
                {'error': 'Application not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class TranscriptRequestViewSet(viewsets.ModelViewSet):
    """API endpoints for transcript requests."""
    queryset = TranscriptRequest.objects.all()
    serializer_class = TranscriptRequestSerializer
    
    @action(detail=False, methods=['post'])
    def request_transcript(self, request):
        """Request new transcript."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)