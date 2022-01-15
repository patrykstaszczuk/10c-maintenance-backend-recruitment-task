from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone

from core.models import Investor, Project


class InvestorDetailsViewTestCase(TestCase):
    @staticmethod
    def _get_url(investor_id: int) -> str:
        return f'/investors/{investor_id}/'

    def setUp(self) -> None:
        self.investor = Investor.objects.create(
            name='test_name', total_amount=100000, individual_amount=500,
            project_delivery_deadline=timezone.now() + timezone.timedelta(days=21)
        )
        self.client = APIClient()

    def test_get(self) -> None:
        url = self._get_url(self.investor.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        investor_data = response.data

        self.assertEqual(investor_data['id'], self.investor.id)
        self.assertEqual(investor_data['name'], self.investor.name)


class ProjectDetailsViewTestCase(TestCase):
    @staticmethod
    def _get_url(investor_id: int) -> str:
        return f'/projects/{investor_id}/'

    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='test_name', description='test', amount=500,
            delivery_date=timezone.now() + timezone.timedelta(days=21)
        )
        self.client = APIClient()

    def test_get(self) -> None:
        url = self._get_url(self.project.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project_data = response.data

        self.assertEqual(project_data['id'], self.project.id)
        self.assertEqual(project_data['name'], self.project.name)


class MatchingProjectsForInvestorsViewTestCase(TestCase):
    @staticmethod
    def _get_url(investor_id: int) -> str:
        return f'/investors/{investor_id}/matches'

    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='test_name', description='test', amount=500,
            delivery_date=timezone.now() + timezone.timedelta(days=21)
        )
        self.investor = Investor.objects.create(
            name='test_name', total_amount=100000, individual_amount=500,
            project_delivery_deadline=timezone.now() + timezone.timedelta(days=21)
        )
        self.client = APIClient()

    def test_list(self) -> None:
        url = self._get_url(self.investor.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        projects_data = response.data

        self.assertEqual(len(projects_data), 1)
        self.assertEqual(projects_data[0]['id'], self.project.id)


class MatchingInvestorsForProjectsViewTestCase(TestCase):
    @staticmethod
    def _get_url(project_id: int) -> str:
        return f'/projects/{project_id}/matches'

    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='test_name', description='test', amount=500,
            delivery_date=timezone.now() + timezone.timedelta(days=21)
        )
        self.investor = Investor.objects.create(
            name='test_name', total_amount=100000, individual_amount=500,
            project_delivery_deadline=timezone.now() + timezone.timedelta(days=21)
        )
        self.client = APIClient()

    def test_list(self) -> None:
        url = self._get_url(self.project.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        investors = response.data

        self.assertEqual(len(investors), 1)
        self.assertEqual(investors[0]['id'], self.investor.id)


class InvestIntoProjectViewTestCase(TestCase):
    @staticmethod
    def _get_url(investor_id: int, project_id: int) -> str:
        return f'/investors/{investor_id}/invest/{project_id}/'

    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='test_name', description='test', amount=500,
            delivery_date=timezone.now() + timezone.timedelta(days=21)
        )
        self.investor = Investor.objects.create(
            name='test_name', total_amount=100000, individual_amount=500,
            project_delivery_deadline=timezone.now() + timezone.timedelta(days=21)
        )
        self.client = APIClient()

    def test_post(self) -> None:
        url = self._get_url(self.investor.id, self.project.id)
        response = self.client.post(url)

        self.investor.refresh_from_db()
        self.project.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.project.funded_by, self.investor)
        self.assertEqual(self.project.funded, True)
        self.assertEqual(
            response.data['remaining_amount'], self.investor.remaining_amount)

    def test_post_with_error(self) -> None:
        self.project.funded = True
        self.project.save()

        url = self._get_url(self.investor.id, self.project.id)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
