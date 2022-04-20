from django.contrib import admin

from apps.resource.models import ResourceItem, ResourceList, ResourceListScanTask


class ResourceListScanTaskInline(admin.StackedInline):
    model = ResourceListScanTask


@admin.register(ResourceList)
class ResourceListAdmin(admin.ModelAdmin):
    inlines = [
        ResourceListScanTaskInline
    ]


@admin.register(ResourceItem)
class ResourceItemAdmin(admin.ModelAdmin):
    pass
