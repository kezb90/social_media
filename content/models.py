from django.db import models
from accounts.models import MyBaseModel
from accounts.models import Profile

# Create your models here.


class Post(MyBaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    caption = models.TextField()
    is_story = models.BooleanField(default=False)

    @property
    def mentioned_users(self):
        return Mention.objects.filter(post=self, is_active=True).values_list(
            "user__username", flat=True
        )

    @property
    def total_view_count(self):
        return (
            Viewer.objects.filter(post=self).aggregate(models.Sum("count"))[
                "count__sum"
            ]
            or 0
        )

    @property
    def likes_count(self):
        return Like.objects.filter(post=self).count()

    # Count number of persons who viewed this post
    @property
    def views_count(self):
        return Viewer.objects.filter(post=self).count()

    @property
    def users_access_post_readOnly(self):
        # return Profile.objects.get(user=self.owner).get_followers()
        pass

    # Add user to mentioned list of a specific post
    def add_user_to_mention_list(self, user):
        """
        Add a user to the mentioned users of the post.

        Args:
            user (User): The user to be added.

        Raises:
            ValueError: If the user is already mentioned in the post.
        """
        if Mention.objects.filter(post=self, user=user).exists():
            raise ValueError("User is already mentioned in this post.")
        Mention.objects.create(post=self, user=user, is_active=True)

    def __str__(self):
        return f"{self.title} by {self.owner.username}"


class Like(MyBaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # Get the specific post
    # post = get_object_or_404(Post, id=post_id)
    # Check if the user has liked the post
    # user_has_liked = Like.objects.filter(user=user, post=post).exists()

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


class Mention(MyBaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} mentioned {self.post.title}"


class Viewer(MyBaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} viewed {self.post.title}"


class Image(MyBaseModel):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="Post/Media/image/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Video(MyBaseModel):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="Post/Media/viedo/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Audio(MyBaseModel):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="audios")
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to="Post/Media/audio/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
