from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ServiceRequest

def officer_required(view_func):
    """
    Custom decorator — blocks citizens from accessing officer pages.
    """
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ['officer', 'admin']:
            messages.error(request, 'This area is restricted to government officers.')
            return redirect('citizen_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@officer_required
def officer_dashboard(request):
    """
    Shows all requests across the system. 
    select_related prevents database thrashing (N+1 queries).
    """
    requests_qs = ServiceRequest.objects.select_related(
        'citizen', 'category', 'assigned_officer'
    ).order_by('-created_at')

    status_counts = {
        'pending': requests_qs.filter(status='pending').count(),
        'in_review': requests_qs.filter(status='in_review').count(),
        'approved': requests_qs.filter(status='approved').count(),
        'completed': requests_qs.filter(status='completed').count(),
    }

    return render(request, 'officer/dashboard.html', {
        'service_requests': requests_qs,
        'status_counts': status_counts,
    })

@officer_required
def request_detail(request, pk):
    """
    Shows request details and handles form submissions for status/notes updates.
    """
    sreq = get_object_or_404(ServiceRequest, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes')

        if new_status:
            sreq.status = new_status
        if notes is not None:
            sreq.notes = notes

        # Automatically assign the request to the officer processing it
        if sreq.assigned_officer is None and new_status != 'pending':
            sreq.assigned_officer = request.user

        sreq.save()
        messages.success(request, 'Request updated successfully.')
        return redirect('officer_request_detail', pk=sreq.pk)

    return render(request, 'officer/request_detail.html', {
        'sreq': sreq,
        'status_choices': ServiceRequest.STATUS_CHOICES
    })
