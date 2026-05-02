"""
Management command to initialize the system
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.core.models import AcademicSession, Faculty, Department, Programme

User = get_user_model()


class Command(BaseCommand):
    help = 'Initialize the UMS system with default data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-email',
            type=str,
            default='admin@unicore.edu',
            help='Admin email address'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            default='admin123',
            help='Admin password'
        )

    def handle(self, *args, **options):
        self.stdout.write('🎓 Initializing UMS...')
        
        # Create superuser
        self._create_superuser(
            options['admin_email'],
            options['admin_password']
        )
        
        # Create academic session
        self._create_session()
        
        # Create sample faculties
        self._create_faculties()
        
        self.stdout.write(self.style.SUCCESS('✅ Initialization complete!'))

    def _create_superuser(self, email, password):
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                first_name='System',
                last_name='Administrator'
            )
            self.stdout.write(f'✅ Created superuser: {email}')
        else:
            self.stdout.write(f'ℹ️  Superuser already exists: {email}')

    def _create_session(self):
        if not AcademicSession.objects.exists():
            AcademicSession.objects.create(
                name='2024/2025',
                is_current=True
            )
            self.stdout.write('✅ Created academic session: 2024/2025')
        else:
            self.stdout.write('ℹ️  Academic session already exists')

    def _create_faculties(self):
        if Faculty.objects.exists():
            self.stdout.write('ℹ️  Faculty already exists')
            return
            
        # Create faculties
        faculties = [
            {'name': 'Faculty of Science', 'code': 'SCI'},
            {'name': 'Faculty of Arts', 'code': 'ART'},
            {'name': 'Faculty of Engineering', 'code': 'ENG'},
            {'name': 'Faculty of Medicine', 'code': 'MED'},
            {'name': 'Faculty of Social Sciences', 'code': 'SOC'},
        ]
        
        for f in faculties:
            Faculty.objects.create(**f)
        
        self.stdout.write(f'✅ Created {len(faculties)} faculties')
        
        # Create departments
        science = Faculty.objects.get(code='SCI')
        departments = [
            {'name': 'Computer Science', 'code': 'CS', 'faculty': science},
            {'name': 'Mathematics', 'code': 'MTH', 'faculty': science},
            {'name': 'Physics', 'code': 'PHY', 'faculty': science},
            {'name': 'Chemistry', 'code': 'CHM', 'faculty': science},
            {'name': 'Biology', 'code': 'BIO', 'faculty': science},
        ]
        
        for d in departments:
            Department.objects.create(**d)
        
        self.stdout.write(f'✅ Created {len(departments)} departments')
        
        # Create programmes
        cs = Department.objects.get(code='CS')
        programmes = [
            {
                'name': 'Computer Science',
                'code': 'CS',
                'duration_years': 4,
                'department': cs
            },
            {
                'name': 'Software Engineering',
                'code': 'SE',
                'duration_years': 4,
                'department': cs
            },
            {
                'name': 'Information Systems',
                'code': 'IS',
                'duration_years': 4,
                'department': cs
            },
        ]
        
        for p in programmes:
            Programme.objects.create(**p)
        
        self.stdout.write(f'✅ Created {len(programmes)} programmes')