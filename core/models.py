from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


class Account(AbstractUser):
    first_name = None
    last_name = None

    class Meta:
        ordering = ["username"]
        indexes = [
            models.Index(fields=["username"]),
        ]

    avatar = models.ImageField(upload_to="images/avatars/", null=True, blank=True)

    long_name = models.CharField(max_length=150, null=True, blank=True)
    short_name = models.CharField(max_length=150, null=True, blank=True)

    long_description = models.TextField(null=True, blank=True)
    short_description = models.CharField(max_length=150, null=True, blank=True)

    is_company = models.BooleanField(default=False)

    following = models.ManyToManyField(
        "self", through="Contact", related_name="followers", symmetrical=False
    )

    saved_posts = models.ManyToManyField(
        "Post", through="SavedPost", related_name="saved_by"
    )

    def __str__(self):
        return self.long_name if self.long_name else self.username.title()

    def get_absolute_url(self):
        return reverse("account_detail_view", args=[self.id])


class Post(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    body = models.TextField()

    thumbnail = models.ImageField(upload_to="images/thumbnails/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_public = models.BooleanField(default=False)
    is_job_post = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["-updated_at"]),
        ]

    def __str__(self):
        return self.title + (" (Job)" if self.is_job_post else " (Project)")

    def get_absolute_url(self):
        return reverse("post_detail_view", args=[self.id])


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_report = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["-updated_at"]),
        ]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


class Contact(models.Model):
    from_account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="contact_from_set",
        on_delete=models.CASCADE,
    )
    to_account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="contact_to_set",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_account} follows {self.to_account}"


class SavedPost(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="acount_set",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        "Post",
        related_name="post_set",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.account} saves {self.post}"
