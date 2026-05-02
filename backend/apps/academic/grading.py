import uuid
from django.db import models
from apps.accounts.models import User


class GradingPolicy(models.Model):
    """Grading policy with inheritance."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    scale_type = models.CharField(max_length=20)  # british_nigerian, american, custom
    grade_boundaries = models.JSONField(
        default=list,
        help_text='List of grade boundaries [{grade, min, point}]'
    )
    pass_mark = models.IntegerField(default=40)
    max_score = models.IntegerField(default=100)
    cgpa_formula = models.CharField(
        max_length=20, default='standard',
        help_text='Formula for CGPA calculation'
    )
    
    # Inheritance - nullable foreign keys for policy overrides
    faculty = models.ForeignKey(
        'academic.Faculty', on_delete=models.CASCADE, 
        null=True, blank=True, related_name='grading_policies'
    )
    programme = models.ForeignKey(
        'academic.Programme', on_delete=models.CASCADE,
        null=True, blank=True, related_name='grading_policies'
    )
    course = models.ForeignKey(
        'academic.Course', on_delete=models.CASCADE,
        null=True, blank=True, related_name='grading_policies'
    )
    
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'grading_policies'
        ordering = ['-is_default', 'name']

    def __str__(self):
        return self.name

    @classmethod
    def resolve_policy(cls, course_id, programme_id, faculty_id):
        """Resolve effective grading policy with inheritance."""
        # Check course-level policy first
        policy = cls.objects.filter(course_id=course_id).first()
        if policy:
            return policy
        
        # Then programme-level
        policy = cls.objects.filter(programme_id=programme_id).first()
        if policy:
            return policy
        
        # Then faculty-level
        policy = cls.objects.filter(faculty_id=faculty_id).first()
        if policy:
            return policy
        
        # Finally institution default
        policy = cls.objects.filter(is_default=True).first()
        if not policy:
            # Create default if doesn't exist
            policy = cls.objects.create(
                name='Default',
                scale_type='british_nigerian',
                grade_boundaries=[
                    {'grade': 'A', 'min': 70, 'point': 5.0},
                    {'grade': 'B', 'min': 60, 'point': 4.0},
                    {'grade': 'C', 'min': 50, 'point': 3.0},
                    {'grade': 'D', 'min': 45, 'point': 2.0},
                    {'grade': 'E', 'min': 40, 'point': 1.0},
                    {'grade': 'F', 'min': 0, 'point': 0.0},
                ],
                pass_mark=40,
                is_default=True
            )
        return policy

    def get_grade(self, score):
        """Get grade for a given score."""
        for boundary in sorted(self.grade_boundaries, key=lambda x: x['min'], reverse=True):
            if score >= boundary['min']:
                return boundary
        return self.grade_boundaries[-1]  # Return lowest grade

    def calculate_grade_point(self, score):
        """Calculate grade point for a score."""
        grade = self.get_grade(score)
        return grade.get('point', 0.0)