from django.contrib import admin
from .models import Course, User, Video


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_admin',
                    'date_joined', 'last_login')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'course_type')
    search_fields = ('category', 'title', 'username')


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course_id', 'duration')
    search_fields = ('title',)


admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Video,VideoAdmin)
