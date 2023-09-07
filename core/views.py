from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count

from .forms import (
    LoginForm,
    SignupForm,
    PostForm,
    CompanyPostForm,
    CommentForm,
    AccountForm,
)
from .models import Post, Account, Comment, Contact, SavedPost


def home_view(request):
    return render(request, "pages/home.html")


def index_view(request):
    return render(request, "pages/home.html")


def company_signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.is_company = True
            account.is_active = False
            account.save()
            return redirect("login_view")
    else:
        form = SignupForm()
    return render(request, "pages/account/company_signup.html", {"form": form})


def developer_signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_view")
    else:
        form = SignupForm()
    return render(request, "pages/account/developer_signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            return redirect(request.GET.get("next") or "home_view")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("home_view")


def job_post_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        post_list = Post.objects.filter(
            Q(title__icontains=query_str) | Q(body__icontains=query_str),
            is_job_post=True,
            is_public=True,
            is_active=True,
            author__is_active=True,
        )
    else:
        post_list = Post.objects.filter(is_job_post=True, is_active=True, author__is_active=True, is_public=True)
    # Pagination with 2 posts per page
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/post/job_list.html", {"posts": posts})


def project_post_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        post_list = Post.objects.filter(
            Q(title__icontains=query_str) | Q(body__icontains=query_str),
            is_job_post=False,
            is_public=True,
            is_active=True,
            author__is_active=True,
        )
    else:
        post_list = Post.objects.filter(is_job_post=False, is_active=True, author__is_active=True, is_public=True)
    # Pagination with 2 posts per page
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/post/project_list.html", {"posts": posts})


@login_required(login_url="/login/")
def saved_project_post_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        post_list = request.user.saved_posts.filter(
            Q(title__icontains=query_str) | Q(body__icontains=query_str),
            is_job_post=False,
            is_public=True,
            is_active=True,
            author__is_active=True,
        )
    else:
        post_list = request.user.saved_posts.filter(is_job_post=False, is_active=True,author__is_active=True,is_public=True)
    # Pagination with 2 posts per page
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/post/saved_project_list.html", {"posts": posts})


@login_required(login_url="/login/")
def saved_job_post_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        post_list = request.user.saved_posts.filter(
            Q(title__icontains=query_str) | Q(body__icontains=query_str),
            is_job_post=True,
            is_public=True,
            is_active=True,author__is_active=True,
        )
    else:
        post_list = request.user.saved_posts.filter(is_job_post=True,is_active=True, author__is_active=True,is_public=True)
    # Pagination with 2 posts per page
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/post/saved_job_list.html", {"posts": posts})


@login_required(login_url="/login/")
def following_post_list_view(request):
    following = request.user.following.filter(is_active=True)
    query_str = request.GET.get("q")
    if query_str:
        post_list = Post.objects.filter(
            Q(title__icontains=query_str) | Q(body__icontains=query_str),
            is_public=True,
            is_active=True,
            author__is_active=True,
            author__in=following,
        )
    else:
        post_list = Post.objects.filter(is_public=True,author__is_active=True,is_active=True, author__in=following)
    # Pagination with 2 posts per page
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/post/following_list.html", {"posts": posts})


@login_required(login_url="/login/")
def following_project_post_list_view(request):
    following = request.user.following.filter(is_active=True)
    query_str = request.GET.get("q")
    if query_str:
        post_list = Post.objects.filter(
            Q(title__icontains=query_str) | Q(body__icontains=query_str),
            is_job_post=False,
            is_public=True,
            is_active=True,
            author__is_active=True,
            author__in=following,
        )
    else:
        post_list = Post.objects.filter(
            is_job_post=False, is_active=True,is_public=True,author__is_active=True, author__in=following 
        )
    # Pagination with 2 posts per page
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/post/following_project_list.html", {"posts": posts})


@login_required(login_url="/login/")
def following_job_post_list_view(request):
    following = request.user.following.filter(is_active=True)
    query_str = request.GET.get("q")
    if query_str:
        post_list = Post.objects.filter(
            Q(title__icontains=query_str) | Q(body__icontains=query_str),
            is_job_post=True,
            is_public=True,
            is_active=True,
            author__is_active=True,
            author__in=following,
        )
    else:
        post_list = Post.objects.filter(
            is_job_post=True, is_active=True,is_public=True,author__is_active=True, author__in=following
        )
    # Pagination with 2 posts per page
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/post/following_job_list.html", {"posts": posts})


@login_required(login_url="/login/")
def my_job_post_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        post_list = Post.objects.filter(
            Q(title__icontains=query_str) | Q(body__icontains=query_str),
            is_job_post=True,
            author=request.user,
        )
    else:
        post_list = Post.objects.filter(is_job_post=True, author=request.user)
    # Pagination with 2 posts per page
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/post/my_job_list.html", {"posts": posts})


@login_required(login_url="/login/")
def my_project_post_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        post_list = Post.objects.filter(
            Q(title__icontains=query_str) | Q(body__icontains=query_str),
            author=request.user,
        )
    else:
        post_list = Post.objects.filter(author=request.user)
    # Pagination with 2 posts per page
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/post/my_project_list.html", {"posts": posts})


def account_project_post_list_view(request, id):
    author = get_object_or_404(Account, id=id)
    posts = Post.objects.filter(author=author, is_job_post=False, is_active=True,author__is_active=True, is_public=True)
    # Pagination with 2 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/account/project_list.html", {"posts": posts})


def account_job_post_list_view(request, id):
    author = get_object_or_404(Account, id=id)
    posts = Post.objects.filter(author=author, is_job_post=True, is_active=True, author__is_active=True, is_public=True)
    # Pagination with 2 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "pages/account/job_list.html", {"posts": posts})


def company_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        accounts = Account.objects.filter(
            Q(long_name__icontains=query_str) | Q(username__icontains=query_str),
            is_company=True,
            is_active=True,
        )
    else:
        accounts = Account.objects.filter(is_company=True, is_active=True)

    
    # Pagination with 2 posts per page
    paginator = Paginator(accounts, 10)
    page_number = request.GET.get("page", 1)
    try:
        accounts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        accounts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        accounts = paginator.page(paginator.num_pages)
    return render(request, "pages/account/company_list.html", {"accounts": accounts})


def developer_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        accounts = Account.objects.filter(
            Q(long_name__icontains=query_str) | Q(username__icontains=query_str),
            is_company=False,
            is_active=True,
        )
    else:
        accounts = Account.objects.filter(is_company=False, is_active=True)
    # Pagination with 2 posts per page
    paginator = Paginator(accounts, 10)
    page_number = request.GET.get("page", 1)
    try:
        accounts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        accounts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        accounts = paginator.page(paginator.num_pages)
    return render(request, "pages/account/developer_list.html", {"accounts": accounts})


@login_required(login_url="/login/")
def following_account_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        accounts = request.user.following.filter(
            Q(long_name__icontains=query_str) | Q(username__icontains=query_str),
            is_active=True,
        )
    else:
        accounts = request.user.following.filter(is_active=True)
    # Pagination with 2 posts per page
    paginator = Paginator(accounts, 10)
    page_number = request.GET.get("page", 1)
    try:
        accounts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        accounts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        accounts = paginator.page(paginator.num_pages)
    return render(
        request, "pages/account/following_list.html", {"accounts": accounts}
    )


@login_required(login_url="/login/")
def following_company_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        accounts = request.user.following.filter(
            Q(long_name__icontains=query_str) | Q(username__icontains=query_str),
            is_company=True,
            is_active=True,
        )
    else:
        accounts = request.user.following.filter(is_company=True, is_active=True)
    # Pagination with 2 posts per page
    paginator = Paginator(accounts, 10)
    page_number = request.GET.get("page", 1)
    try:
        accounts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        accounts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        accounts = paginator.page(paginator.num_pages)
    return render(
        request, "pages/account/following_company_list.html", {"accounts": accounts}
    )


@login_required(login_url="/login/")
def following_developer_list_view(request):
    query_str = request.GET.get("q")
    if query_str:
        accounts = request.user.following.filter(
            Q(long_name__icontains=query_str) | Q(username__icontains=query_str),
            is_company=False,
            is_active=True,
        )
    else:
        accounts = request.user.following.filter(is_company=False, is_active=True)
    # Pagination with 2 posts per page
    paginator = Paginator(accounts, 10)
    page_number = request.GET.get("page", 1)
    try:
        accounts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        accounts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        accounts = paginator.page(paginator.num_pages)
    return render(
        request, "pages/account/following_developer_list.html", {"accounts": accounts}
    )


def post_detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        if not (post.is_public and post.is_active and post.author.is_active):
            return redirect('home_view')
    
    form = CommentForm()
    if request.user.is_authenticated:
        my_report = Comment.objects.filter(post=post, author=request.user).first()
        if my_report:
            form = CommentForm(instance=my_report)

    context = {
        "post": post,
        "form": form,
    }
    return render(request, "pages/post/detail.html", context)


@login_required(login_url="/login")
def comment_create_view(request, id):
    post = get_object_or_404(Post, id=id, is_active=True, author__is_active=True, is_public=True)
    if request.method == "POST":
        my_report = Comment.objects.filter(post=post, author=request.user).first()
        if my_report:
            form = CommentForm(request.POST, instance=my_report)
        else:
            form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect("post_detail_view", id=post.id)

@login_required(login_url="/login")
def comment_delete_view(request, id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=id)
        comment = Comment.objects.filter(post=post, author=request.user).first()
        if comment:
            comment.delete()
        return redirect("post_detail_view", id=post.id)
    return redirect("home_view")

# Inbox, create, delete, deactive, list sended, list
@login_required(login_url="/login")
def inbox_create_view(request, id):
    post = get_object_or_404(Post, id=id, is_public=True, author__is_active=True, is_active=True)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.is_report = False
            comment.save()
        return redirect("my_sended_inbox_list_view")
    return render(request, "pages/inbox/create.html", {'post':post, 'form':form})

@login_required(login_url="/login")
def inbox_delete_view(request, id):
    if request.method == "POST":
        comment = Comment.objects.filter(id=id, author=request.user).first()
        if comment:
            comment.delete()
    return redirect("my_sended_inbox_list_view")

@login_required(login_url="/login")
def inbox_deactive_view(request, id):
    if request.method == "POST":
        comment = Comment.objects.filter(id=id, post__author=request.user).first()
        if request.user.is_staff:
            comment = Comment.objects.filter(id=id).first()
        if comment:
            comment.is_active = False
            comment.save()
        return redirect("my_inbox_list_view")
    return redirect("home_view")

@login_required(login_url="/login")
def inbox_active_view(request, id):
    if request.method == "POST":
        comment = Comment.objects.filter(id=id, post__author=request.user).first()
        if request.user.is_staff:
            comment = Comment.objects.filter(id=id).first()
        if comment:
            comment.is_active = True
            comment.save()
        return redirect("my_readed_inbox_list_view")
    return redirect("home_view")

@login_required(login_url="/login/")
def my_sended_inbox_list_view(request):

    inbox_list = Comment.objects.filter(author=request.user, is_report=False)
    # Pagination with 2 posts per page

    paginator = Paginator(inbox_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        inboxs = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        inboxs = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        inboxs = paginator.page(paginator.num_pages)
    return render(request, "pages/inbox/sended_inbox_list.html", {"inboxs": inboxs})

@login_required(login_url="/login/")
def my_readed_inbox_list_view(request):
    inbox_list = Comment.objects.filter(post__author=request.user, is_report=False, is_active=False)
    if request.user.is_staff:
        inbox_list = Comment.objects.filter(is_report=True, is_active=False).order_by('created_at')
    # Pagination with 2 posts per page
    paginator = Paginator(inbox_list, 10)
    page_number = request.GET.get("page", 1)
    try:
        inboxs = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        inboxs = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        inboxs = paginator.page(paginator.num_pages)
    return render(request, "pages/inbox/readed_inbox_list.html", {"inboxs": inboxs})

@login_required(login_url="/login/")
def my_inbox_list_view(request):
    inbox_list = Comment.objects.filter(post__author=request.user, is_report=False, is_active=True).order_by('created_at')
    if request.user.is_staff:
        inbox_list = Comment.objects.filter(is_report=True, is_active=True).order_by('created_at')
    # Pagination with 2 posts per page
    paginator = Paginator(inbox_list, 1)
    page_number = request.GET.get("page", 1)
    try:
        inboxs = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        inboxs = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        inboxs = paginator.page(paginator.num_pages)
    return render(request, "pages/inbox/inbox_list.html", {"inboxs": inboxs})


@login_required(login_url="/login")
def project_create_view(request):
    if request.method == "POST":
        if request.user.is_company:
            form = CompanyPostForm(request.POST, request.FILES)
        else:
            form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if not request.user.is_company:
                post.is_job_post = False
            post.save()
            return redirect("post_detail_view", id=post.id)
    else:
        if request.user.is_company:
            form = CompanyPostForm()
        else:
            form = PostForm()
    return render(request, "pages/post/create.html", {"form": form})


@login_required(login_url="/login")
def post_update_view(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    state = post.is_active
    if request.method == "POST":
        if request.user.is_company:
            form = CompanyPostForm(request.POST, request.FILES, instance=post)
        else:
            form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.is_active = state
            if not request.user.is_company:
                post.is_job_post = False
            post.save()
            return redirect("post_detail_view", id=post.id)
    else:
        if request.user.is_company:
            form = CompanyPostForm(instance=post)
        else:
            form = PostForm(instance=post)
    return render(request, "pages/post/update.html", {"form": form, "post": post})


@login_required(login_url="/login")
def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("my_project_post_list_view")
    return render(request, "pages/post/delete.html", {"post": post})


@login_required(login_url="/login")
def post_save_view(request, id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=id)
        saved = SavedPost.objects.filter(post=post, account=request.user)
        if not saved:
            SavedPost.objects.create(post=post, account=request.user)
        return redirect("post_detail_view", id=post.id)
    return redirect("home_view")


@login_required(login_url="/login")
def post_unsave_view(request, id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=id)
        saved = SavedPost.objects.filter(post=post, account=request.user).first()
        if saved:
            saved.delete()
        return redirect("post_detail_view", id=post.id)
    return redirect("home_view")


@login_required(login_url="/login")
def account_follow_view(request, id):
    if request.method == "POST":
        user = get_object_or_404(Account, id=id)
        saved = Contact.objects.filter(from_account=request.user, to_account=user).first()
        if not saved:
            Contact.objects.create(from_account=request.user, to_account=user)
        return redirect("account_detail_view", id=user.id)
    return redirect("home_view")


@login_required(login_url="/login")
def account_unfollow_view(request, id):
    if request.method == "POST":
        user = get_object_or_404(Account, id=id)
        saved = Contact.objects.filter(from_account=request.user, to_account=user).first()
        if saved:
            saved.delete()
        return redirect("account_detail_view", id=user.id)
    return redirect("home_view")


def account_detail_view(request, id):
    account = get_object_or_404(Account, id=id)
    if request.user != account:
        if not (account.is_active):
            return redirect('home_view')
    jobs = Post.objects.filter(author=account, is_job_post=True,is_active=True, is_public=True)[:3]
    projects = Post.objects.filter(
        author=account, is_job_post=False, is_active=True, is_public=True
    )[:5]
    context = {
        "account": account,
        "projects": projects,
        "jobs": jobs,
    }
    return render(request, "pages/account/detail.html", context)


@login_required(login_url="/login")
def account_update_view(request):
    account = get_object_or_404(Account, id=request.user.id)
    if request.method == "POST":
        form = AccountForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            account.is_company = request.user.is_company
            account.save()
            return redirect("account_detail_view", id=account.id)
    else:
        form = AccountForm(instance=account)
    return render(
        request, "pages/account/update.html", {"form": form, "account": account}
    )
