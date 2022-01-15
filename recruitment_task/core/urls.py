from django.urls import path, include
from core import views

urlpatterns = [
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("projects/<int:pk>/", views.ProjectDetailsView.as_view(),
         name="project-details"),
    path("projects/<int:pk>/matches", views.ProjectMatchingInvestorsView.as_view(),
         name="project-matching-investors"),
    path("investors/", views.InvestorsView.as_view(), name="investors"),
    path("investors/<int:pk>/", views.InvestorDetailsView.as_view(),
         name="investor-details"),
    path("investors/<int:pk>/matches", views.InvestorMatchingProjectsView.as_view(),
         name='investor-matching-projects'),
    path("investors/<int:pk>/invest/<int:project_id>/",
         views.InvestIntoProject.as_view(), name="invest-into-project"),
    path('__debug__/', include('debug_toolbar.urls')),
]
