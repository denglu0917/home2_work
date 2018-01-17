from django.shortcuts import render, redirect
from firstapp.models import Article, Comment, Ticket, UserProfile
from firstapp.forms import CommentForm, UserProfileForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# Create your views here.
def collection(request):
    if request.user.is_authenticated:
        context = {}
        # 获取用户点赞的文章，以下两种均可以
        # like_ticket_articles = request.user.user_tickets.filter(choice='like')
        like_ticket_articles = Ticket.objects.filter(
            choice='like', voter=request.user)

        # 使用for循环从like_ticket_articles中取出票的 id ，在用ticket.article取出文章
        # 然后装载在article_like_list列表中
        # 使用article.voter可以取出点赞用户
        article_like_list = [ticket.article for ticket in like_ticket_articles]
        # 文章分页
        page_robot = Paginator(article_like_list, 3)
        page_num = request.GET.get('page')
        try:
            article_like_list = page_robot.page(page_num)
        except EmptyPage:
            article_like_list = page_robot.page(page_robot.num_pages)
        except PageNotAnInteger:
            article_like_list = page_robot.page(1)

        context['article_like_list'] = article_like_list
        return render(request, 'mycollection.html', context)
    else:
        return redirect(to='index')


def myinfo(request):
    if request.user.is_authenticated:
        context = {}

        if request.method == 'GET':
            form = UserProfileForm

        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data['name']
                sex = form.cleaned_data['sex']
                avatar = form.cleaned_data['avatar']
                # 异常处理，当用户没有profile文件时创建profile
                try:
                    user_info = UserProfile.objects.get(belong_to=request.user)
                except ObjectDoesNotExist:
                    user_info = UserProfile.objects.create(
                        belong_to=request.user)
                user_info.name = name
                user_info.sex = sex
                user_info.avatar = avatar
                user_info.save()
        context['form'] = form
        return render(request, 'myinfo.html', context)
    else:
        return redirect(to='index')


def index(request):
    article_list = Article.objects.all()

    page_robot = Paginator(article_list, 9)
    page_num = request.GET.get('page')
    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        article_list = page_robot.page(1)

    context = {}
    context["article_list"] = article_list

    return render(request, 'index.html', context)


def detail(request, id, error_form=None):
    article = Article.objects.get(id=id)
    context = {}
    voter_id = request.user.id
    print(request.user)
    article_likes = Ticket.objects.filter(choice='like', article_id=id).count()
    context['article_likes'] = article_likes
    try:
        user_ticket_for_this_article = Ticket.objects.get(
            voter_id=voter_id, article_id=id)
        context['user_ticket'] = user_ticket_for_this_article
    except:
        pass
    form = CommentForm
    if error_form is not None:
        context['form'] = error_form
    else:
        context['form'] = form
    context["article"] = article
    return render(request, 'detail.html', context)


def comment(request, id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.cleaned_data["comment"]
        article = Article.objects.get(id=id)
        c = Comment(
            comment=comment,
            belong_to_article=article,
            belong_to_user=request.user)
        c.save()
    else:
        return detail(request, id, error_form=form)
    return redirect(to="detail", id=id)


def index_login(request):
    if request.method == "GET":
        form = AuthenticationForm

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(to="index")

    context = {}
    context['form'] = form

    return render(request, 'login.html', context)


def index_register(request):
    if request.method == "GET":
        form = UserCreationForm

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')

    context = {}
    context['form'] = form

    return render(request, 'register.html', context)


def vote(request, id):
    # 未登录用户不允许投票，自动跳回评论页
    if not isinstance(request.user, User):
        return redirect(to="detail", id=id)

    # 获取页面用户的id
    voter_id = request.user.id

    try:
        # 如果找不到登陆用户对此篇文章的操作，就报错
        user_ticket_for_this_article = Ticket.objects.get(
            voter_id=voter_id, article_id=id)
        user_ticket_for_this_article.choice = request.POST["vote"]
        user_ticket_for_this_article.save()
    except ObjectDoesNotExist:
        new_ticket = Ticket(
            voter_id=voter_id, article_id=id, choice=request.POST["vote"])
        new_ticket.save()

    # 如果是点赞，更新点赞总数
    if request.POST["vote"] == "like":
        article = Article.objects.get(id=id)
        article.likes += 1
        article.save()

    return redirect(to="detail", id=id)
