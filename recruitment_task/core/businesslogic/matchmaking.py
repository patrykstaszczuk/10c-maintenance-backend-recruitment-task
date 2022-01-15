from core.models import Investor, Project
from core.businesslogic.errors import CannotMatchInvestors


def get_matching_projects(investor: Investor) -> list[Project]:
    deadline = investor.project_delivery_deadline
    individual_amount = investor.individual_amount
    remaining_amount = investor.remaining_amount
    print('get matching')
    investor_max_amount_per_project = min(remaining_amount, individual_amount)

    return Project.objects.filter(
        funded_by=None,
        funded=False,
        delivery_date__lte=deadline,
        amount__lte=investor_max_amount_per_project,
        )


def get_matching_investors(project: Project) -> list[Investor]:
    amount = project.amount
    funded_by = project.funded_by
    funded = project.funded
    delivery_date = project.delivery_date

    if funded_by is not None or funded:
        raise CannotMatchInvestors(f'Project already funded')

    return Investor.objects.filter(
        individual_amount__gte=amount,
        remaining_amount__gte=amount,
        project_delivery_deadline__gte=delivery_date
    )
