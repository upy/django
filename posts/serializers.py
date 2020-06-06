from django.utils.translation import gettext_lazy as _

from .models import Post, Company, Tag
from rest_framework import serializers


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ("name", "slug", "logo", "www", "twitter", "linkedin")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name", "slug")


class PostSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    post_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "apply_email",
            "apply_url",
            "company",
            "created_at",
            "description",
            "is_featured",
            "location",
            "position",
            "post_url",
            "slug",
            "status",
            "tags",
            "type",
            "updated_at",
        )



class LocationSerializer(serializers.Serializer):
    location = serializers.CharField(label=_("Location"))

    class Meta:
        fields = ("location",)

class CreatePostSerializer(serializers.Serializer):
    company_email = serializers.EmailField(label=_("E-mail"))
    company_linkedin = serializers.URLField(label=_("Linkedin"), allow_blank=True)
    company_name = serializers.CharField(max_length=100, label=_("Company name"))
    company_twitter = serializers.CharField()
