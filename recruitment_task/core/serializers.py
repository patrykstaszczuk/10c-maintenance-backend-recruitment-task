from rest_framework import serializers

from core.models import Project, Investor
from core.businesslogic.matchmaking import (
    get_matching_investors,
    get_matching_projects,
)
from core.businesslogic.errors import CannotMatchInvestors


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_field = ["funded", "funded_by"]


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = "__all__"
        read_only_fields = ["remaining_amount"]


class ProjectDetailsSerializer(serializers.ModelSerializer):

    matching_investors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["funded", "funded_by"]

    def get_matching_investors(self, instance: Project):
        try:
            return get_matching_investors(
                instance).values_list("id", flat=True)
        except CannotMatchInvestors:
            return []


class InvestorDetailsSerializer(serializers.ModelSerializer):

    matching_projects = serializers.SerializerMethodField()

    class Meta:
        model = Investor
        fields = "__all__"
        read_only_fields = ["remaining_amount"]

    def get_matching_projects(self, instance: Investor):
        return get_matching_projects(instance).values_list("id", flat=True)
