from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MyBaseModel(models.Model):
    is_active = models.BooleanField(verbose_name="Is active", default=False)
    created_at = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="date updated", auto_now=True)

    class Meta:
        abstract = True
        ordering = ("pk",)

    def __str__(self):
        raise NotImplementedError("Implement __str__ method!")


class Profile(User):
    is_public = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(verbose_name="date created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="date updated", auto_now=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(
        Profile, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        Profile, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["follower", "following"]

    def __str__(self):
        return f"{self.follower.username} is follower of {self.following.username}"
