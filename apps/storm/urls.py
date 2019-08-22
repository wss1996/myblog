# ---------------------------
__author__='stormsha'
__date__='2019/3/10 21:03'
# ---------------------------



from django.conf.urls import url
from .views import (IndexView,DetailView,AboutView,ProjectView,DonateView,LoveView)
from video.views import VlogListView

urlpatterns = [
    # 首页
    url(r'^$', IndexView.as_view(template_name='index.html'), name='index'),  # 主页，自然排序
    # url(r'^link/$', LinkView, name='link'),     # 申请友情链接
    # url(r'^category/message/$', MessageView, name='message'),
    url(r'^category/about//$', AboutView.as_view(template_name='about.html'), name='about'),#关于作者
    url(r'^category/money//$', DonateView.as_view(template_name='donate.html'), name='donate'),#赞助作者
    # url(r'^category/exchange/$', ExchangeView, name='exchange'),
    url(r'^category/Cooperation//$', ProjectView.as_view(), name='Cooperation'),
    url(r'^category/chuibi//$', VlogListView.as_view(), name='question'),
    # 分类页面
    url(r'^category/(?P<bigslug>.*?)/(?P<slug>.*?)/$', IndexView.as_view(template_name='content.html'), name='category'),
    # 归档页面
    url(r'^date/(?P<year>\d*)/(?P<month>\d*)/$', IndexView.as_view(template_name='archive.html'), name='date'),
    # 标签页面
    url(r'^tag/(?P<tag>.*?)/$', IndexView.as_view(template_name='content.html'), name='tag'),
    # 文章详情页面
    # url(r'^article/(?P<slug>.*?)/$', DetailView.as_view(), name='article'),
    # url(r'^article/(?P<pk>[0-9]+)/$', DetailView.as_view(), name='article'),
    url(r'^article/(?P<pk>.*?)/$', DetailView.as_view(template_name='article.html'), name='article'),
    # 全文搜索
    # url(r'^search/$', MySearchView.as_view(), name='search'),
    # 喜欢
    url(r'^love/$', LoveView, name='love')
]

