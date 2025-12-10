import csv
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import TicketForm, TicketStatusForm
from .models import Ticket, RuleConfig
from accounts.models import Resident, MunicipalStaff


@login_required
def submit_issue(request):
    """
    Resident submits a new issue ticket.
    """
    if not hasattr(request.user, "resident"):
        messages.error(request, "Only residents can submit issues.")
        return redirect("home")

    form = TicketForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        ticket = form.save(commit=False)
        ticket.resident = request.user.resident
        ticket.rule_config = RuleConfig.objects.first()

        ticket.save()
        ticket.compute_priority()
        ticket.save()

        messages.success(request, "Issue submitted successfully.")
        return redirect("accounts:resident_dashboard")

    return render(request, "tickets/submit_issue.html", {"form": form})


@login_required
def my_issues(request):
    if not hasattr(request.user, "resident"):
        messages.error(request, "Only residents can view this page.")
        return redirect("home")

    tickets = Ticket.objects.filter(resident=request.user.resident).order_by("-created_at")
    return render(request, "tickets/my_issues.html", {"tickets": tickets})


@login_required
def ticket_list(request):
    user = request.user

    if hasattr(user, "municipalstaff"):
        staff = user.municipalstaff
        tickets = Ticket.objects.filter(
            assigned_staff=staff
        ).order_by("-priority_score", "created_at")

    elif hasattr(user, "adminprofile"):
        tickets = Ticket.objects.all().order_by("-priority_score", "created_at")

    else:
        messages.error(request, "You don't have access to this page.")
        return redirect("home")

    return render(request, "tickets/staff_ticket_list.html", {"tickets": tickets})


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user = request.user

    # Resident access control
    if hasattr(user, "resident") and ticket.resident != user.resident:
        messages.error(request, "You do not have permission to view this ticket.")
        return redirect("accounts:resident_dashboard")

    # Ticket status update
    if request.method == "POST":
        form = TicketStatusForm(request.POST)
        if form.is_valid():
            ticket.status = form.cleaned_data["status"]

            if ticket.status == "assigned" and not ticket.assignment_date:
                ticket.assignment_date = timezone.now()

            ticket.save()
            ticket.compute_priority()
            ticket.save()

            messages.success(request, "Ticket status updated.")
            return redirect(ticket.get_absolute_url())
    else:
        form = TicketStatusForm(initial={"status": ticket.status})

    staff_list = None
    if hasattr(user, "adminprofile"):
        staff_list = MunicipalStaff.objects.all()

    return render(request, "tickets/view_ticket.html", {
        "ticket": ticket,
        "form": form,
        "staff_list": staff_list,
    })


# ---------------------------------------------------------
# ⭐⭐⭐ UPDATED ASSIGN TICKET VIEW (GET + POST SUPPORTED)
# ---------------------------------------------------------

@login_required
def assign_ticket(request, ticket_id):
    """
    Admin assigns a ticket to a staff member.
    GET → show selection page
    POST → perform assignment
    """
    if not hasattr(request.user, "adminprofile"):
        messages.error(request, "Only admins can assign tickets.")
        return redirect("home")

    ticket = get_object_or_404(Ticket, id=ticket_id)

    # ✅ GET REQUEST: Load staff selection page
    if request.method == "GET":
        staff_list = MunicipalStaff.objects.all()
        return render(request, "tickets/assign_ticket.html", {
            "ticket": ticket,
            "staff_list": staff_list
        })

    # ✅ POST REQUEST: Assign staff
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        if not staff_id:
            messages.error(request, "Please select a staff member.")
            return redirect(request.path)

        staff = get_object_or_404(MunicipalStaff, id=staff_id)

        ticket.assigned_staff = staff
        ticket.status = "assigned"
        ticket.assignment_date = timezone.now()

        ticket.save()
        ticket.compute_priority()
        ticket.save()

        messages.success(request, f"Ticket assigned to {staff.user.username}.")
        return redirect("tickets:view", ticket_id=ticket.id)

    raise Http404("Invalid request method.")


# ---------------------------------------------------------

@login_required
def change_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user = request.user

    allowed = False
    if hasattr(user, "adminprofile"):
        allowed = True
    if hasattr(user, "municipalstaff") and ticket.assigned_staff == user.municipalstaff:
        allowed = True

    if not allowed:
        messages.error(request, "You are not authorized to change this ticket's status.")
        return redirect("home")

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in dict(Ticket.STATUS_CHOICES):
            ticket.status = new_status
            ticket.save()

            ticket.compute_priority()
            ticket.save()

            messages.success(request, "Ticket status updated.")

            if hasattr(user, "municipalstaff"):
                return redirect("accounts:staff_dashboard")

            return redirect("accounts:admin_dashboard")

    raise Http404("Invalid request")


@login_required
def download_history(request):
    user = request.user

    if hasattr(user, "resident"):
        tickets = Ticket.objects.filter(resident=user.resident).order_by("-created_at")
    elif hasattr(user, "adminprofile"):
        tickets = Ticket.objects.all().order_by("-created_at")
    else:
        messages.error(request, "You don't have permission to download history.")
        return redirect("home")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="ticket_history.csv"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Title", "Status", "Priority", "Location", "Created At", "Assigned Staff"])

    for t in tickets:
        staff_name = t.assigned_staff.user.username if t.assigned_staff else ""
        writer.writerow([
            t.id,
            t.title,
            t.status,
            t.priority_score,
            t.location,
            t.created_at.isoformat(),
            staff_name,
        ])

    return response
