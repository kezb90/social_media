from django.db import models
from accounts.models import MyBaseModel, Profile
from content.models import Post


class Comment(MyBaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username} commented  {self.content}"

    class Meta:
        ordering = ["-created_at"]
