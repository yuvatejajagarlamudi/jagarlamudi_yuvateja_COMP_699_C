from django.db import models
from django.utils import timezone
from django.urls import reverse


class RuleConfig(models.Model):
    """
    Priority rule configuration. Admin can tune these values.
    """
    name = models.CharField(max_length=100, default="Default Rules")
    base_score = models.IntegerField(default=10)
    image_bonus = models.IntegerField(default=5)
    long_description_bonus = models.IntegerField(default=3)
    urgent_keyword_bonus = models.IntegerField(default=10)
    overdue_penalty = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Ticket(models.Model):

    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("cancelled", "Cancelled"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)

    # Relations
    resident = models.ForeignKey(
        "accounts.Resident",
        on_delete=models.CASCADE,
        related_name="tickets",
        null=True,
        blank=True,
    )
    assigned_staff = models.ForeignKey(
        "accounts.MunicipalStaff",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )

    # Status & assignment
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="submitted")
    assignment_date = models.DateTimeField(null=True, blank=True)

    # Priority
    priority_score = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional: due_date
    due_date = models.DateTimeField(null=True, blank=True)

    rule_config = models.ForeignKey(
        RuleConfig,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Rules used for priority calculation."
    )

    class Meta:
        ordering = ["-priority_score", "created_at"]

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"

    def get_absolute_url(self):
        return reverse("tickets:view", args=[self.id])

    # ----------------------------
    # SAFE CREATED_AT VALUE
    # ----------------------------
    @property
    def safe_created_at(self):
        """
        Avoid crashing when created_at is None on initial save.
        """
        return self.created_at or timezone.now()

    # ----------------------------
    # CORRECTED OVERDUE LOGIC
    # ----------------------------
    @property
    def is_overdue(self):
        """
        A ticket is overdue if:
        - due_date exists AND is in the past AND not resolved
        - OR if older than 7 days with no due_date AND not resolved
        """
        if self.status == "resolved":
            return False

        now = timezone.now()

        # When due date is set
        if self.due_date:
            return self.due_date < now

        # When due date is NOT set — fallback rule
        return (now - self.safe_created_at).days >= 7

    # ----------------------------
    # FIXED PRIORITY COMPUTATION
    # ----------------------------
    def compute_priority(self):
        """
        Compute priority using RuleConfig values.
        This version avoids any None-type crashes.
        """
        rule = self.rule_config or RuleConfig.objects.first()
        if not rule:
            rule = RuleConfig.objects.create()

        score = rule.base_score or 0

        # Image bonus
        if self.image:
            score += rule.image_bonus or 0

        # Long description bonus
        if len(self.description or "") > 300:
            score += rule.long_description_bonus or 0

        # Urgent keywords
        text = f"{self.title} {self.description}".lower()
        if "urgent" in text or "asap" in text:
            score += rule.urgent_keyword_bonus or 0

        # Overdue penalty (safe now)
        if self.is_overdue:
            score -= rule.overdue_penalty or 0

        # Prevent negative
        self.priority_score = max(0, int(score))
        return self.priority_score
