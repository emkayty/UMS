"""
from django.shortcuts import get_object_or_404
from django.utils import timezone
ICT, Sports, Clinic, Security APIs
"""

from ninja import Router, Schema
from typing import List, Optional

router = Router(tags=['ICT_Sports'])


# === ICT Schemas ===
class ITAssetSchema(Schema):
    id: str
    asset_tag: str
    name: str
    asset_type: str
    status: str


class TicketSchema(Schema):
    id: str
    title: str
    category: str
    priority: str
    status: str


class TicketCreateSchema(Schema):
    title: str
    description: str
    category: str
    priority: str = 'medium'


class EventSchema(Schema):
    id: str
    title: str
    event_type: str
    start_date: str
    venue: str


# === ICT APIs ===
@router.get('/assets')
def list_assets(request):
    """List IT assets."""
    from apps.institution.ict import ITAsset
    
    assets = ITAsset.objects.all()
    
    return [
        {
            'id': str(a.id),
            'tag': a.asset_tag,
            'name': a.name,
            'type': a.asset_type,
            'status': a.status
        }
        for a in assets
    ]


@router.get('/assets/{id}')
def get_asset(request, id: str):
    """Get asset details."""
    from apps.institution.ict import ITAsset
    
    asset = get_object_or_404(ITAsset, id=id)
    
    return {
        'id': str(asset.id),
        'tag': asset.asset_tag,
        'name': asset.name,
        'serial': asset.serial_number,
        'status': asset.status,
        'assigned': asset.assigned_to.get_full_name() if asset.assigned_to else None
    }


@router.post('/assets')
def create_asset(request, data: ITAssetSchema):
    """Create IT asset."""
    from apps.institution.ict import ITAsset
    import uuid
    
    asset = ITAsset.objects.create(
        asset_tag=f"IT{uuid.uuid4().hex[:6].upper()}",
        name=data.name,
        asset_type=data.asset_type
    )
    
    return {'success': True, 'id': str(asset.id)}


@router.get('/tickets')
def list_tickets(request):
    """List support tickets."""
    from apps.institution.ict import ITSupportTicket
    
    tickets = ITSupportTicket.objects.all().order_by('-created_at')
    
    return [
        {
            'id': str(t.id),
            'title': t.title,
            'category': t.category,
            'priority': t.priority,
            'status': t.status
        }
        for t in tickets
    ]


@router.post('/tickets')
def create_ticket(request, data: TicketCreateSchema):
    """Create support ticket."""
    from apps.institution.ict import ITSupportTicket
    
    ticket = ITSupportTicket.objects.create(
        reporter=request.user,
        title=data.title,
        description=data.description,
        category=data.category,
        priority=data.priority
    )
    
    return {'success': True, 'id': str(ticket.id)}


@router.post('/tickets/{id}/assign')
def assign_ticket(request, id: str):
    """Assign ticket to staff."""
    from apps.institution.ict import ITSupportTicket
    
    ticket = get_object_or_404(ITSupportTicket, id=id)
    ticket.assigned_to = request.user
    ticket.status = 'in_progress'
    ticket.save()
    
    return {'success': True}


@router.post('/tickets/{id}/resolve')
def resolve_ticket(request, id: str, resolution: str):
    """Resolve ticket."""
    from apps.institution.ict import ITSupportTicket
    
    ticket = get_object_or_404(ITSupportTicket, id=id)
    ticket.resolution = resolution
    ticket.status = 'resolved'
    ticket.resolved_at = timezone.now()
    ticket.save()
    
    return {'success': True}


# === Events ===
@router.get('/events')
def list_events(request):
    """List events."""
    from apps.institution.ict import Event
    
    events = Event.objects.all().order_by('start_date')
    
    return [
        {
            'id': str(e.id),
            'title': e.title,
            'type': e.event_type,
            'start': str(e.start_date),
            'venue': e.venue
        }
        for e in events
    ]


@router.post('/events')
def create_event(request, data: EventSchema):
    """Create event."""
    from apps.institution.ict import Event
    
    event = Event.objects.create(
        title=data.title,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
        venue=data.venue,
        event_type=data.event_type,
        created_by=request.user
    )
    
    return {'success': True, 'id': str(event.id)}


