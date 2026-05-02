"""
Grade Moderation Service.
Implements exam grade moderation and scaling.
"""
from decimal import Decimal
from django.db.models import Avg, Max, Min, Count
from apps.learning.models import CourseRegistration, Result


class GradeModerationService:
    """Service for moderating exam grades."""
    
    # Standard boundaries
    SCALES = {
        'percentile': 'Scale based on class percentile',
        'gaussian': 'Normal distribution scaling',
        'fixed': 'Fixed percentage scaling',
        'none': 'No moderation applied',
    }
    
    @classmethod
    def get_course_statistics(cls, course, semester):
        """Get statistics for a course."""
        results = Result.objects.filter(
            registration__course=course,
            registration__semester=semester,
            status='approved'
        )
        
        if not results.exists():
            return None
        
        stats = results.aggregate(
            avg_score=Avg('score'),
            max_score=Max('score'),
            min_score=Min('score'),
            count=Count('id')
        )
        
        # Grade distribution
        grade_dist = {}
        for grade in ['A', 'B', 'C', 'D', 'E', 'F']:
            grade_dist[grade] = results.filter(grade=grade).count()
        
        stats['grade_distribution'] = grade_dist
        return stats
    
    @classmethod
    def apply_percentile_scaling(cls, results, target_mean=65):
        """Apply percentile-based scaling."""
        if not results:
            return results
        
        scores = [r['score'] for r in results]
        current_mean = sum(scores) / len(scores)
        
        # Calculate scaling factor
        if current_mean > 0:
            factor = target_mean / current_mean
        else:
            factor = 1
        
        # Apply with constraints
        scaled = []
        for r in results:
            new_score = min(100, r['score'] * factor)
            new_score = max(0, new_score)
            scaled.append({
                **r,
                'original_score': r['score'],
                'score': round(new_score, 2),
                'moderation_factor': factor
            })
        
        return scaled
    
    @classmethod
    def apply_gaussian_scaling(cls, results, target_mean=65, target_std=15):
        """Apply Gaussian/normal distribution scaling."""
        if not results:
            return results
        
        scores = [r['score'] for r in results]
        n = len(scores)
        
        # Calculate current mean and std
        mean = sum(scores) / n
        variance = sum((x - mean) ** 2 for x in scores) / n
        std = variance ** 0.5
        
        # Don't scale if too small variance
        if std < 5:
            return results
        
        # Standardize, rescale
        scaled = []
        for r in results:
            if std > 0:
                z = (r['score'] - mean) / std
                new_score = target_mean + z * target_std
            else:
                new_score = r['score']
            
            # Constrain
            new_score = min(100, max(0, new_score))
            scaled.append({
                **r,
                'original_score': r['score'],
                'score': round(new_score, 2)
            })
        
        return scaled
    
    @classmethod
    def apply_fixed_scaling(cls, results, percentage=5):
        """Apply fixed percentage increase."""
        factor = 1 + (percentage / 100)
        
        scaled = []
        for r in results:
            new_score = min(100, r['score'] * factor)
            scaled.append({
                **r,
                'original_score': r['score'],
                'score': round(new_score, 2)
            })
        
        return scaled
    
    @classmethod
    def moderate_grades(cls, course, semester, method='percentile', **kwargs):
        """Apply grade moderation to course results."""
        # Get results
        results_data = []
        results = Result.objects.filter(
            registration__course=course,
            registration__semester=semester,
            status='approved'
        )
        
        for result in results:
            results_data.append({
                'id': result.id,
                'score': float(result.score),
                'registration': result.registration,
            })
        
        # Apply selected method
        if method == 'percentile':
            target = kwargs.get('target_mean', 65)
            moderated = cls.apply_percentile_scaling(results_data, target)
        elif method == 'gaussian':
            moderated = cls.apply_gaussian_scaling(results_data)
        elif method == 'fixed':
            moderated = cls.apply_fixed_scaling(
                results_data, 
                kwargs.get('percentage', 5)
            )
        else:
            return results_data
        
        # Save moderated scores
        for m in moderated:
            result = Result.objects.get(id=m['id'])
            result.score = m['score']
            result.is_moderated = True
            result.moderation_method = method
            result.save()
        
        return moderated
    
    @classmethod
    def detect_grade_anomalies(cls, course, semester):
        """Detect unusual grade patterns."""
        results = Result.objects.filter(
            registration__course=course,
            registration__semester=semester
        )
        
        stats = results.aggregate(
            avg=Avg('score'),
            std_dev=Count('score')
        )
        
        anomalies = []
        if stats['avg']:
            mean = stats['avg']
            for result in results:
                deviation = abs(result.score - mean)
                # Flag if > 2 std devs (simplified)
                if deviation > 30:
                    anomalies.append({
                        'student': str(result.registration.student),
                        'score': result.score,
                        'deviation': deviation
                    })
        
        return anomalies


def get_default_moderation_method(course):
    """Get recommended moderation method."""
    # Could be configured per course/programme
    return 'percentile'
