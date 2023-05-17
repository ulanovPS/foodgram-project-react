from django.contrib import admin

from .models import User


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email',)


admin.site.register(User, CustomUserAdmin)
