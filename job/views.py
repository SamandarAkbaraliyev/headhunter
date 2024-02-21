from job import serializers
from job import models as models
from rest_framework import generics
from job.filters import JobDayModelFilter
from rest_framework.response import Response
from django.db.models import Count, Min, Max, Prefetch, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class MainFeaturedJobs(generics.ListAPIView):
    queryset = models.Job.objects.filter(is_featured=True). \
        select_related('district', 'company')

    serializer_class = serializers.FeaturedJobsSerializer


class MainFeaturedCompanies(generics.ListAPIView):
    queryset = models.Company.objects.filter(is_featured=True)[:12] \
        .annotate(vacancy_count=Count('jobs'))
    serializer_class = serializers.CompanySerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        count_all = models.Job.objects.filter(company__is_featured=True).count()
        return Response({'companies': response.data, 'count': count_all})


class MainSpecializationList(generics.ListAPIView):
    queryset = models.Specialization.objects.all().prefetch_related(
        Prefetch('specializationtypes',
                 queryset=models.SpecializationType.objects.annotate(
                     min_price=Min('jobs__price_from'),
                     max_price=Max('jobs__price_to'),
                     openings=Count('jobs')
                 )
                 )
    ) \
        .annotate(
        spec_min_price=Min('specializationtypes__jobs__price_from'),
        spec_max_price=Max('specializationtypes__jobs__price_to'),
        openings=Count('specializationtypes__jobs')
    )
    serializer_class = serializers.SpecializationSerializer


class JobListAPIView(generics.ListAPIView):
    queryset = models.Job.objects.all().select_related('company', 'experience', 'district',
                                                       'company__district').order_by("-is_top")
    serializer_class = serializers.JobSerializer

    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    filterset_fields = (
        'price_from',
        'price_to',
        'district__name',
        'specialization_type__title',
        'specialization_type__specialization__title',
        'company__branch__id',
        'experience__code',
        'employment_type__code',
        'work_schedule__code',
    )

    search_fields = (
        'title',
        'company__name',
        'specialization_type__title',
        'specialization_type__specialization__title'
    )
    ordering_fields = (
        'published_at',
        'price_to',
        'price_from'
    )
    # filterset_class = JobDayModelFilter


class JobDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Job.objects.all() \
        .select_related(
        'company',
        'company__district',
        'experience',
        'employment_type',
        'district'
    ).prefetch_related('required_skills', )
    serializer_class = serializers.JobDetailSerializer

    # def get_queryset(self):
    #     current_job_pk = self.kwargs.get('pk')
    #     current_job = models.Job.objects.get(id=current_job_pk)
    #     similar_criteria = (
    #         Q(experience=current_job.experience) |
    #         Q(employment_type=current_job.employment_type)
    #     )
    #
    #     qs = super().get_queryset().select_related(
    #         'company',
    #         'company__district',
    #         'experience',
    #         'employment_type',
    #         'district'
    #     ).prefetch_related(
    #         'required_skills',
    #         Prefetch(
    #             'similar_vacancies',
    #             queryset=models.Job.objects.filter(similar_criteria).exclude(id=current_job_pk)))
    #     return qs


class SimilarJobsAPIView(generics.ListAPIView):
    serializer_class = serializers.JobSerializer

    def get_queryset(self):
        current_job_pk = self.kwargs.get('pk')

        current_job = models.Job.objects.prefetch_related('required_skills').get(pk=current_job_pk)
        skills = current_job.required_skills.all()

        similar_jobs = models.Job.objects.filter(required_skills__in=skills,
                                                 specialization_type=current_job.specialization_type).exclude(
            pk=current_job_pk) \
            .select_related('company', 'company__district', 'experience',
                            'employment_type', 'district').distinct()

        return similar_jobs
#
