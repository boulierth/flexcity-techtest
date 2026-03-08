
from django.test import TestCase, Client
from flexcity_techtest.activation.models import Asset, Availability
from datetime import date
from unittest.mock import patch

class ApiTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("flexcity_techtest.activation.business.strategy.get_activated_assets")
    def test_activate_endpoint(self, mock_get_activated_assets):
        asset = Asset.objects.create(
            code="TST-00001",
            name="Test Asset",
            volume=10,
            activation_cost=100.0,
        )
        Availability.objects.create(asset=asset, date=date.today())
        mock_get_activated_assets.return_value = [
            {
                "code": "TST-00001",
                "name": "Test Asset",
                "volume": 10,
                "activation_cost": 100.0,
            }
        ]
        payload = {
            "volume": 10,
            "date": str(date.today()),
        }
        response = self.client.post("/api/activate", payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(a["name"] == "Test Asset" for a in response.json()))

    @patch("flexcity_techtest.activation.business.strategy.get_activated_assets")
    def test_activate_endpoint_error(self, mock_get_activated_assets):
        mock_get_activated_assets.side_effect = Exception("Not enough capacity available")
        payload = {
            "volume": 10,
            "date": str(date.today()),
        }
        response = self.client.post("/api/activate", payload, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Not enough capacity available")

    def test_available_capacity_today(self):
        asset = Asset.objects.create(
            code="TST-00002",
            name="Test Asset 2",
            volume=20,
            activation_cost=200.0,
        )
        Availability.objects.create(asset=asset, date=date.today())
        response = self.client.get("/api/available-capacity?date=today")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_capacity"], 20)
        self.assertEqual(data["total_cost"], 200.0)

    def test_available_capacity_invalid_date(self):
        response = self.client.get("/api/available-capacity?date=invalid")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date format", response.json()["detail"])
