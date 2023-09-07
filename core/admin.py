from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Post, Contact, Comment, SavedPost

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ["username", "long_name", "email", "is_company", "is_staff"]
    list_filter = ['is_company', 'is_staff']
    search_fields = ['username', 'long_name']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "is_company",
                    "email",
                    "avatar",
                    "long_name",
                    "short_name",
                    "short_description",
                    "long_description",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "is_job_post", "is_public", "is_active"]
    list_filter = ['is_job_post', 'is_public', "is_active"]
    search_fields = ['title', 'description', 'body']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "is_report"]
    list_filter = ['is_report']
    search_fields = ['post', 'author']

admin.site.register(Contact)
admin.site.register(SavedPost)
