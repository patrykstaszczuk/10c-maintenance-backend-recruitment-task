from django.test import TestCase
from django.utils import timezone

from core.models import Project, Investor
from core.businesslogic.matchmaking import (
    get_matching_projects,
    get_matching_investors,
    )
from core.businesslogic.errors import CannotMatchInvestors


class MatchmakingProjectsTestCase(TestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='test_name', description='test', amount=500,
            delivery_date=timezone.now() + timezone.timedelta(days=21)
        )
        self.investor = Investor.objects.create(
            name='test_name', total_amount=100000, individual_amount=500,
            project_delivery_deadline=timezone.now() + timezone.timedelta(days=21)
        )

    def test_get_matching_projects(self) -> None:
        projects = get_matching_projects(self.investor)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].id, self.project.id)

    def test_project_with_exceeded_deadline_not_retrieved(self) -> None:
        self.project.delivery_date += timezone.timedelta(days=1)
        self.project.save()

        projects = get_matching_projects(self.investor)
        self.assertEqual(len(projects), 0)

    def test_already_funded_project_not_retrieved(self) -> None:
        self.project.funded_by = self.investor
        self.project.save()

        projects = get_matching_projects(self.investor)
        self.assertEqual(len(projects), 0)

    def test_projects_with_greater_amount_then_investor_individual_amount_not_retrieved(self) -> None:
        self.project.amount += 10
        self.project.save()
        projects = get_matching_projects(self.investor)
        self.assertEqual(len(projects), 0)

    def test_projects_without_funder_but_funded_in_the_past_not_retrieve(self) -> None:
        self.project.funded = True
        self.project.save()
        projects = get_matching_projects(self.investor)
        self.assertEqual(len(projects), 0)


class MatchmakingInvestorsTestCase(TestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='test_name', description='test', amount=500,
            delivery_date=timezone.now() + timezone.timedelta(days=21)
        )
        self.investor = Investor.objects.create(
            name='test_name', total_amount=100000, individual_amount=500,
            project_delivery_deadline=timezone.now() + timezone.timedelta(days=21)
        )

    def test_get_matching_investors(self) -> None:
        investors = get_matching_investors(self.project)
        self.assertEqual(len(investors), 1)
        self.assertEqual(investors[0].id, self.investor.id)

    def test_matchmaking_investors_when_already_funded_raise_error(self) -> None:
        self.project.funded_by = self.investor
        with self.assertRaises(CannotMatchInvestors):
            get_matching_investors(self.project)

    def test_investors_with_not_enought_individual_amount_not_retrieved(self) -> None:
        self.investor.individual_amount -= 100
        self.investor.save()
        investors = get_matching_investors(self.project)
        self.assertEqual(len(investors), 0)

    def test_investors_with_not_enought_remaining_amount_not_retrieved(self) -> None:
        self.investor.remaining_amount = 0
        self.investor.save()
        investors = get_matching_investors(self.project)
        self.assertEqual(len(investors), 0)

    def test_investors_with_shorter_deadline_not_retrieved(self) -> None:
        self.investor.project_delivery_deadline -= timezone.timedelta(1)
        self.investor.save()
        investors = get_matching_investors(self.project)
        self.assertEqual(len(investors), 0)