# === Sports APIs ===
@router.get('/facilities')
def list_sports_facilities(request):
    """List sports facilities."""
    from apps.institution.sports import SportsFacility
    
    facilities = SportsFacility.objects.filter(is_active=True)
    
    return [
        {
            'id': str(f.id),
            'name': f.name,
            'type': f.facility_type,
            'capacity': f.capacity
        }
        for f in facilities
    ]


@router.get('/teams')
def list_teams(request):
    """List sports teams."""
    from apps.institution.sports import SportsTeam
    
    teams = SportsTeam.objects.all()
    
    return [
        {
            'id': str(t.id),
            'name': t.name,
            'sport': t.game_type,
            'coach': t.coach.user.get_full_name() if t.coach and t.coach.user else None
        }
        for t in teams
    ]


@router.get('/teams/{id}/members')
def get_team_members(request, id: str):
    """Get team members."""
    from apps.institution.sports import TeamMember
    
    members = TeamMember.objects.filter(team_id=id)
    
    return [
        {
            'student': m.student.user.get_full_name() if m.student and m.student.user else None,
            'role': m.role,
            'jersey': m.jersey_number
        }
        for m in members
    ]


# === Clinic APIs ===
@router.get('/clinic')
def list_clinic_records(request):
    """List clinic records."""
    from apps.institution.sports import ClinicRecord
    
    records = ClinicRecord.objects.all().order_by('-visit_date')
    
    return [
        {
            'id': str(r.id),
            'student': r.student.user.get_full_name() if r.student and r.student.user else None,
            'complaint': r.complaint,
            'diagnosis': r.diagnosis
        }
        for r in records
    ]


# === Security APIs ===
@router.get('/incidents')
def list_security_incidents(request):
    """List security incidents."""
    from apps.institution.sports import SecurityIncident
    
    incidents = SecurityIncident.objects.all().order_by('-incident_date')
    
    return [
        {
            'id': str(i.id),
            'type': i.incident_type,
            'location': i.location,
            'status': i.status
        }
        for i in incidents
    ]


@router.post('/incidents')
def report_incident(request, data: dict):
    """Report security incident."""
    from apps.institution.sports import SecurityIncident
    
    incident = SecurityIncident.objects.create(
        incident_date=data.get('date'),
        incident_time=data.get('time'),
        incident_type=data.get('type'),
        description=data.get('description'),
        location=data.get('location'),
        reported_by=request.user
    )
    
    return {'success': True, 'id': str(incident.id)}


@router.get('/visitors')
def list_visitors(request):
    """List visitors."""
    from apps.institution.sports import VisitorLog
    
    visitors = VisitorLog.objects.all().order_by('-entry_time')
    
    return [
        {
            'id': str(v.id),
            'visitor': v.visitor_name,
            'purpose': v.purpose,
            'host': v.host.get_full_name() if v.host else None
        }
        for v in visitors
    ]


@router.get('/visitors/checkin')
def visitor_checkin(request):
    """Active visitor passes."""
    from apps.institution.sports import VisitorLog
    
    visitors = VisitorLog.objects.filter(exit_time__isnull=True)
    
    return [{'id': str(v.id), 'visitor': v.visitor_name, 'purpose': v.purpose} for v in visitors]


# === QA & Ethics ===
@router.get('/qa')
def list_qa(request):
    """List quality assurance."""
    from apps.institution.sports import QualityAssurance
    
    qa = QualityAssurance.objects.all().order_by('-date')
    
    return [
        {
            'id': str(q.id),
            'title': q.title,
            'type': q.qa_type,
            'body': q.body,
            'status': q.status
        }
        for q in qa
    ]


@router.get('/ethics')
def list_ethics(request):
    """List ethics applications."""
    from apps.institution.sports import ResearchEthics
    
    ethics = ResearchEthics.objects.all().order_by('-created_at')
    
    return [
        {
            'id': str(e.id),
            'researcher': e.researcher.user.get_full_name() if e.researcher and e.researcher.user else None,
            'title': e.title,
            'status': e.status
        }
        for e in ethics
    ]