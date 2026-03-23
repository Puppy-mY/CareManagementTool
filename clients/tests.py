from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Client


class ClientCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass12345")
        self.client.login(username="tester", password="pass12345")

    def test_get_create_form_renders(self):
        url = reverse("client_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "clients/client_form.html")
        # Headings to confirm layout sections exist
        self.assertContains(resp, "基本情報")
        self.assertContains(resp, "介護保険関係")
        self.assertContains(resp, "医療保険関係")
        self.assertContains(resp, "家族情報")

    def test_post_create_minimal_required_fields(self):
        url = reverse("client_create")
        data = {
            "insurance_number": "1234567890",
            "name": "山田 太郎",
            "furigana": "やまだ たろう",
            "birth_date": "1950-01-01",
            "gender": "male",
        }
        resp = self.client.post(url, data)
        # Expect redirect to detail page on success
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Client.objects.filter(insurance_number="1234567890").exists())
