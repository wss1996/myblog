"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
# from django.views import static ##新增
# from django.conf import settings ##新增
from django.contrib.sitemaps.views import sitemap


# from rest_framework.routers import DefaultRouter
# # from api import views as api_views
# if settings.API_FLAG:
#     router = DefaultRouter()
#     router.register(r'users', api_views.UserListSet)
#     router.register(r'articles', api_views.ArticleListSet)
#     router.register(r'tags', api_views.TagListSet)
#     router.register(r'categorys', api_views.CategoryListSet)



urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # url(r'^static/(?P<path>.*)$', static.serve,
    #     {'document_root': settings.STATIC_ROOT}, name='static'),
    # 用户
    url(r'^accounts/', include('user.urls', namespace='accounts')),
    # storm
    url('', include('storm.urls', namespace='blog')),  # blog
    # 评论
    url('', include('comment.urls', namespace='comment')),  # comment

    url('', include('video.urls', namespace='video')),  # video
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#
# if settings.API_FLAG:
#     urlpatterns.append(url(r'^api/v1/', include(router.urls, namespace='api')))    # restframework