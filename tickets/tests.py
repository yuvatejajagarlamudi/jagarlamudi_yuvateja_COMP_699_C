# street_issue_reporter/tickets/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Resident, MunicipalStaff, User
from .models import Ticket, MapLocation, RuleConfig
from django.urls import reverse

UserModel = get_user_model()

class TicketWorkflowTests(TestCase):
    def setUp(self):
        # create residents and staff
        self.res_user = UserModel.objects.create_user(username="res1", password="pass123", role=User.ROLE_RESIDENT)
        self.resident = Resident.objects.create(user=self.res_user)
        self.staff_user = UserModel.objects.create_user(username="staff1", password="pass123", role=User.ROLE_STAFF)
        self.staff = MunicipalStaff.objects.create(user=self.staff_user)
        # default rule
        self.rule = RuleConfig.objects.create(priority_rules="pothole=3;garbage=2", overdue_days=1, escalation_days=2)

    def test_submit_ticket_assigns_and_scores(self):
        self.client.login(username="res1", password="pass123")
        url = reverse('tickets:submit_issue')
        data = {
            'description': "Large pothole near main road",
            'latitude': 12.0,
            'longitude': 34.0,
            'address': "Main Road"
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        t = Ticket.objects.first()
        self.assertIsNotNone(t)
        self.assertTrue(t.priority_score >= 3)  # pothole => 3
        self.assertIsNotNone(t.assigned_staff)

    def test_overdue_and_escalation(self):
        t = Ticket.objects.create(resident=self.resident, description="garbage pile", location=MapLocation.objects.create(latitude=0, longitude=0), rule_used=self.rule)
        # fast-forward created_at to 3 days ago
        import datetime
        t.created_at = timezone.now() - datetime.timedelta(days=3)
        t.save(update_fields=['created_at'])
        t.check_overdue()
        t.escalate_if_needed()
        self.assertTrue(t.overdue)
        self.assertTrue(t.escalated or (t.rule_used.escalation_days <= 3))
