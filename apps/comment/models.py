from django.db import models

from django.conf import settings
from storm.models import Article
from user.models import Ouser
from ckeditor.fields import RichTextField

import markdown
import emoji

class Articlecomment(models.Model):
    author = models.ForeignKey(Ouser,related_name='user_comments',verbose_name='评论人')
    article = models.ForeignKey(Article, related_name='article_comments', verbose_name='所属文章')
    content = RichTextField(verbose_name='评论内容')
    create_date = models.DateTimeField('创建的时间',auto_now_add=True)
    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural = verbose_name
        ordering = ['create_date']
    def __str__(self):
        return self.content[:20]

    # def content_to_markdown(self):
    #     # 先转换成emoji然后转换成markdown,'escape':所有原始HTML将被转义并包含在文档中
    #     to_emoji_content = emoji.emojize(self.content, use_aliases=True)
    #     to_md = markdown.markdown(to_emoji_content,
    #                                     safe_mode='escape',
    #                                     extensions=[
    #                                     'markdown.extensions.extra',
    #                                     'markdown.extensions.codehilite',
    #                                       ])
    #     return to_md