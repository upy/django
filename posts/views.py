from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .enums import PostStatuses
from .filters import PostFilter, PostSearchFilter
from .models import Post
from .serializers import (
    PostSerializer,
    LocationSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status=PostStatuses.APPROVED.value)
    serializer_class = PostSerializer
    filterset_class = PostFilter

    @action(detail=False, methods=["get"])
    def locations(self, request):
        queryset = super().get_queryset()
        queryset = (
            queryset.values("location")
                .annotate(count=Count("location"))
                .order_by("-count")
        )
        data = LocationSerializer(queryset, many=True).data
        return Response(data=data)


class PostSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(status=PostStatuses.APPROVED.value)
    serializer_class = PostSerializer
    filterset_class = PostSearchFilter

