from django.urls import path
from job import views

urlpatterns = [
    path('featured/jobs/', views.MainFeaturedJobs.as_view()),
    path('specialization/', views.MainSpecializationList.as_view()),

    path('featured/companies/', views.MainFeaturedCompanies.as_view()),
    path('job-list/', views.JobListAPIView.as_view()),
]


