from django.contrib import admin
from .models import Course, User,Video

class UserAdmin(admin.ModelAdmin):
    list_display=('email', 'username','is_admin','date_joined','last_login')
    search_fields=('email','username')
    readonly_fields=('id','date_joined','last_login')

admin.site.register(User,UserAdmin)
admin.site.register(Course)
admin.site.register(Video)
