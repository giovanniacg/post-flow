from django.db import models
from simple_history.models import HistoricalRecords

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    current_status = models.ForeignKey('status.Status', on_delete=models.CASCADE)
    address = models.ForeignKey('address.Address', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.user} - {self.created_at} - {self.current_status}"

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        PostStatus.objects.create(post=self, status=self.current_status)


class PostStatus(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.ForeignKey('status.Status', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.post} - {self.status}"
