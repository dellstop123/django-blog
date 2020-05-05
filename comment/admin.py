from django.contrib import admin
from .models import Comment

# Register your models here.
# Register your models here.


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]
    # list_editable = ["title"]

    class Meta:
        model = Comment


admin.site.register(Comment)
