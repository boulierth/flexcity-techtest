from django.test import TestCase
from flexcity_techtest.activation.business.knapsack_solver import get_assets_knapsack_solver
from flexcity_techtest.activation.models import Asset
from unittest.mock import patch, MagicMock

class KnapsackSolverTests(TestCase):
    def test_knapsack_solver_selects_assets(self):
        # Setup assets
        a1 = Asset.objects.create(code="A1", name="Asset 1", volume=10, activation_cost=100)
        a2 = Asset.objects.create(code="A2", name="Asset 2", volume=20, activation_cost=150)
        assets = [a1, a2]

        selected = get_assets_knapsack_solver(assets, 20)
        # Should only return a2
        self.assertEqual(selected, [a2])

    def test_knapsack_solver_selects_none(self):
        a1 = Asset.objects.create(code="A1", name="Asset 1", volume=10, activation_cost=100)
        assets = [a1]

        with self.assertRaises(Exception):
            get_assets_knapsack_solver(assets, 20)

    def test_knapsack_solver_selects_all(self):
        a1 = Asset.objects.create(code="A1", name="Asset 1", volume=10, activation_cost=100)
        a2 = Asset.objects.create(code="A2", name="Asset 2", volume=20, activation_cost=150)
        assets = [a1, a2]

        selected = get_assets_knapsack_solver(assets, 30)
        self.assertEqual(selected, assets)
