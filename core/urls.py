from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("jobs/", views.job_post_list_view, name="job_post_list_view"),
    path("projects/", views.project_post_list_view, name="project_post_list_view"),
    path(
        "projects/saved/",
        views.saved_project_post_list_view,
        name="saved_project_post_list_view",
    ),
    path(
        "jobs/saved/",
        views.saved_job_post_list_view,
        name="saved_job_post_list_view",
    ),
    path(
        "posts/following/",
        views.following_post_list_view,
        name="following_post_list_view",
    ),
    path(
        "projects/following/",
        views.following_project_post_list_view,
        name="following_project_post_list_view",
    ),
    path(
        "jobs/following/",
        views.following_job_post_list_view,
        name="following_job_post_list_view",
    ),
    path(
        "accounts/posts/",
        views.my_project_post_list_view,
        name="my_project_post_list_view",
    ),
    path(
        "accounts/jobs/",
        views.my_job_post_list_view,
        name="my_job_post_list_view",
    ),
    path(
        "accounts/<int:id>/projects/",
        views.account_project_post_list_view,
        name="account_project_post_list_view",
    ),
    path(
        "accounts/<int:id>/jobs/",
        views.account_job_post_list_view,
        name="account_job_post_list_view",
    ),
    path(
        "developers/",
        views.developer_list_view,
        name="developer_list_view",
    ),
    path(
        "companies/",
        views.company_list_view,
        name="company_list_view",
    ),
    path(
        "developers/following/",
        views.following_developer_list_view,
        name="following_developer_list_view",
    ),
    path(
        "companies/following/",
        views.following_company_list_view,
        name="following_company_list_view",
    ),
    path(
        "accounts/following/",
        views.following_account_list_view,
        name="following_account_list_view",
    ),
    path("account/<int:id>/", views.account_detail_view, name="account_detail_view"),
    path("account/<int:id>/follow/", views.account_follow_view, name="account_follow_view"),
    path("account/<int:id>/unfollow/", views.account_unfollow_view, name="account_unfollow_view"),
    path("profile/edit/", views.account_update_view, name="account_update_view"),
    path("posts/<int:id>/", views.post_detail_view, name="post_detail_view"),
    path(
        "posts/<int:id>/comment/", views.comment_create_view, name="comment_create_view"
    ),
    path(
        "posts/<int:id>/uncomment/", views.comment_delete_view, name="comment_delete_view"
    ),
    path('posts/<int:id>/inbox/', views.inbox_create_view, name='inbox_create_view'),
    path('inboxs/<int:id>/deactive/', views.inbox_deactive_view, name='inbox_deactive_view'),
    path('inboxs/<int:id>/active/', views.inbox_active_view, name='inbox_active_view'),
    path('inboxs/<int:id>/delete/', views.inbox_delete_view, name='inbox_delete_view'),
    path('inboxs/sended', views.my_sended_inbox_list_view, name='my_sended_inbox_list_view'),
    path('inboxs/', views.my_inbox_list_view, name='my_inbox_list_view'),
    path('inboxs/read', views.my_readed_inbox_list_view, name='my_readed_inbox_list_view'),

    path("projects/new", views.project_create_view, name="project_create_view"),
    path("posts/<int:id>/edit", views.post_update_view, name="post_update_view"),
    path("posts/<int:id>/delete", views.post_delete_view, name="post_delete_view"),
    path("posts/<int:id>/save", views.post_save_view, name="post_save_view"),
    path("posts/<int:id>/unsave", views.post_unsave_view, name="post_unsave_view"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/developer", views.developer_signup_view, name="developer_signup_view"),
    path("signup/company", views.company_signup_view, name="company_signup_view"),

    path('password-change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
