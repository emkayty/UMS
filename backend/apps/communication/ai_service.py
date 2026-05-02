"""
AI Chatbot Service
Production-ready LLM integration with fallback
"""

import os
import json
import requests
import uuid
from datetime import datetime
from django.db import models
from django.conf import settings

# Try to import OpenAI, provide fallback if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ChatbotService:
    """AI-powered university assistant."""
    
    # System prompt for university context
    SYSTEM_PROMPT = """You are UniCore, an AI assistant for a Nigerian university.
    
    You help students with:
    - Admission inquiries and requirements
    - Course registration and scheduling
    - Fee payments and financial aid
    - Academic policies and procedures
    - Hostel and facilities
    - NYSC and graduation requirements
    
    Guidelines:
    - Be helpful, accurate, and concise
    - If unsure, suggest contacting the registry
    - Reference university policies when relevant
    - Be empathetic to student concerns
    
    Current academic calendar info:
    - First Semester: October - February
    - Second Semester: March - July
    - Registration deadline: 2 weeks after semester starts
    """
    
    @classmethod
    def get_client(cls):
        """Get OpenAI client."""
        if not OPENAI_AVAILABLE:
            return None
        
        api_key = getattr(settings, 'OPENAI_API_KEY', None) or os.getenv('OPENAI_API_KEY')
        if not api_key:
            return None
        
        return OpenAI(api_key=api_key)
    
    @classmethod
    def chat(cls, message, conversation_history=None, user_context=None):
        """Process chat message."""
        client = cls.get_client()
        
        if client is None:
            # Use rule-based fallback
            return cls._rule_based_response(message)
        
        try:
            # Build messages
            messages = [{"role": "system", "content": cls.SYSTEM_PROMPT}]
            
            # Add conversation_history
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages
                    messages.append(msg)
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Get response
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                'message': response.choices[0].message.content,
                'model': 'gpt-4o-mini',
                'tokens': response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
            
        except Exception as e:
            # Fallback to rule-based
            return cls._rule_based_response(message)
    
    @classmethod
    def _rule_based_response(cls, message):
        """Rule-based responses for common questions."""
        message = message.lower()
        
        responses = {
            'admission': {
                'keywords': ['admission', 'apply', 'jamb', 'utme', 'post-utme'],
                'response': """For admission inquiries:

• UTME/POST-UTME: Score requirements vary by programme
• O-Level: At least 5 credits including English and Math
• Direct Entry: Good ND/NCE results considered
• Visit the admissions office or call for current requirements
• Apply online at university portal"""
            },
            'registration': {
                'keywords': ['register', 'course', 'registration', 'add', 'drop'],
                'response': """Course Registration:

• Log in to student portal
• Select 'Course Registration' from menu
• Choose courses for your level/programme
• Verify no time conflicts
• Pay school fees first
• Submit before deadline"""
            },
            'fees': {
                'keywords': ['fee', 'payment', 'school fees', 'tuition'],
                'response': """Fee Information:

• School fees vary by level and programme
• Payment via bank or online portal
• Get clearance slip after payment
• Contact bursary for issues
• Financial aid available for qualifying students"""
            },
            'result': {
                'keywords': ['result', 'grade', 'score', 'transcript'],
                'response': """Results & Transcripts:

• Check portal for semester results
• Request transcript from registry
• Minimum 30% for pass
• First class: 3.5+ CGPA
• Contact HOD for grading concerns"""
            },
            'hostel': {
                'keywords': ['hostel', 'accommodation', 'room'],
                'response': """Hostel Allocation:

• First come, first served
• Apply through portal after admission
• Limited availability
• Off-campus options available
• Pay hostel fees separately"""
            },
            'nysc': {
                'keywords': ['nysc', 'service', 'post-graduation'],
                'response': """NYSC Information:

• Compulsory after graduation
• Register within specific timeframe
• Upload credentials to NYSC portal
• Contact Dean of Students for clearance
• mobilisation is seasonal"""
            },
            'default': {
                'keywords': [],
                'response': """Thank you for your message. 

For specific inquiries, please contact:
• Academic: Registry - registry@university.edu
• Finance: Bursary - bursary@university.edu
• Student Affairs: Dean of Students

Or visit the student portal for self-service."""
            }
        }
        
        # Find matching category
        for category, data in responses.items():
            for keyword in data['keywords']:
                if keyword in message:
                    return {
                        'message': data['response'],
                        'model': 'rule-based',
                        'fallback': True
                    }
        
        return {
            'message': responses['default']['response'],
            'model': 'rule-based',
            'fallback': True
        }


class DocumentAIService:
    """Document processing with AI (OCR, extraction)."""
    
    @classmethod
    def extract_text(cls, image_path):
        """Extract text from image (requires OCR service)."""
        # Would use Google Vision API or Tesseract
        # Placeholder implementation
        
        return {
            'text': '',
            'confidence': 0,
            'error': 'OCR not configured'
        }
    
    @classmethod
    def validate_document(cls, doc_type, extracted_data):
        """Validate extracted document data."""
        validators = {
            'transcript': ['matric_number', 'gpa', 'courses'],
            'certificate': ['name', 'award', 'date'],
            'id_card': ['matric_number', 'name', 'photo']
        }
        
        required_fields = validators.get(doc_type, [])
        missing = [f for f in required_fields if f not in extracted_data]
        
        return {
            'valid': len(missing) == 0,
            'missing_fields': missing,
            'confidence': (len(required_fields) - len(missing)) / len(required_fields)
        }


class SmartSearchService:
    """Semantic search across university data."""
    
    @classmethod
    def search(cls, query, target='all'):
        """Search with keyword matching."""
        results = []
        
        # Would use embeddings for semantic search
        # Using keyword matching as fallback
        
        if target in ['all', 'courses']:
            from apps.academic.models import Course
            courses = Course.objects.filter(
                models.Q(code__icontains=query) |
                models.Q(title__icontains=query) |
                models.Q(description__icontains=query)
            )[:10]
            
            for c in courses:
                results.append({
                    'type': 'course',
                    'id': str(c.id),
                    'title': c.title,
                    'code': c.code
                })
        
        if target in ['all', 'programmes']:
            from apps.academic.models import Programme
            progs = Programme.objects.filter(
                models.Q(name__icontains=query) |
                models.Q(code__icontains=query)
            )[:10]
            
            for p in progs:
                results.append({
                    'type': 'programme',
                    'id': str(p.id),
                    'title': p.name,
                    'code': p.code
                })
        
        return results[:20]