from django.test import TestCase
from django.utils import timezone

from core.businesslogic.investing import invest_into_project
from core.businesslogic.errors import CannotInvestIntoProjectException
from core.models import Project, Investor


class InvestingIntoProjectTestCase(TestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(
            name='test_name', description='test', amount=500,
            delivery_date=timezone.now() + timezone.timedelta(days=21)
        )
        self.investor = Investor.objects.create(
            name='test_name', total_amount=100000, individual_amount=500,
            project_delivery_deadline=timezone.now() + timezone.timedelta(days=21)
        )

    def test_invest_into_project_success(self) -> None:
        invest_into_project(self.investor, self.project)
        expected_remaining_amount = self.investor.total_amount - self.project.amount
        self.assertEqual(self.investor.remaining_amount,
                         expected_remaining_amount)

        self.assertEqual(self.project.funded_by, self.investor)

    def test_invest_into_project_with_not_enought_amount_raise_erorr(self) -> None:
        self.investor.individual_amount = self.project.amount - 1
        with self.assertRaises(CannotInvestIntoProjectException):
            invest_into_project(self.investor, self.project)

    def test_invest_into_project_with_exceeded_deadline_raise_error(self) -> None:
        self.investor.project_delivery_deadline = self.project.delivery_date - \
            timezone.timedelta(1)
        with self.assertRaises(CannotInvestIntoProjectException):
            invest_into_project(self.investor, self.project)

    def test_invest_into_already_funded_project_raise_error(self) -> None:
        self.project.funded_by = self.investor
        self.project.funded = True
        with self.assertRaises(CannotInvestIntoProjectException):
            invest_into_project(self.investor, self.project)
