from django.db import models
from django.contrib.auth.models import User
from accounts.models import MyBaseModel
# Create your models here.


class Post(MyBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    caption = models.TextField()
    like = models.ManyToManyField(User, blank=True, related_name='likes')
    mention = models.ManyToManyField(User, blank=True, related_name='mentions')
    view = models.ManyToManyField(User, blank=True, related_name='views')
    
    
    def total_like(self):
        return self.like.count()
    
    def total_view(self):
        return self.view.count()
    
    def mentions(self):
        return self.view.all()
    

    def __str__(self):
        return self.title
    
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