from django.db import models
from django.contrib.auth.models import User
from accounts.models import MyBaseModel

# Create your models here.


class Post(MyBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    caption = models.TextField()
    is_story = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
class Like(MyBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} mentioned {self.post.title}"
    
class Viewer(MyBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

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
