"""
Extended Student Lifecycle & Data Collection Models
Comprehensive Nigerian University Standards
"""

from django.db import models
import uuid


# ==================== PRE-ADMISSION DATA ====================

class ApplicantData(models.Model):
    """Complete pre-admission data collection."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Personal Information
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    
    # Additional personal details
    title = models.CharField(max_length=10, blank=True)  # Mr, Mrs, Miss, Dr, Prof
    other_names = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100, blank=True)
    nationality = models.CharField(max_length=50, default='Nigerian')
    state_of_origin = models.CharField(max_length=50)
    local_govt_area = models.CharField(max_length=50)
    
    # Contact Information
    postal_address = models.TextField()
    residential_address = models.TextField()
    permanent_address = models.TextField()
    
    # Parent/Guardian Information
    father_name = models.CharField(max_length=100, blank=True)
    father_phone = models.CharField(max_length=20, blank=True)
    father_email = models.EmailField(blank=True)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_office_address = models.TextField(blank=True)
    
    mother_name = models.CharField(max_length=100, blank=True)
    mother_phone = models.CharField(max_length=20, blank=True)
    mother_email = models.EmailField(blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_office_address = models.TextField(blank=True)
    
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)
    guardian_email = models.EmailField(blank=True)
    guardian_occupation = models.CharField(max_length=100, blank=True)
    guardian_address = models.TextField(blank=True)
    guardian_relationship = models.CharField(max_length=50, blank=True)
    
    # Sponsor Details (for international students)
    sponsor_name = models.CharField(max_length=100, blank=True)
    sponsor_address = models.TextField(blank=True)
    sponsor_phone = models.CharField(max_length=20, blank=True)
    sponsor_relationship = models.CharField(max_length=50, blank=True)
    
    # Medical Information
    blood_group = models.CharField(max_length=5, blank=True)
    genotype = models.CharField(max_length=5, blank=True)
    disabilities = models.TextField(blank=True)
    chronic_illnesses = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relationship = models.CharField(max_length=50)
    
    # Educational Background
    primary_school = models.CharField(max_length=200, blank=True)
    primary_school_year = models.IntegerField(null=True, blank=True)
    secondary_school = models.CharField(max_length=200, blank=True)
    secondary_school_year = models.IntegerField(null=True, blank=True)
    
    # O-Level Results (Multiple sittings)
    o_level_sitting1_exam_type = models.CharField(max_length=20, blank=True)  # WAEC, NECO
    o_level_sitting1_year = models.IntegerField(null=True, blank=True)
    o_level_sitting1_center = models.CharField(max_length=50, blank=True)
    o_level_sitting1_results = models.JSONField(default=dict)  # {subject: grade}
    
    o_level_sitting2_exam_type = models.CharField(max_length=20, blank=True)
    o_level_sitting2_year = models.IntegerField(null=True, blank=True)
    o_level_sitting2_center = models.CharField(max_length=50, blank=True)
    o_level_sitting2_results = models.JSONField(default=dict)
    
    # JAMB Details
    jamb_registration_number = models.CharField(max_length=20, blank=True)
    jamb_score = models.IntegerField(null=True, blank=True)
    jamb_subject1 = models.CharField(max_length=50, blank=True)
    jamb_subject2 = models.CharField(max_length=50, blank=True)
    jamb_subject3 = models.CharField(max_length=50, blank=True)
    jamb_subject4 = models.CharField(max_length=50, blank=True)
    jamb_choices = models.JSONField(default=list)  # List of institution choices
    
    # Post-UTME
    post_utme_score = models.IntegerField(null=True, blank=True)
    post_utme_date = models.DateField(null=True, blank=True)
    
    # Transfer Students
    is_transfer = models.BooleanField(default=False)
    previous_institution = models.CharField(max_length=200, blank=True)
    previous_matric_number = models.CharField(max_length=30, blank=True)
    transfer_credits = models.JSONField(default=list)  # [{course: code, grade: grade, credits: int}]
    
    # International Students
    is_international = models.BooleanField(default=False)
    passport_number = models.CharField(max_length=30, blank=True)
    passport_expiry = models.DateField(null=True, blank=True)
    visa_number = models.CharField(max_length=30, blank=True)
    visa_expiry = models.DateField(null=True, blank=True)
    country_of_origin = models.CharField(max_length=50, blank=True)
    
    # Documents Upload
    passport_photo = models.URLField(blank=True)
    birth_certificate = models.URLField(blank=True)
    o_level_certificate = models.URLField(blank=True)
    jamb_admission_letter = models.URLField(blank=True)
    medical_certificates = models.JSONField(default=list)
    sponsor_passport = models.URLField(blank=True)
    
    # Status
    application_status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('screening', 'Screening'),
            ('offered', 'Offer Made'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='draft'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ==================== ADMISSION PROCESS ====================

class AdmissionOffer(models.Model):
    """Admission offer management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    applicant = models.ForeignKey(ApplicantData, on_delete=models.CASCADE)
    
    # Offer Details
    programme = models.ForeignKey('academic.Programme', on_delete=models.CASCADE)
    admission_batch = models.CharField(max_length=50)  # e.g., 2024/2025-1
    
    # Matriculation
    matric_number = models.CharField(max_length=30, unique=True, null=True, blank=True)
    
    # Offer Acceptance
    offer_accepted = models.BooleanField(default=False)
    acceptance_date = models.DateField(null=True, blank=True)
    acceptance_fee_paid = models.BooleanField(default=False)
    
    # Admission Letter
    admission_letter_url = models.URLField(blank=True)
    letter_issued_date = models.DateField(null=True, blank=True)
    
    # Screening
    screening_date = models.DateField(null=True, blank=True)
    screening_venue = models.CharField(max_length=100, blank=True)
    screening_result = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('cleared', 'Cleared'),
            ('incomplete', 'Incomplete Documents'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    screening_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class StudentIDCard(models.Model):
    """Student ID Card management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.OneToOneField('student.StudentProfile', on_delete=models.CASCADE)
    
    # Photo
    photo_url = models.URLField(blank=True)
    photo_uploaded_at = models.DateTimeField(null=True, blank=True)
    
    # Card Details
    card_number = models.CharField(max_length=30, unique=True)
    barcode = models.CharField(max_length=50, unique=True)
    qr_code = models.CharField(max_length=100, unique=True)
    
    # Status
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('printed', 'Printed'),
        ('issued', 'Issued'),
        ('expired', 'Expired'),
        ('lost', 'Lost'),
        ('replaced', 'Replaced'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    # Issue Details
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    collected_by = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


# ==================== STUDENT SERVICES ====================

class StudentHostelAllocation(models.Model):
    """Hostel room allocation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    # Hostel Details
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)
    block = models.CharField(max_length=20)
    floor = models.IntegerField()
    room_number = models.CharField(max_length=20)
    bed_number = models.IntegerField()
    room_type = models.CharField(
        max_length=20,
        choices=[
            ('single', 'Single'),
            ('double', 'Double'),
            ('triple', 'Triple'),
            ('4_in_room', '4 in Room'),
            ('6_in_room', '6 in Room'),
        ]
    )
    
    # Status
    STATUS = [
        ('allocated', 'Allocated'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='allocated')
    
    # Check-in/out
    check_in_date = models.DateField(null=True, blank=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    
    # Fees
    hostel_fee = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)


class Hostel(models.Model):
    """Hostel management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('mixed', 'Mixed')])
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)
    
    # Facilities
    has_wifi = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=False)
    has_bathroom = models.BooleanField(default=True)
    has_laundry = models.BooleanField(default=False)
    
    # Location
    location = models.CharField(max_length=100)
    description = models.TextField()
    
    is_active = models.BooleanField(default=True)


class StudentChangeRequest(models.Model):
    """Student change requests (programme, name, etc.)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    
    REQUEST_TYPES = [
        ('programme', 'Change of Programme'),
        ('department', 'Change of Department'),
        ('faculty', 'Change of Faculty'),
        ('name', 'Change of Name'),
        ('details', 'Update Personal Details'),
    ]
    
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    
    # Change Details
    current_value = models.TextField()
    requested_value = models.TextField()
    reason = models.TextField()
    
    # Supporting Documents
    documents = models.JSONField(default=list)
    
    # Approval Workflow
    STATUS = [
        ('pending', 'Pending'),
        ('hod_approved', 'HOD Approved'),
        ('dean_approved', 'Dean Approved'),
        ('registrar_approved', 'Registrar Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    # Approvers
    hod_comment = models.TextField(blank=True)
    hod_approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    hod_approved_at = models.DateTimeField(null=True, blank=True)
    
    dean_comment = models.TextField(blank=True)
    dean_approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    dean_approved_at = models.DateTimeField(null=True, blank=True)
    
    registrar_comment = models.TextField(blank=True)
    registrar_approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    registrar_approved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentDiscipline(models.Model):
    """Student disciplinary records."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    
    # Incident
    incident_date = models.DateField()
    incident_location = models.CharField(max_length=100)
    incident_description = models.TextField()
    
    OFFENCE_TYPES = [
        ('academic_dishonesty', 'Academic Dishonesty'),
        ('examination_misconduct', 'Examination Misconduct'),
        ('assault', 'Assault'),
        ('theft', 'Theft'),
        ('drugs', 'Drug Possession/Use'),
        ('alcohol', 'Alcohol'),
        ('bullying', 'Bullying/Harassment'),
        ('vandalism', 'Vandalism'),
        ('noise', 'Noise Pollution'),
        ('non_attendance', 'Non-Attendance'),
        ('uniform', 'Uniform Violation'),
        ('other', 'Other'),
    ]
    
    offence_type = models.CharField(max_length=30, choices=OFFENCE_TYPES)
    
    # Severity
    SEVERITY = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('major', 'Major'),
        ('severe', 'Severe'),
    ]
    severity = models.CharField(max_length=20, choices=SEVERITY)
    
    # Action
    ACTION_TYPES = [
        ('warning', 'Written Warning'),
        ('counseling', 'Counseling'),
        ('suspension', 'Suspension'),
        ('expulsion', 'Expulsion'),
        ('rustication', 'Rustication'),
        ('dismissal', 'Dismissal'),
        ('withdrawal', 'Withdrawal'),
        ('not_proven', 'Not Proven'),
        ('acquitted', 'Acquitted'),
    ]
    
    action = models.CharField(max_length=20, choices=ACTION_TYPES, blank=True)
    action_start_date = models.DateField(null=True, blank=True)
    action_end_date = models.DateField(null=True, blank=True)
    
    # Investigation
    investigated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='discipline_investigated')
    investigation_report = models.TextField(blank=True)
    investigation_date = models.DateField(null=True, blank=True)
    
    # Panel
    disciplinary_panel = models.JSONField(default=list)  # List of panel members
    panel_decision = models.TextField(blank=True)
    
    # Appeal
    appeal_filed = models.BooleanField(default=False)
    appeal_date = models.DateField(null=True, blank=True)
    appeal_decision = models.TextField(blank=True)
    
    # Status
    STATUS = [
        ('reported', 'Reported'),
        ('investigating', 'Under Investigation'),
        ('hearing', 'Panel Hearing'),
        ('decided', 'Decision Made'),
        ('appealed', 'Under Appeal'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='reported')
    
    created_at = models.DateTimeField(auto_now_add=True)


class StudentSurvey(models.Model):
    """Student feedback and surveys."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    SURVEY_TYPES = [
        ('course_eval', 'Course Evaluation'),
        ('lecturer_eval', 'Lecturer Evaluation'),
        ('exit', 'Exit Survey'),
        ('satisfaction', 'Satisfaction Survey'),
        ('nss', 'National Service'),
    ]
    
    survey_type = models.CharField(max_length=20, choices=SURVEY_TYPES)
    
    # Target
    target_level = models.IntegerField(null=True, blank=True)
    target_programme = models.ForeignKey('academic.Programme', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Questions
    questions = models.JSONField(default=list)
    # [{question: text, type: rating/text, options: [], required: bool}]
    
    # Schedule
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Anonymity
    is_anonymous = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class StudentSurveyResponse(models.Model):
    """Student survey responses."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    survey = models.ForeignKey(StudentSurvey, on_delete=models.CASCADE)
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    
    responses = models.JSONField(default=dict)
    # {question_id: answer}
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['survey', 'student']


# ==================== SIWES / INDUSTRIAL TRAINING ====================

class IndustrialAttachment(models.Model):
    """SIWES/Industrial Training tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    # Company Details
    company_name = models.CharField(max_length=200)
    company_address = models.TextField()
    company_phone = models.CharField(max_length=20)
    company_email = models.EmailField()
    company_industry = models.CharField(max_length=100)
    
    # Supervisor
    supervisor_name = models.CharField(max_length=100)
    supervisor_phone = models.CharField(max_length=20)
    supervisor_email = models.EmailField()
    supervisor_designation = models.CharField(max_length=100)
    
    # Period
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Logbook
    weekly_log_url = models.URLField(blank=True)
    supervisor_evaluation_url = models.URLField(blank=True)
    company_cert_url = models.URLField(blank=True)
    
    # Assessment
    supervisor_rating = models.IntegerField(null=True, blank=True)  # 1-5
    supervisor_remarks = models.TextField(blank=True)
    
    # University Assessment
    university_grade = models.CharField(max_length=5, blank=True)
    university_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Status
    STATUS = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('graded', 'Graded'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)


# ==================== GRADUATION ====================

class GraduationClearance(models.Model):
    """Graduation clearance checklist."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    # Clearance Items - Each department signs off
    LIBRARY = 'library'
    BURSAR = 'bursar'
    HOSTEL = 'hostel'
    DEPARTMENT = 'department'
    DEAN = 'dean'
    REGISTRAR = 'registrar'
    SPORTS = 'sports'
    ICT = 'ict'
    
    CLEARANCE_AREAS = [
        (LIBRARY, 'Central Library'),
        (BURSAR, 'Bursary'),
        (HOSTEL, 'Hostel Management'),
        (DEPARTMENT, 'Department'),
        (DEAN, 'Dean of Faculty'),
        (REGISTRAR, 'Registrar'),
        (SPORTS, 'Sports Department'),
        (ICT, 'ICT Center'),
    ]
    
    # Each area has their own clearance
    library_cleared = models.BooleanField(default=False)
    library_date = models.DateField(null=True, blank=True)
    library_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='lib_clearances')
    library_notes = models.TextField(blank=True)
    
    bursar_cleared = models.BooleanField(default=False)
    bursar_date = models.DateField(null=True, blank=True)
    bursar_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='bursar_clearances')
    bursar_notes = models.TextField(blank=True)
    
    hostel_cleared = models.BooleanField(default=False)
    hostel_date = models.DateField(null=True, blank=True)
    hostel_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='hostel_clearances')
    hostel_notes = models.TextField(blank=True)
    
    department_cleared = models.BooleanField(default=False)
    department_date = models.DateField(null=True, blank=True)
    department_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='dept_clearances')
    department_notes = models.TextField(blank=True)
    
    sports_cleared = models.BooleanField(default=False)
    sports_date = models.DateField(null=True, blank=True)
    sports_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='sports_clearances')
    
    ict_cleared = models.BooleanField(default=False)
    ict_date = models.DateField(null=True, blank=True)
    ict_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='ict_clearances')
    
    # Overall
    eligible_to_graduate = models.BooleanField(default=False)
    cleared_at = models.DateTimeField(null=True, blank=True)
    cleared_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='grad_clearances')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AlumniRecord(models.Model):
    """Alumni tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE)
    
    # Graduation Details
    graduation_year = models.IntegerField()
    convocation_date = models.DateField(null=True, blank=True)
    degree_awarded = models.CharField(max_length=100)
    class_of_degree = models.CharField(
        max_length=30,
        choices=[
            ('first_class', 'First Class'),
            ('second_upper', 'Second Class Upper'),
            ('second_lower', 'Second Class Lower'),
            ('third', 'Third Class'),
            ('pass', 'Pass'),
        ]
    )
    
    # Current Employment
    is_employed = models.BooleanField(default=False)
    employer_name = models.CharField(max_length=200, blank=True)
    employer_address = models.TextField(blank=True)
    employer_phone = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    job_start_date = models.DateField(null=True, blank=True)
    salary_range = models.CharField(max_length=30, blank=True)
    
    # Sector
    SECTORS = [
        ('public', 'Public Sector'),
        ('private', 'Private Sector'),
        ('self_employed', 'Self Employed'),
        ('ngo', 'NGO'),
        ('startup', 'Startup'),
        ('further_study', 'Further Study'),
        ('unemployed', 'Unemployed'),
        ('other', 'Other'),
    ]
    employment_sector = models.CharField(max_length=20, choices=SECTORS, blank=True)
    
    # Further Study
    further_institution = models.CharField(max_length=200, blank=True)
    further_programme = models.CharField(max_length=100, blank=True)
    further_country = models.CharField(max_length=50, blank=True)
    
    # Location
    current_city = models.CharField(max_length=50, blank=True)
    current_country = models.CharField(max_length=50, default='Nigeria')
    
    # Contact
    personal_phone = models.CharField(max_length=20, blank=True)
    personal_email = models.EmailField(blank=True)
    
    # Social
    linkedin_url = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    facebook_url = models.URLField(blank=True)
    
    # Consent
    can_contact = models.BooleanField(default=True)
    can_list = models.BooleanField(default=True)  # In alumni directory
    verified = models.BooleanField(default=False)
    
    updated_at = models.DateTimeField(auto_now=True)