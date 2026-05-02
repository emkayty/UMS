"""
Extended Staff Lifecycle & HR Models
Comprehensive Nigerian University Standards
"""

from django.db import models
import uuid


# ==================== RECRUITMENT ====================

class JobPosting(models.Model):
    """Job vacancy posting."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Position Details
    title = models.CharField(max_length=200)
    department = models.ForeignKey('academic.Department', on_delete=models.CASCADE)
    faculty = models.ForeignKey('academic.Faculty', on_delete=models.CASCADE, null=True, blank=True)
    
    # Employment Terms
    EMPLOYMENT_TYPES = [
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('adjunct', 'Adjunct'),
        ('visiting', 'Visiting'),
        ('part_time', 'Part-time'),
        ('tutorial', 'Tutorial'),
    ]
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default='permanent')
    
    # Level
    LEVELS = [
        ('assistant', 'Assistant Lecturer'),
        ('lecturer', 'Lecturer II'),
        ('lecturer_i', 'Lecturer I'),
        ('senior', 'Senior Lecturer'),
        ('associate', 'Associate Professor'),
        ('professor', 'Professor'),
        ('professor_emeritus', 'Professor Emeritus'),
        ('chief', 'Chief Lecturer'),
        ('principal', 'Principal Lecturer'),
        ('senior_lecturer', 'Senior Lecturer'),
    ]
    level = models.CharField(max_length=30, choices=LEVELS, default='lecturer')
    
    # Requirements
    minimum_qualification = models.CharField(max_length=50)  # PhD, MSc, BSc
    required_experience_years = models.IntegerField(default=0)
    required_specialization = models.CharField(max_length=200)
    required_publications = models.IntegerField(default=0)
    
    # Description
    job_description = models.TextField()
    responsibilities = models.TextField()
    benefits = models.TextField()
    
    # Salary
    salary_range_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_range_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Timeline
    posting_date = models.DateField()
    closing_date = models.DateField()
    expected_start_date = models.DateField(null=True, blank=True)
    
    # Status
    STATUS = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('filled', 'Position Filled'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    
    # Views
    view_count = models.IntegerField(default=0)
    application_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class JobApplication(models.Model):
    """Job application tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    
    # Applicant Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Application Documents
    cv_url = models.URLField()
    cover_letter_url = models.URLField(blank=True)
    certificates_url = models.JSONField(default=list)
    
    # Qualification
    highest_qualification = models.CharField(max_length=50)
    qualification_institution = models.CharField(max_length=200)
    year_obtained = models.IntegerField()
    grade = models.CharField(max_length=20, blank=True)
    
    # Experience
    work_experience = models.JSONField(default=list)
    # [{company: str, position: str, start: date, end: date, current: bool}]
    
    # References
    references = models.JSONField(default=list)
    # [{name: str, position: str, phone: str, email: str}]
    
    # Status
    STATUS = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('offered', 'Offer Made'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='applied')
    
    # Screening
    screening_score = models.IntegerField(null=True, blank=True)
    screening_notes = models.TextField(blank=True)
    
    # Interview
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_venue = models.CharField(max_length=200, blank=True)
    interview_score = models.IntegerField(null=True, blank=True)
    interview_notes = models.TextField(blank=True)
    
    # Offer
    offered_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    offered_date = models.DateField(null=True, blank=True)
    offer_accepted = models.BooleanField(default=False)
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InterviewSchedule(models.Model):
    """Interview scheduling."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    
    # Interview Details
    interview_date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    duration_minutes = models.IntegerField(default=60)
    
    # Interviewers
    interviewers = models.JSONField(default=list)
    # [{name: str, email: str, role: str}]
    
    # Type
    TYPES = [
        ('phone', 'Phone'),
        ('video', 'Video'),
        ('in_person', 'In Person'),
        ('panel', 'Panel'),
    ]
    interview_type = models.CharField(max_length=20, choices=TYPES, default='in_person')
    
    # Result
    SCORES = [
        ('pending', 'Pending'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('deferred', 'Deferred'),
    ]
    result = models.CharField(max_length=20, choices=SCORES, default='pending')
    feedback = models.TextField(blank=True)
    
    # Reminders
    reminder_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)


# ==================== APPOINTMENT ====================

class Appointment(models.Model):
    """Staff appointment letter management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE)
    
    # Appointment Details
    job_posting = models.ForeignKey(JobPosting, on_delete=models.SET_NULL, null=True, blank=True)
    
    appointment_type = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New Appointment'),
            ('promotion', 'Promotion'),
            ('transfer', 'Transfer'),
            ('reappointment', 'Re-appointment'),
            ('contract_renewal', 'Contract Renewal'),
        ]
    )
    
    # Contract Terms
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_permanent = models.BooleanField(default=False)
    
    # Position
    job_title = models.CharField(max_length=200)
    department = models.ForeignKey('academic.Department', on_delete=models.CASCADE)
    faculty = models.ForeignKey('academic.Faculty', on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.CharField(max_length=50)
    
    # Salary
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    salary_scale = models.CharField(max_length=50)  # e.g., CONUASS
    step = models.IntegerField(default=1)
    
    # Terms
    probation_months = models.IntegerField(default=12)
    notice_period_days = models.IntegerField(default=30)
    
    # Documents
    appointment_letter_url = models.URLField(blank=True)
    contract_url = models.URLField(blank=True)
    terms_of_service_url = models.URLField(blank=True)
    
    # Status
    STATUS = [
        ('draft', 'Draft'),
        ('pending', 'Pending Acceptance'),
        ('accepted', 'Accepted'),
        ('active', 'Active'),
        ('terminated', 'Terminated'),
        ('expired', 'Expired'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    
    accepted_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class StaffIDCard(models.Model):
    """Staff ID Card management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.OneToOneField('staff.StaffProfile', on_delete=models.CASCADE)
    
    photo_url = models.URLField(blank=True)
    card_number = models.CharField(max_length=30, unique=True)
    barcode = models.CharField(max_length=50, unique=True)
    
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('printed', 'Printed'),
        ('issued', 'Issued'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


# ==================== TRAINING & DEVELOPMENT ====================

class TrainingNeed(models.Model):
    """Staff training needs analysis."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    # Current Skills Gap
    skills_gap = models.JSONField(default=list)
    # [{skill: str, current_level: int, required_level: int}]
    
    # Training Needs
    training_needs = models.JSONField(default=list)
    # [{topic: str, priority: str, reason: str}]
    
    # Status
    STATUS = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    
    created_at = models.DateTimeField(auto_now_add=True)


class TrainingProgram(models.Model):
    """Training program management."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Provider
    provider = models.CharField(max_length=200)
    provider_contact = models.TextField()
    
    # Details
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=200, blank=True)
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(blank=True)
    
    # Cost
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='NGN')
    
    # Certificates
    certificate_url = models.URLField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class StaffTraining(models.Model):
    """Staff training attendance."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE)
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)
    
    # Status
    STATUS = [
        ('nominated', 'Nominated'),
        ('approved', 'Approved'),
        ('attended', 'Attended'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='nominated')
    
    nomination_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)
    
    certificate_awarded = models.BooleanField(default=False)


class ConferenceAttendance(models.Model):
    """Conference attendance tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE)
    
    conference_name = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Paper Presentation
    paper_title = models.CharField(max_length=300, blank=True)
    is_presenter = models.BooleanField(default=False)
    
    # Funding
    funding_source = models.CharField(max_length=100, blank=True)
    amount_approved = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Report
    report_url = models.URLField(blank=True)
    
    STATUS = [
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='approved')
    
    created_at = models.DateTimeField(auto_now_add=True)


# ==================== PROMOTION ====================

class PromotionRequest(models.Model):
    """Staff promotion workflow."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    # Current Position
    current_rank = models.CharField(max_length=50)
    current_salary = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Promoted To
    proposed_rank = models.CharField(max_length=50)
    proposed_salary = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Criteria Met
    publications = models.IntegerField(default=0)
    years_in_grade = models.IntegerField(default=0)
    teaching_score = models.IntegerField(default=0)
    research_score = models.IntegerField(default=0)
    community_score = models.IntegerField(default=0)
    
    # Supporting Documents
    cv_url = models.URLField(blank=True)
    publications_url = models.JSONField(default=list)
    teaching_evaluation_url = models.URLField(blank=True)
    
    # HOD Recommendation
    hod_recommendation = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('recommended', 'Recommended'),
            ('not_recommended', 'Not Recommended'),
        ],
        default='pending'
    )
    hod_comment = models.TextField(blank=True)
    hod_approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    
    # Dean Recommendation
    dean_recommendation = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('recommended', 'Recommended'),
            ('not_recommended', 'Not Recommended'),
        ],
        default='pending'
    )
    dean_comment = models.TextField(blank=True)
    dean_approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    
    # VC/Registry Decision
    STATUS = [
        ('draft', 'Draft'),
        ('pending_hod', 'Pending HOD'),
        ('pending_dean', 'Pending Dean'),
        ('pending_vc', 'Pending VC'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    
    vc_approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    vc_approved_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


# ==================== LEAVE ====================

class LeaveRequest(models.Model):
    """Staff leave request with approval workflow."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE)
    
    LEAVE_TYPES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('study', 'Study Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('compassionate', 'Compassionate Leave'),
        ('unpaid', 'Unpaid Leave'),
        ('sabbatical', 'Sabbatical Leave'),
        ('conference', 'Conference Leave'),
    ]
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    
    start_date = models.DateField()
    end_date = models.DateField()
    working_days = models.IntegerField()
    
    reason = models.TextField()
    supporting_documents = models.JSONField(default=list)
    
    # Coverage
    has_cover = models.BooleanField(default=False)
    cover_officer = models.ForeignKey(
        'staff.StaffProfile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='covering_for'
    )
    
    # Approval Workflow
    STATUS = [
        ('draft', 'Draft'),
        ('pending_hod', 'Pending HOD Approval'),
        ('pending_hr', 'Pending HR Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    
    # HOD Approval
    hod_approved = models.BooleanField(default=False)
    hod_approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    hod_comment = models.TextField(blank=True)
    hod_approved_date = models.DateField(null=True, blank=True)
    
    # HR Approval
    hr_approved = models.BooleanField(default=False)
    hr_approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='+')
    hr_comment = models.TextField(blank=True)
    hr_approved_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class LeaveBalance(models.Model):
    """Staff leave balance tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE)
    session = models.ForeignKey('academic.AcademicSession', on_delete=models.CASCADE)
    
    # Leave Types and Balances
    annual_leave_days = models.IntegerField(default=21)
    annual_used = models.IntegerField(default=0)
    annual_remaining = models.IntegerField(default=21)
    
    sick_leave_days = models.IntegerField(default=14)
    sick_used = models.IntegerField(default=0)
    sick_remaining = models.IntegerField(default=14)
    
    casual_leave_days = models.IntegerField(default=7)
    casual_used = models.IntegerField(default=0)
    casual_remaining = models.IntegerField(default=7)
    
    class Meta:
        unique_together = ['staff', 'session']


# ==================== EXIT ====================

class ExitProcess(models.Model):
    """Staff exit process."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey('staff.StaffProfile', on_delete=models.CASCADE)
    
    EXIT_TYPES = [
        ('resignation', 'Resignation'),
        ('retirement', 'Retirement'),
        ('termination', 'Termination'),
        ('end_of_contract', 'End of Contract'),
        ('death', 'Death'),
        ('abscondment', 'Abscondment'),
    ]
    exit_type = models.CharField(max_length=20, choices=EXIT_TYPES)
    
    # Details
    notice_date = models.DateField()
    last_working_day = models.DateField()
    reason = models.TextField()
    
    # Exit Interview
    exit_interview_date = models.DateField(null=True, blank=True)
    exit_interview_by = models.ForeignKey(
        'accounts.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='exit_interviews'
    )
    interview_summary = models.TextField(blank=True)
    
    # Clearance
    clearance_items = models.JSONField(default=list)
    # [{item: str, cleared: bool, cleared_by: str, date: date}]
    
    # Handover
    handover_to = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='handed_over_to'
    )
    handover_completed = models.BooleanField(default=False)
    
    # Final Settlement
    final_salary_paid = models.BooleanField(default=False)
    exit_benefits = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status
    STATUS = [
        ('initiated', 'Initiated'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('clearance_in_progress', 'Clearance In Progress'),
        ('cleared', 'Cleared'),
        ('settled', 'Settled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='initiated')
    
    created_at = models.DateTimeField(auto_now_add=True)


# ==================== PARENT PORTAL ====================

class ParentAccount(models.Model):
    """Parent/Guardian portal access."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Link to student
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE, related_name='parent_accounts')
    
    # Parent Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    
    # Relationship
    RELATIONSHIPS = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
        ('sponsor', 'Sponsor'),
    ]
    relationship = models.CharField(max_length=20, choices=RELATIONSHIPS)
    
    # Access
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    
    # Permissions
    can_view_fees = models.BooleanField(default=True)
    can_view_results = models.BooleanField(default=True)
    can_view_attendance = models.BooleanField(default=True)
    can_make_payments = models.BooleanField(default=True)
    
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)