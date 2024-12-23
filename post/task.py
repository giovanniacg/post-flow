from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
from status.models import Status
from .models import Post, PostStatus


@shared_task
def update_post_status(post_id):
    """
    Celery task to update the status of a post to the next available status based on the 'order' field.
    """
    try:
        post = Post.objects.get(id=post_id)

        current_status = post.current_status
        next_status = Status.objects.filter(order__gt=current_status.order).order_by('order').first()

        if not next_status:
            return {"success": False, "message": "No next status available."}

        post.current_status = next_status
        post.save()

        PostStatus.objects.create(post=post, status=next_status)

        return {
            "success": True,
            "message": f"Post {post_id} status updated to {next_status.name}.",
        }
    except ObjectDoesNotExist:
        return {
            "success": False,
            "message": f"Post {post_id} does not exist.",
        }
