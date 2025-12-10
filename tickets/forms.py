from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "location", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Short descriptive title", "class": "input"}),
            "description": forms.Textarea(attrs={"placeholder": "Describe the issue with details", "rows": 6, "class": "textarea"}),
            "location": forms.TextInput(attrs={"placeholder": "Street / neighborhood / landmark", "class": "input"}),
        }


class AssignForm(forms.Form):
    staff_id = forms.IntegerField(widget=forms.HiddenInput())


class TicketStatusForm(forms.Form):
    status = forms.ChoiceField(choices=Ticket.STATUS_CHOICES)
