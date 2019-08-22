from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.shortcuts import render, HttpResponse, render_to_response
from .models import Video
from django.views.decorators.csrf import csrf_exempt
from comment.forms import CommentForm
# from utils.utils import PaginatorMixin

class VlogListView(ListView):
    """
    列表
    """
    model = Video
    context_object_name = 'articles'
    template_name = 'video_list.html'


class VlogDetailView(DetailView):
    """
    单篇
    """
    model = Video
    context_object_name = 'article'
    template_name = 'video_detail.html'

    def get_context_data(self, **kwargs):
        context = super(VlogDetailView, self).get_context_data(**kwargs)
        self.object.increase_views()

        # 传递给模板文章类型，用于评论表单区分
        # article_type = 'vlog'
        #
        # comment_form = CommentForm()
        # extra_data = {
        #     'comment_form': comment_form,
        #     # 生成树形评论
        #     'comments': self.object.comments.all(),
        #     'article_type': article_type,
        # }
        # context.update(extra_data)
        return context


# @csrf_exempt
# def LoveView(request):
#     data_id = request.POST.get('um_id', '')
#     if data_id:
#         article = Video.objects.get(id=data_id)
#         article.loves += 1
#         article.save()
#         return HttpResponse(article.loves)
#     else:
#         return HttpResponse('error', status=405)