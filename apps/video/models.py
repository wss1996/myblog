
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from django.urls import reverse

from django.conf import settings



# Create your models here.
class Video(models.Model):
    IMG_LINK = '/static/images/summary.jpg'
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='作者',
    )
    title = models.CharField(max_length=150, verbose_name='视频标题')
    summary = models.TextField('文章摘要', max_length=230, default='文章摘要等同于网页description内容，请务必填写...')
    body = models.TextField(blank=True,verbose_name='标签内容')
    img_link = models.CharField('图片地址', default=IMG_LINK, max_length=255)

    video_url = models.URLField(verbose_name='视频链接')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField('观看量', default=0)
    loves = models.IntegerField('喜爱量', default=0)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[:20]

    # 该函数用来获取视频详细地址
    def get_absolute_url(self):
        return reverse('video:detail', kwargs={'pk': self.pk})
        # 统计浏览量

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])