from rest_framework import serializers
from job import models


class FeaturedJobsSerializer(serializers.ModelSerializer):
    # openings = serializers.IntegerField()
    district = serializers.StringRelatedField()
    company = serializers.StringRelatedField()

    class Meta:
        model = models.Job
        fields = (
            'id',
            'title',
            'price_from',
            'price_to',
            'company',
            'district',
            # 'openings',
        )


class CompanySerializer(serializers.ModelSerializer):
    vacancy_count = serializers.IntegerField()

    class Meta:
        model = models.Company
        fields = ('id', 'name', 'vacancy_count')


class SpecializationTypeSerializer(serializers.ModelSerializer):
    min_price = serializers.IntegerField()
    max_price = serializers.IntegerField()
    openings = serializers.IntegerField()

    class Meta:
        model = models.SpecializationType
        fields = ('id', 'title', 'min_price', 'max_price', 'openings')


class SpecializationSerializer(serializers.ModelSerializer):
    specializationtypes = SpecializationTypeSerializer(many=True)
    spec_min_price = serializers.IntegerField()
    spec_max_price = serializers.IntegerField()
    openings = serializers.IntegerField()

    class Meta:
        model = models.Specialization
        fields = ('id', 'title', 'specializationtypes', 'spec_min_price',
                  'spec_max_price', 'openings')


class JobSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    experience = serializers.StringRelatedField()

    class Meta:
        model = models.Job
        fields = ('id', 'title', 'price_from', 'price_to', 'company', 'experience', 'is_top')
