from django.contrib import admin

from .models import Channel, ChannelMessage, ChannelUser, MessageModel


from django.contrib.admin import ModelAdmin, site


class MessageModelAdmin(ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'user__username', 'recipient__username')
    list_display = ('id', 'user', 'recipient', 'timestamp', 'characters')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'timestamp'


class ChannelMessageInline(admin.TabularInline):
    model = ChannelMessage
    extra = 1


class ChannelUserInline(admin.TabularInline):
    model = ChannelUser
    extra = 1


class ChannelAdmin(admin.ModelAdmin):
    inlines = [ChannelUserInline, ChannelMessageInline]

    class Meta:
        model = Channel


admin.site.register(Channel, ChannelAdmin)

admin.site.register(ChannelMessage)

site.register(MessageModel, MessageModelAdmin)
