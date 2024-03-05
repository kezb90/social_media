from django.db import models
from accounts.models import Profile


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        Profile, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} - {self.timestamp}"


class MedaiMessageBaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="media created", auto_now_add=True)
    caption = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ("-pk",)

    def __str__(self):
        raise NotImplementedError("Implement __str__ method!")


class Image(MedaiMessageBaseModel):
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, related_name="image"
    )
    image = models.ImageField(upload_to="Message/Media/image/")

    def __str__(self):
        return f"image sent by {self.message.sender.username} to {self.message.receiver.username} in {self.created_at}"


class Video(MedaiMessageBaseModel):
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, related_name="video"
    )
    video_file = models.FileField(upload_to="Post/Media/viedo/")

    def __str__(self):
        return f"video sent by {self.message.sender.username} to {self.message.receiver.username} in {self.created_at}"


class Audio(MedaiMessageBaseModel):
    message = models.OneToOneField(
        Message, on_delete=models.CASCADE, related_name="audio"
    )
    audio_file = models.FileField(upload_to="Post/Media/audio/")

    def __str__(self):
        return f"audio sent by {self.message.sender.username} to {self.message.receiver.username} in {self.created_at}"
