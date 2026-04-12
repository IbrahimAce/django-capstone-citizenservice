from django import forms
from .models import ServiceRequest, ServiceCategory


class ServiceRequestForm(forms.ModelForm):
    """
    Form for citizens submitting a new service request.
    Only exposes what the citizen should fill in — status, officer, notes
    are intentionally excluded and set by the server or officer later.
    """

    class Meta:
        model = ServiceRequest
        fields = ['category', 'title', 'description', 'priority']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 text-sm'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Brief title for your request',
                'class': 'w-full border border-gray-300 rounded-lg p-2 text-sm'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe what you need in detail...',
                'rows': 4,
                'class': 'w-full border border-gray-300 rounded-lg p-2 text-sm'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 text-sm'
            }),
        }
