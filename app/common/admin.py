from django.contrib import admin

from app.common.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'dob')
    list_display = ('get_user',)

    def get_user(self, obj):
        return "[%s] %s" % (obj.user.id, obj.user.email)

    get_user.short_description = 'User'

admin.site.register(UserProfile, UserProfileAdmin)