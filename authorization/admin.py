from django.contrib import admin

# Register your models here.
from authorization.models import UserProfile, Subscribe


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subscriber')
    list_display_links = ('id', 'user', 'subscriber')


admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
