"""
ICT Services System
IT assets, support tickets, network management
"""

from django.db import models
import uuid


class ITAsset(models.Model):
    """IT equipment inventory."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    asset_tag = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    
    TYPE = [
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
        ('printer', 'Printer'),
        ('projector', 'Projector'),
        ('camera', 'Camera'),
        ('router', 'Router'),
        ('switch', 'Network Switch'),
        ('server', 'Server'),
        (' projector', 'Smart Board'),
        ('other', 'Other'),
    ]
    asset_type = models.CharField(max_length=20, choices=TYPE)
    
    # Details
    serial_number = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    
    # Assignment
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='+'
    )
    location = models.CharField(max_length=100, blank=True)
    
    # Status
    STATUS = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('written_off', 'Written Off'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    
    created_at = models.DateTimeField(auto_now_add=True)


class ITSupportTicket(models.Model):
    """IT support tickets."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    reporter = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='it_tickets'
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    CATEGORY = [
        ('hardware', 'Hardware Issue'),
        ('software', 'Software Issue'),
        ('network', 'Network Issue'),
        ('email', 'Email Issue'),
        ('account', 'Account Issue'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY)
    
    PRIORITY = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY, default='medium')
    
    STATUS = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='open')
    
    # Assigned to
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='+'
    )
    
    resolution = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NetworkDevice(models.Model):
    """Network devices."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=20, blank=True)
    
    TYPE = [
        ('router', 'Router'),
        ('switch', 'Switch'),
        ('access_point', 'Access Point'),
        ('firewall', 'Firewall'),
        ('server', 'Server'),
    ]
    device_type = models.CharField(max_length=20, choices=TYPE)
    
    location = models.CharField(max_length=100)
    building = models.CharField(max_length=100)
    
    STATUS = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('maintenance', 'Maintenance'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='online')
    
    last_check = models.DateTimeField(null=True, blank=True)


class EmailAccount(models.Model):
    """Staff email accounts."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE
    )
    
    email = models.EmailField(unique=True)
    
    # Quota
    quota_mb = models.IntegerField(default=5000)
    used_mb = models.IntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SoftwareLicense(models.Model):
    """Software licenses."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    
    license_key = models.CharField(max_length=100, blank=True)
    license_type = models.CharField(max_length=50)
    
    # Counts
    total_licenses = models.IntegerField()
    used_licenses = models.IntegerField(default=0)
    
    expiry_date = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)


class WebsiteContent(models.Model):
    """Website content management."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    content = models.TextField()
    
    POSITION = [
        ('home', 'Home'),
        ('about', 'About'),
        ('contact', 'Contact'),
        ('news', 'News'),
        ('events', 'Events'),
        ('admission', 'Admission'),
        ('footer', 'Footer'),
    ]
    position = models.CharField(max_length=20, choices=POSITION)
    
    is_published = models.BooleanField(default=False)
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL, null=True, related_name='+'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Event(models.Model):
    """Calendar events."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    venue = models.CharField(max_length=100, blank=True)
    
    TYPE = [
        ('academic', 'Academic'),
        ('administrative', 'Administrative'),
        ('social', 'Social'),
        ('sports', 'Sports'),
        ('religious', 'Religious'),
    ]
    event_type = models.CharField(max_length=20, choices=TYPE)
    
    is_public = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL, null=True, related_name='+'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)