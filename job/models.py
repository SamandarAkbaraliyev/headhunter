from django.db import models
from django.utils.timezone import now


class CompanyBranch(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=256)
    branch = models.ForeignKey(CompanyBranch, on_delete=models.SET_NULL, null=True)
    logo = models.ImageField(upload_to='logos/', null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=256)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    neighboring_cities = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    code = models.CharField(max_length=256, unique=True)
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class EmploymentType(models.Model):
    title = models.CharField(max_length=256)
    code = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.title


class Specialization(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class SpecializationType(models.Model):
    title = models.CharField(max_length=256)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='specializationtypes')

    def __str__(self):
        return self.title


class WorkSchedule(models.Model):
    title = models.CharField(max_length=256)
    code = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.title


class Job(models.Model):
    title = models.CharField(max_length=256)
    published_at = models.DateTimeField(auto_now_add=True, null=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='jobs')

    employment_type = models.ForeignKey(EmploymentType, on_delete=models.SET_NULL, null=True, related_name='jobs')
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='jobs')

    price_from = models.IntegerField(null=True, blank=True)
    price_to = models.IntegerField(null=True, blank=True)

    specialization_type = models.ForeignKey(SpecializationType, on_delete=models.CASCADE, related_name='jobs')
    work_schedule = models.ForeignKey(WorkSchedule, on_delete=models.SET_NULL, null=True)

    is_featured = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)

    def __str__(self):
        return self.title
