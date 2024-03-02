from django.db import models
from django.contrib.auth.models import User
from datetime import date

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


class Profile(MyBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    follower = models.ManyToManyField(User, blank=True, related_name="followers")
    following = models.ManyToManyField(User, blank=True, related_name="followings")
    bio = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )

    @property
    def age(self):
        today = date.today()
        if self.birthday:
            age = (
                today.year
                - self.birthday.year
                - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            )
            return age
        return None

    def get_followers(self):
        followers = self.follower.all()
        return followers

    def get_followings(self):
        followings = self.following.all()
        return followings

    def __str__(self):
        return self.user.username


# class Follow(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     follower = models.ManyToManyField(User,  related_name='followers')
#     following = models.ManyToManyField(User,  related_name='followings')
