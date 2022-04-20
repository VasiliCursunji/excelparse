from django.contrib import admin

from apps.companies_11736.models import Company, ChangeLog


class ChangeLogInline(admin.StackedInline):
    model = ChangeLog


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [ChangeLogInline, ]
    search_fields = ['idno', 'name']


@admin.register(ChangeLog)
class ChangeLogAdmin(admin.ModelAdmin):
    pass
