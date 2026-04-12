from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import ServiceRequest, ServiceCategory
from .citizen_forms import ServiceRequestForm


def citizen_required(view_func):
    """
    Custom decorator — blocks non-citizens from hitting citizen pages.
    Officers who try to visit /citizen/dashboard/ get bounced to their own portal.
    Stack it on top of @login_required so unauthenticated users hit login first.
    """
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ['citizen']:
            messages.error(request, 'This area is for citizens only.')
            return redirect('officer_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@citizen_required
def citizen_dashboard(request):
    """
    Main landing page after citizen login.
    Shows all their requests with counts per status at the top.
    """
    requests_qs = ServiceRequest.objects.filter(
        citizen=request.user
    ).select_related('category', 'assigned_officer').order_by('-created_at')

    # Status counts for the summary cards at the top of the dashboard
    status_counts = {
        'pending': requests_qs.filter(status='pending').count(),
        'in_review': requests_qs.filter(status='in_review').count(),
        'approved': requests_qs.filter(status='approved').count(),
        'completed': requests_qs.filter(status='completed').count(),
    }

    return render(request, 'citizen/dashboard.html', {
        'service_requests': requests_qs,   # renamed — 'requests' clashes with Django's internal request object
        'status_counts': status_counts,
    })


@citizen_required
def submit_request(request):
    """
    GET  → show the empty form
    POST → validate, save, redirect back to dashboard

    The form only exposes fields a citizen should fill in.
    citizen and status are set server-side — never from user input.
    """
    form = ServiceRequestForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.citizen = request.user
            service_request.status = 'pending'
            service_request.save()
            messages.success(request, 'Your request has been submitted successfully.')
            return redirect('citizen_dashboard')
        else:
            messages.error(request, 'Please fix the errors in the form.')

    return render(request, 'citizen/submit_request.html', {'form': form})


@citizen_required
def request_detail(request, pk):
    """
    Shows a single request with its full audit trail.
    Citizens can only view their own requests — get_object_or_404 handles the 404
    but we also filter by citizen to prevent URL guessing (e.g. /citizen/requests/5/).
    """
    service_request = get_object_or_404(
        ServiceRequest,
        pk=pk,
        citizen=request.user  # This is what stops citizens viewing each other's requests
    )
    return render(request, 'citizen/request_detail.html', {
        'sreq': service_request
    })
