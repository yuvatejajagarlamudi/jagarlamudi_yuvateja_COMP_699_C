# street_issue_reporter/tickets/management/commands/check_overdue.py
from django.core.management.base import BaseCommand
from tickets.models import Ticket, RuleConfig
from django.utils import timezone

class Command(BaseCommand):
    help = "Check tickets for overdue and escalate according to RuleConfig"

    def handle(self, *args, **options):
        rule = RuleConfig.objects.first()
        if not rule:
            self.stdout.write(self.style.WARNING("No RuleConfig found."))
            return

        tickets = Ticket.objects.filter(status=Ticket.STATUS_SUBMITTED)
        checked = 0
        overdue_count = 0
        escalated_count = 0
        for t in tickets:
            checked += 1
            t.rule_used = rule
            t.save(update_fields=['rule_used'])
            if t.check_overdue():
                overdue_count += 1
            if t.escalate_if_needed():
                escalated_count += 1
        self.stdout.write(self.style.SUCCESS(f"Checked {checked} tickets. Overdue: {overdue_count}, Escalated: {escalated_count}"))
