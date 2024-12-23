from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser


class TaskStatusView(APIView):
    """
    API View to check the status of a Celery task.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, task_id):
        """
        Get the status and result of a Celery task.
        """
        result = AsyncResult(task_id)

        response_data = {
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None,
        }

        return Response(response_data, status=status.HTTP_200_OK)

