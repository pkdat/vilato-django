from typing import Any
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import Account, Post, Comment


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Account
        fields = ['username', 'email']
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Tài khoản'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Mật khẩu'
        self.fields['password2'].label = 'Xác nhận mật khẩu'

class LoginForm(AuthenticationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Tài khoản'
        self.fields['password'].label = 'Mật khẩu'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "thumbnail", "body", "is_public"]
        widgets = {
            "title": forms.TextInput(),
            "body": forms.Textarea(),
        }
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Tiêu đề'
        self.fields['description'].label = 'Mô tả'
        self.fields['thumbnail'].label = 'Ảnh minh họa'
        self.fields['body'].label = 'Nội dung'
        self.fields['is_public'].label = 'Công khai'
        self.fields['description'].widget.attrs['placeholder'] = 'Hỗ trợ Markdown'
        self.fields['body'].widget.attrs['placeholder'] = 'Hỗ trợ Markdown'

class CompanyPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "thumbnail", "body", "is_job_post", "is_public"]
        widgets = {
            "title": forms.TextInput(),
            "body": forms.Textarea(),
        }
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Tiêu đề'
        self.fields['description'].label = 'Mô tả ngắn gọn'
        self.fields['thumbnail'].label = 'Ảnh minh họa'
        self.fields['body'].label = 'Nội dung'
        self.fields['is_public'].label = 'Công khai'
        self.fields['is_job_post'].label = 'Là bài viết tuyển dụng nhân sự'
        self.fields['description'].widget.attrs['placeholder'] = 'Hỗ trợ Markdown'
        self.fields['body'].widget.attrs['placeholder'] = 'Hỗ trợ Markdown'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['body'].label = 'Nội dung'
        self.fields['body'].widget.attrs['placeholder'] = 'Hỗ trợ Markdown'

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["long_name", 'email', "avatar",   "short_description", "long_description"]
        widgets = {
            "long_name": forms.TextInput(),
            "long_description": forms.Textarea(),
        }
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['long_name'].label = 'Tên đầy dủ'
        self.fields['avatar'].label = 'Ảnh đại diện'
        self.fields['email'].label = 'Email'
        self.fields['short_description'].label = 'Mô tả ngắn gọn'
        self.fields['long_description'].label = 'Nội dung'
        self.fields['long_description'].widget.attrs['placeholder'] = 'Hỗ trợ Markdown'
