from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudyProgram, Subject, Subsubject

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "nickname", "role", "is_staff", "is_active")
    search_fields = ("email", "nickname")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "nickname", "password", "role")}),
        ("Додаткова інформація", {"fields": ("city", "info", "social_networks", "available_times")}),
        ("Дозволи", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nickname", "password1", "password2", "role", "is_staff", "is_active")}
        ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(StudyProgram)
admin.site.register(Subject)
admin.site.register(Subsubject)
