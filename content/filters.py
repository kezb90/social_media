import django_filters
from .models import PostMedia


class MediaFilter(django_filters.FilterSet):
    class Meta:
        model = PostMedia
        fields = {
            "post__id": ["exact"],  # Example filter for the post's id
            "order": ["exact", "gt", "lt"],  # Example filter for the order
            # Add more fields as needed
        }
