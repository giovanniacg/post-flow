from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema

from .permissions import IsOwnerOrAdmin
from .models import Post
from .serializers import PostSerializer, PostDetailSerializer
from .task import update_post_status


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    @method_decorator(cache_page(60 * 5)) # 5 minutes
    def list(self, request, *args, **kwargs):
        """
        Cache the list view (GET /posts) for 5 minutes.
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
    @method_decorator(cache_page(60 * 5)) # 5 minutes
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

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def next_status(self, request, pk=None):
        """
        Custom route to asynchronously update the status of a post to the next status.
        """
        try:
            task = update_post_status.delay(pk)

            return Response(
                {"message": f"Task to update status for post {pk} has been triggered.", "task_id": task.id},
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
