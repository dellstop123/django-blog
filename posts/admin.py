from django.contrib import admin
from .models import Post, Images,AddUserProfile
# Register your models here.


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]
    # list_editable = ["title"]

    class Meta:
        model = Post
        # ordering = ["-timestamp", "-updated"]


class ImagesAdmin(admin.ModelAdmin):
    list_display_image = ['post', 'image']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['bio', 'image']
    
    
admin.site.register(Post, PostModelAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(AddUserProfile, ProfileAdmin)
