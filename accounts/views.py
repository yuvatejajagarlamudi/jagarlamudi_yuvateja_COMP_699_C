from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm, LoginForm
from .models import Resident, MunicipalStaff, AdminProfile
from tickets.models import Ticket


# ------------------ REGISTER ------------------ #

def register_view(request):
    form = UserRegisterForm()

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            role = form.cleaned_data["role"]

            # Create role entry
            if role == "resident":
                Resident.objects.create(user=user)
            elif role == "staff":
                MunicipalStaff.objects.create(user=user, staff_level="junior")

            messages.success(request, "Account created successfully.")
            return redirect("accounts:login")

    return render(request, "accounts/register.html", {"form": form})


# ------------------ LOGIN ------------------ #

def login_view(request):
    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)

                # Redirect based on role
                if hasattr(user, "adminprofile"):
                    return redirect("accounts:admin_dashboard")

                if hasattr(user, "municipalstaff"):
                    return redirect("accounts:staff_dashboard")

                if hasattr(user, "resident"):
                    return redirect("accounts:resident_dashboard")

                # Fallback (rare)
                messages.error(request, "Your user account has no role assigned.")
                return redirect("accounts:login")

    return render(request, "accounts/login.html", {"form": form})


# ------------------ LOGOUT ------------------ #

def logout_view(request):
    logout(request)
    return redirect("home")


# ------------------ DASHBOARDS ------------------ #

@login_required
def resident_dashboard(request):
    """
    Only residents can view this dashboard.
    """
    user = request.user

    if not hasattr(user, "resident"):
        messages.error(request, "You are not a resident. Access denied.")
        return redirect("home")

    tickets = Ticket.objects.filter(resident=user.resident)

    return render(request, "accounts/resident_dashboard.html", {
        "tickets": tickets
    })


@login_required
def staff_dashboard(request):
    """
    Staff dashboard – only staff can access.
    """
    user = request.user

    if not hasattr(user, "municipalstaff"):
        messages.error(request, "You are not municipal staff. Access denied.")
        return redirect("home")

    staff = user.municipalstaff
    assigned = Ticket.objects.filter(assigned_staff=staff)

    return render(request, "accounts/staff_dashboard.html", {
        "assigned_tickets": assigned
    })


@login_required
def admin_dashboard(request):
    """
    Admin dashboard – only admin can access.
    """
    user = request.user

    if not hasattr(user, "adminprofile"):
        messages.error(request, "You are not an admin. Access denied.")
        return redirect("home")

    return render(request, "accounts/admin_dashboard.html", {
        "total_tickets": Ticket.objects.count(),
        "pending": Ticket.objects.filter(status="submitted").count(),
        "resolved": Ticket.objects.filter(status="resolved").count(),
        "overdue": Ticket.objects.filter(status="resolved").count(),
        "staff_count": MunicipalStaff.objects.count(),
        "resident_count": Resident.objects.count(),
    })
