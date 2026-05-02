"""
Staff Human Resource Management
Recruitment, promotion, appraisal, leave, qualifications
"""

from django.db import models


class StaffRecruitment(models.Model):
    """Staff recruitment and posting."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Position details
    position_title = models.CharField(max_length=200)
    department = models.ForeignKey(
        'academic.Department', on_delete=models.CASCADE
    )
    
    # Employment type
    EMPLOYMENT_TYPES = [
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('adjunct', 'Adjunct'),
        ('visiting', 'Visiting'),
        ('part_time', 'Part-time'),
        ('tutorial', 'Tutorial'),
    ]
    
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default='permanent')
    
    # Requirements
    qualifications = models.JSONField(default=list)
    # [{qualification: 'PhD', field: 'Computer Science', required: true}]
    
    experience_years = models.IntegerField(default=0)
    specializations = models.JSONField(default=list)
    
    # Recruitment process
    POSTING_STATUS = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offered', 'Offer Made'),
        ('filled', 'Position Filled'),
        ('closed', 'Closed'),
    ]
    
    status = models.CharField(max_length=20, choices=POSTING_STATUS, default='draft')
    
    # Dates
    posting_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    interview_date = models.DateField(null=True, blank=True)
    
    # Salary
    salary_grade = models.CharField(max_length=20, blank=True)
    salary_range = models.CharField(max_length=50, blank=True)
    
    # Applications
    application_count = models.IntegerField(default=0)
    shortlisted_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)


class StaffQualification(models.Model):
    """Staff academic qualifications."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE,
        related_name='qualifications'
    )
    
    QUALIFICATION_TYPES = [
        ('phd', 'PhD'),
        ('mphil', 'MPhil'),
        ('ma', 'MA'),
        ('msc', 'MSc'),
        ('llm', 'LLM'),
        ('mbbs', 'MBBS'),
        ('mbchb', 'MBChB'),
        ('bsc', 'BSc'),
        ('llb', 'LLB'),
        ('hnd', 'HND'),
        ('nd', 'ND'),
        ('pgd', 'PGD'),
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
    ]
    
    qualification_type = models.CharField(max_length=20, choices=QUALIFICATION_TYPES)
    field_of_study = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    
    country = models.CharField(max_length=50)
    year_completed = models.IntegerField()
    
    grade = models.CharField(max_length=50, blank=True)
    thesis_title = models.TextField(blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateField(null=True, blank=True)
    verification_source = models.CharField(max_length=100, blank=True)
    
    # Document upload
    certificate_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)


class StaffAppraisal(models.Model):
    """Annual staff appraisal."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE,
        related_name='appraisals'
    )
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    
    # Appraisal period
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Self appraisal
    self_appraisal = models.TextField()
    achievements = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    professional_development = models.JSONField(default=list)
    
    # HOD appraisal
    hod_rating = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        null=True, blank=True
    )
    hod_comments = models.TextField(blank=True)
    
    Teaching = models.IntegerField(default=0)
    Research = models.IntegerField(default=0)
    Community_Service = models.IntegerField(default=0)
    Administration = models.IntegerField(default=0)
    
    # Overall score
    total_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    # Rating
    RATING_CHOICES = [
        ('excellent', 'Excellent'),
        ('very_good', 'Very Good'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
        ('poor', 'Poor'),
    ]
    
    overall_rating = models.CharField(max_length=20, choices=RATING_CHOICES, blank=True)
    
    # Status
    STATUS = [
        ('pending', 'Pending'),
        ('self_assessment', 'Self Assessment Complete'),
        ('hod_review', 'HOD Review Complete'),
        ('completed', 'Completed'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    
    reviewer = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)


class WorkloadAllocation(models.Model):
    """Staff workload allocation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE,
        related_name='workloads'
    )
    
    session = models.ForeignKey(
        'academic.AcademicSession', on_delete=models.CASCADE
    )
    semester = models.ForeignKey(
        'academic.Semester', on_delete=models.CASCADE
    )
    
    # Teaching allocation
    courses = models.JSONField(default=list)  # [{course_id, level, enrollment}]
    total_courses = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    
    # Other duties
    supervision_hours = models.IntegerField(default=0)
    admin_hours = models.IntegerField(default=0)
    research_hours = models.IntegerField(default=0)
    community_hours = models.IntegerField(default=0)
    
    # Total workload hours
    total_hours = models.IntegerField(default=0)
    
    # Target
    workload_target_hours = models.IntegerField(default=150)
    
    # Status
    STATUS = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    
    approved_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    
    class Meta:
        unique_together = ['staff', 'session', 'semester']


class Publication(models.Model):
    """Staff research publications."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    staff = models.ForeignKey(
        'staff.StaffProfile', on_delete=models.CASCADE,
        related_name='publications'
    )
    
    title = models.CharField(max_length=500)
    authors = models.JSONField(default=list)
    
    # Publication type
    PUB_TYPES = [
        ('journal', 'Journal Article'),
        ('conference', 'Conference Paper'),
        ('book', 'Book'),
        ('chapter', 'Book Chapter'),
        ('technical', 'Technical Report'),
    ]
    
    publication_type = models.CharField(max_length=20, choices=PUB_TYPES)
    
    # Journal details
    journal_name = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    volume = models.CharField(max_length=20, blank=True)
    issue = models.CharField(max_length=20, blank=True)
    pages = models.CharField(max_length=20, blank=True)
    doi = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    
    year = models.IntegerField()
    
    # Indexing
    INDEXING = [
        ('sci', 'SCI/SSCI'),
        ('scopus', 'Scopus'),
        ('google_scholar', 'Google Scholar'),
        ('web_of_science', 'Web of Science'),
        ('local', 'Local'),
    ]
    
    indexed_in = models.JSONField(default=list)
    impact_factor = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    # Citation
    citations = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)