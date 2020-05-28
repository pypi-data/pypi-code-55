from django.db import models
from blog.models import Post


# Create your models here.
class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    nickname = models.CharField(max_length=50, verbose_name="昵称")
    email = models.EmailField(verbose_name="邮箱")
    website = models.URLField(verbose_name="网站")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    content = models.CharField(max_length=2000, verbose_name="内容")
    # target = models.ForeignKey(to=Post, verbose_name="评论目标", on_delete=models.DO_NOTHING)
    target = models.CharField(max_length=100, verbose_name="评论目标")
    class Meta:
        verbose_name_plural = verbose_name = "评论"

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)

