from django.db import models
from accounts.models import MyBaseModel
from accounts.models import Profile

# Create your models here.


class Post(MyBaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    caption = models.TextField()
    likes = models.ManyToManyField(
        Profile, related_name="liked_posts", through="Like")

    def __str__(self):
        return f"{self.title} posted by {self.owner.username}"


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


class Tag(MyBaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} taged {self.post.title}"


class Viewer(MyBaseModel):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False, blank=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=False, blank=False)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} viewed {self.post.title}"


class Image(MyBaseModel):
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="Post/Media/image/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Video(MyBaseModel):
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="Post/Media/viedo/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Audio(MyBaseModel):
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="audios")
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to="Post/Media/audio/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Story(MyBaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    caption = models.TextField()

    def __str__(self):
        return f"{self.title} storied by {self.owner.username}"


class Mention(MyBaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "story")

    def __str__(self):
        return f"{self.user.username} taged {self.story.title}"


class StoryViewer(MyBaseModel):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=False, blank=False)
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, null=False, blank=False)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "story")

    def __str__(self):
        return f"{self.user.username} viewed {self.story.title}"


class StoryImage(MyBaseModel):
    story = models.ForeignKey(
        "Story", on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="Story/Media/image/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class StoryVideo(MyBaseModel):
    sory = models.ForeignKey(
        "Story", on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="Story/Media/viedo/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class StoryAudio(MyBaseModel):
    story = models.ForeignKey(
        "Story", on_delete=models.CASCADE, related_name="audios")
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to="Story/Media/audio/")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
