from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema

from .permissions import IsOwnerOrAdmin
from .models import Post
from .serializers import PostSerializer, PostDetailSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    @method_decorator(cache_page(60 * 5)) # 10 minutes
    def list(self, request, *args, **kwargs):
        """
        Cache the list view (GET /posts) for 10 minutes.
        """
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Returns all posts for admins, or only the posts belonging to the authenticated user.
        """
        user = self.request.user
        if user.is_staff:
            return Post.objects.all()
        return Post.objects.filter(user=user)

    @extend_schema(
        responses=PostDetailSerializer,
        description="Retrieve a post along with all its statuses.",
        summary="Post details with statuses"
    )
    @action(detail=True, methods=['get'], permission_classes=[IsOwnerOrAdmin])
    @method_decorator(cache_page(60 * 5)) # 10 minutes
    def status(self, request, pk=None):
        """
        Custom action to retrieve a post along with all its statuses.
        """
        try:
            post = self.get_queryset().get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=404)

        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
