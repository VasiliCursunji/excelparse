from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.forms import model_to_dict

from apps.companies_11736.utils import ModelDiffMixin


class BaseModel(models.Model):
    class Meta:
        abstract = True

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


# class LicenseClassification(BaseModel):
#     class Meta:
#         abstract = True
#
#     # ID
#     classification_id = models.CharField(max_length=50)
#     # Denumire
#     name = models.CharField(max_length=255, null=True)
#
#     def __str__(self):
#         return self.classification_id
#
#
# class Licensed(LicenseClassification):
#     pass
#
#
# class Unlicensed(LicenseClassification):
#     # Cod CAEM
#     caem_code = models.CharField(max_length=100, null=True)
#     # (1 - CAEM; 2 - CAEM rev.2)
#     CAEM_VERSION_TYPE = (
#         ('1', 'CAEM'),
#         ('2', 'CAEM rev.2')
#     )
#     # Versiunea CAEM
#     caem_version = models.CharField(max_length=100, null=True, choices=CAEM_VERSION_TYPE)


# class CustomManager(models.Manager):
#     def bulk_update(self, items, fields, **kwargs):
#         super().bulk_update(self, items, fields, **kwargs)
#         for item in items:
#             post_save(instance=item, changes=fields)


class Company(BaseModel):
    class Meta:
        unique_together = [['idno', 'name']]

    # IDNO/ Cod fiscal
    idno = models.CharField(max_length=255, null=True)
    # Data înregistrării
    register_date = models.DateTimeField(null=True)
    # Denumirea completă
    name = models.CharField(max_length=255, null=True)
    # Forma org./jurid.
    organization_form = models.CharField(max_length=255, null=True)
    # Adresa
    address = models.CharField(max_length=255, null=True)
    # Lista conducătorilor
    managers = models.JSONField(null=True)
    # Codul unităţii administrativ-teritoriale (CUATM)
    cuatm = models.CharField(max_length=255, null=True)
    # Lista fondatorilor
    founders = models.JSONField(null=True)
    # Lista beneficiarilor efectivi
    beneficiaries = models.JSONField(null=True)
    # Statutul
    state = models.CharField(max_length=255, null=True)
    # Data lichidării
    liquidation_date = models.DateTimeField(null=True)
    # Genuri de activitate licentiate
    licensed_activities = models.JSONField(null=True)
    # Genuri de activitate nelicentiate
    unlicensed_activities = models.JSONField(null=True)

    def __str__(self):
        return self.name


class ChangeLog(BaseModel):
    # if smth is updated
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_changes')
    change = models.JSONField(null=True)
