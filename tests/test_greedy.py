from django.test import TestCase
from flexcity_techtest.activation.business.greedy import get_assets_greedy
from flexcity_techtest.activation.models import Asset


class GreedyAssetSelectionTests(TestCase):
    def test_greedy_basic_selection(self):
        a1 = Asset.objects.create(
            code="A1", name="Asset 1", volume=10, activation_cost=100
        )
        a2 = Asset.objects.create(
            code="A2", name="Asset 2", volume=20, activation_cost=150
        )
        a3 = Asset.objects.create(
            code="A3", name="Asset 3", volume=5, activation_cost=50
        )
        assets = Asset.objects.all()
        selected = get_assets_greedy(assets, 15)
        codes = [a.code for a in selected]
        self.assertIn("A3", codes)
        self.assertIn("A1", codes)
        self.assertGreaterEqual(sum(a.volume for a in selected), 15)

    def test_greedy_overflow_removal(self):
        a1 = Asset.objects.create(
            code="A1", name="Asset 1", volume=5, activation_cost=10
        )
        a2 = Asset.objects.create(
            code="A2", name="Asset 2", volume=10, activation_cost=100
        )
        a3 = Asset.objects.create(
            code="A3", name="Asset 3", volume=10, activation_cost=150
        )
        assets = Asset.objects.all()
        selected = get_assets_greedy(assets, 20)
        self.assertNotIn(a1, selected)
        self.assertIn(a2, selected)
        self.assertIn(a3, selected)
        self.assertGreaterEqual(sum(a.volume for a in selected), 20)

    def test_greedy_compute_usefull_of_rate(self):
        # Even though A2 has a better cost/volume ratio, 
        # A1 should be selected because it has a better cost/useful volume ratio (10/10 vs 11/20)
        a1 = Asset.objects.create(
            code="A1", name="Asset 1", volume=10, activation_cost=10
        )
        a2 = Asset.objects.create(
            code="A2", name="Asset 2", volume=20, activation_cost=11
        )
        assets = Asset.objects.all()
        selected = get_assets_greedy(assets, 10)
        self.assertIn(a1, selected)
        self.assertNotIn(a2, selected)
        self.assertGreaterEqual(sum(a.volume for a in selected), 10)

    def test_greedy_compute_usefull_of_rate_with_already_filled(self):
        # a1 has the best ration and should be selected first
        # then a3 should be selected to meet the required volume
        # even though a2 has a better cost/volume ratio, it should not be selected its useful ratio is worse than a3
        a1 = Asset.objects.create(
            code="A1", name="Asset 1", volume=10, activation_cost=1
        )
        a2 = Asset.objects.create(
            code="A2", name="Asset 2", volume=20, activation_cost=11
        )
        a3 = Asset.objects.create(
            code="A3", name="Asset 3", volume=5, activation_cost=10
        )
        assets = Asset.objects.all()
        selected = get_assets_greedy(assets, 15)
        self.assertIn(a1, selected)
        self.assertNotIn(a2, selected)
        self.assertGreaterEqual(sum(a.volume for a in selected), 15)

    def test_greedy_empty_assets(self):
        assets = Asset.objects.none()
        selected = get_assets_greedy(assets, 10)
        self.assertEqual(selected, [])

    def test_greedy_exact_volume(self):
        a1 = Asset.objects.create(
            code="A1", name="Asset 1", volume=10, activation_cost=100
        )
        assets = Asset.objects.all()
        selected = get_assets_greedy(assets, 10)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].code, "A1")
