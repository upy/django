from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .enums import PostStatuses
from .models import Company, Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name", "slug")
    list_display = ("name", "slug")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ("company__name", "company__slug", "position", "slug", "location")
    list_display = ("company", "slug", "position", "status", "is_featured", "location")
    list_filter = (
        "status",
        "type",
    )
    autocomplete_fields = ("tags",)

    def make_approved(self, request, queryset):
        queryset.update(status=PostStatuses.APPROVED)

    make_approved.short_description = _("Mark selected posts as approved")

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)

    make_featured.short_description = _("Mark selected posts as featured")

    def make_nonfeatured(self, request, queryset):
        queryset.update(is_featured=False)

    make_nonfeatured.short_description = _("Mark selected posts as non featured")


class PostAdminInline(admin.StackedInline):
    model = Post


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = (
        "slug",
        "name",
        "email",
    )
    list_display = (
        "name",
        "slug",
        "email",
        "www",
        "twitter",
        "linkedin",
    )

    inlines = [
        PostAdminInline,
    ]
