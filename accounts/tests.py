from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsSmokeTests(TestCase):
    def test_register_resident_get(self):
        resp = self.client.get(reverse('accounts:register_resident'))
        self.assertEqual(resp.status_code, 200)

    def test_register_staff_get(self):
        resp = self.client.get(reverse('accounts:register_staff'))
        self.assertEqual(resp.status_code, 200)
