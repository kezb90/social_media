from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MyBaseModel(models.Model):
    is_active = models.BooleanField(verbose_name="Is active", default=True)
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

    """
    This method uses the follow_requests_sent reverse relation
    to filter profiles that have sent follow requests to the
    current profile (self). The distinct() method ensures that
    each sender profile is included only once in the result.
    """

    def follow_request_senders(self):
        return Profile.objects.filter(follow_requests_sent__to_user=self).distinct()

    def has_follow_requests(self):
        return FollowRequest.objects.filter(to_user=self).exists()

    """
    The followers method uses the reverse relation followings
    to filter profiles that are following the current profile (self).
    """

    # Get followers
    @property
    def followers(self):
        return Profile.objects.filter(followings__following=self)

    """
    The followings method uses the reverse relation followers
    to filter profiles that the current profile is following.
    """

    # Get followings
    @property
    def followings(self):
        return Profile.objects.filter(followers__follower=self)


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


class FollowRequest(models.Model):
    from_user = models.ForeignKey(
        Profile, related_name="follow_requests_sent", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        Profile, related_name="follow_requests_received", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["from_user", "to_user"]

    def __str__(self):
        return f"{self.from_user.username} wants to follow {self.to_user.username}"


class ViewProfile(models.Model):
    viewer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="viewers_of_profile"
    )
    viewed_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="viewed_profile"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.viewer.username} viewed {self.viewed_profile.username} on {self.timestamp}"
