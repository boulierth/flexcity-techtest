from django.test import TestCase
from unittest.mock import patch, MagicMock
from flexcity_techtest.activation.business.strategy import get_activated_assets
from flexcity_techtest.activation.models import Asset, Availability
from flexcity_techtest.activation.schemas import ActivationIn
from datetime import date


class StrategyTests(TestCase):
    def setUp(self):
        self.asset1 = Asset.objects.create(
            code="A1", name="Asset 1", volume=10, activation_cost=100
        )
        self.asset2 = Asset.objects.create(
            code="A2", name="Asset 2", volume=20, activation_cost=150
        )
        Availability.objects.create(asset=self.asset1, date=date.today())
        Availability.objects.create(asset=self.asset2, date=date.today())
        self.data = ActivationIn(volume=10, date=date.today())

    @patch("flexcity_techtest.activation.business.strategy.get_assets_greedy")
    def test_greedy_strategy(self, mock_greedy):
        mock_greedy.return_value = [self.asset1]
        result = get_activated_assets(self.data, strategy="greedy")
        self.assertEqual(result, [self.asset1])
        mock_greedy.assert_called_once()

    @patch("flexcity_techtest.activation.business.strategy.get_assets_knapsack_solver")
    def test_knapsack_strategy(self, mock_knapsack):
        mock_knapsack.return_value = [self.asset2]
        result = get_activated_assets(self.data, strategy="knapsack_solver")
        self.assertEqual(result, [self.asset2])
        mock_knapsack.assert_called_once()

    def test_all_strategy(self):
        result = get_activated_assets(self.data, strategy="all")
        self.assertEqual(set(result), {self.asset1, self.asset2})

    def test_not_enough_capacity(self):
        data = ActivationIn(volume=1000, date=date.today())
        with self.assertRaises(Exception) as ctx:
            get_activated_assets(data, strategy="all")
        self.assertIn("Not enough capacity available", str(ctx.exception))

    def test_no_assets_available(self):
        data = ActivationIn(volume=10, date=date(2000, 1, 1))
        with self.assertRaises(Exception) as ctx:
            get_activated_assets(data, strategy="all")
        self.assertIn("Not enough capacity available", str(ctx.exception))
