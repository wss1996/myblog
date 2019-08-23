# ---------------------------
__author__ = 'wss'
__date__ = '2019/7/9 21:37'
# ---------------------------
import markdown
import time
from django.views import generic
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import render, HttpResponse, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Article, BigCategory, Category, Tag
from video.models import Video
from comment.forms import CommentForm
from comment.models import Articlecomment
from markdown.extensions.toc import TocExtension  # 锚点的拓展
# from haystack.generic_views import SearchView  # 导入搜索视图
# from haystack.query import SearchQuerySet


# Create your views here.
class IndexView(generic.ListView):
    """
        首页视图,继承自ListVIew，用于展示从数据库中获取的文章列表
    """
    # 获取数据库中的文章列表
    model = Article
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'index.html'
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    # context_object_name = 'articles'
    # post = Article.objects.all()
    # print(post)
    paginate_by = 6

    # 重写通用视图的 get_queryset 函数，获取定制数据
    def get_queryset(self):
        # 调用父类的方法获取查询集
        queryset = super().get_queryset()
        # print(queryset)
        # 日期归档
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')

        # 标签
        tag = self.kwargs.get('tag')
        # print(self.kwargs)

        # 导航条
        self.big_slug = self.kwargs.get('bigslug')
        # print(self.big_slug)

        # 文章分类
        self.slug = self.kwargs.get('slug')

        # print(self.kwargs)
        if self.big_slug:
            big = get_object_or_404(BigCategory, slug=self.big_slug)
            # print(big)
            queryset = queryset.filter(category__bigcategory=big)
            # print(type(queryset))

        if self.slug:
                slu = get_object_or_404(Category, slug=self.slug)
                # print(slu)
                # print(type(slu))
                queryset = queryset.filter(category=slu)

        if year and month:
            queryset = get_list_or_404(queryset, create_date__year=year, create_date__month=month)

        if tag:
            tags = get_object_or_404(Tag, name=tag)
            # self.big_slug = BigCategory.objects.filter(category__article__tags=tags)
            # self.big_slug = self.big_slug[0].slug
            queryset = queryset.filter(tags=tags)

        return queryset

    def get_context_data(self, **kwargs):

        # 首先获得父类生成的传递给模板的字典。
        context = super(IndexView, self).get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。

        paginator = context.get('paginator')
        page = context.get('page_obj')
        # print(page)
        is_paginated = context.get('is_paginated')

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        self.right = []
        if not is_paginated:
            self.right = []
        else:
            self.right = page_range[page_number:total_pages+1]

        context['right'] = self.right
        # print(context)
        # print(context.page_obj)
        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context


class DetailView(generic.DetailView):
    """
        Django有基于类的视图DetailView,用于显示一个对象的详情页，我们继承它
    """
    # 获取数据库中的文章列表
    model = Article
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'article.html'
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'article'
    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(DetailView, self).get(request, *args, **kwargs)
        # 注意 self.object 的值就是被访问的文章 post
        # self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response


    def get_object(self,queryset=None):
        obj = super(DetailView, self).get_object(queryset=None)
        # pk = self.kwargs.get(self.pk_url_kwarg)
        # 设置浏览量增加时间判断,同一篇文章两次浏览超过半小时才重新统计阅览量,作者浏览忽略
        u = self.request.user
        if u != obj.author:
            obj.update_views()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify),
        ])
        obj.body = md.convert(obj.body)
        obj.toc = md.toc
        return obj

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        # article = Article.objects.get(id=id)
        # # 取出文章评论
        # comments = self.objects.filter(article=id)
        comments = self.object.article_comments.all()
        form = CommentForm()

        context.update(
            {
                'comments': comments,
                'form':form
            }
        )

        return context


# def MessageView(request):
#     return render(request, 'message.html', {'category':'message'})
#
#
# def LinkView(request):
#     return render(request, 'link.html')
#
#
 # def AboutView(request):
 #    return render(request, 'about.html', {'category': 'about'})

class AboutView(generic.TemplateView):
    template_name = "about.html"
#
#
# def DonateView(request):
#     return render(request, 'donate.html', {'category':'money'})
class DonateView(generic.TemplateView):
    template_name = "donate.html"


#
#
# def ExchangeView(request):
#     return render(request, 'exchange.html', {'category':'exchange'})
#
#
# def ProjectView(request):
#      return render(request, 'project.html', {'category':'Cooperation'})

class ProjectView(generic.TemplateView):
    template_name = "project.html"
#
#
# class QuestionView(generic.TemplateView):
#     template_name = "video_list.html"

# def QuestionView(request):
#     return render(request, 'video_list.html',{'category':'question'})


#
#
@csrf_exempt
def LoveView(request):
    data_id = request.POST.get('um_id', '')
    if data_id:
        article = Article.objects.get(id=data_id)
        # print(data_id)
        # for id in Video.id:
        #     print(id)

        video = Video.objects.get(id=1)
        article.loves += 1
        video.loves =article.loves
        video.save()
        article.save()
        return HttpResponse(article.loves)
    else:
        return HttpResponse('error', status=405)
#
#
# # 重写搜索视图，可以增加一些额外的参数，且可以重新定义名称
# class MySearchView(SearchView):
#     # 返回搜索结果集
#     context_object_name = 'search_list'
#     # 设置分页
#     paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
#     paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
#     # 搜索结果以浏览量排序
#     queryset = SearchQuerySet().order_by('-views')
#
#
def page_not_found(request):
    return render_to_response('404.html')

