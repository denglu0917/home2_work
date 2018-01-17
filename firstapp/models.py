from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=500)
    img = models.CharField(null=True, blank=True, max_length=250)
    content = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    createtime = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    avatar = models.CharField(
        max_length=250, default="static/images/default.png")
    comment = models.TextField(null=True, blank=True)
    createtime = models.DateField(auto_now=True)
    belong_to_user = models.ForeignKey(
        to=User,
        related_name='user_comment',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    belong_to_article = models.ForeignKey(
        to=Article,
        related_name="under_comments",
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

# 以下两种方法都能拿到相同人的票,取出的票是列表的形式
# 使用for...in...，取出列表中的每一个对象，然后使用.article取出文章，在装载到列表中
# 形成文章列表
# us = request.user
# like_tic = us.user_tickets.filter(choice='like')
# like_tic_1 = Ticket.objects.filter(choice='like', voter=us)


class Ticket(models.Model):
    voter = models.ForeignKey(
        to=User, related_name="user_tickets", on_delete=models.CASCADE)
    article = models.ForeignKey(
        to=Article, related_name="article_tickets", on_delete=models.CASCADE)
    ARTICLE_CHOICES = (
        ("like", "like"),
        ("dislike", "dislike"),
        ("normal", "normal"),
    )
    choice = models.CharField(choices=ARTICLE_CHOICES, max_length=10)

    def __str__(self):
        return str(self.id)


class UserProfile(models.Model):
    belong_to = models.OneToOneField(
        to=User, related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=100)
    avatar = models.ImageField(
        null=True, blank=True, upload_to='profile_image')
    SEX_CHOICE = (
        ('男', '男'),
        ('女', '女'),
    )
    sex = models.CharField(
        choices=SEX_CHOICE, max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.belong_to)
