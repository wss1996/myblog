from django.shortcuts import render

# Create your views here.
from django.shortcuts import  render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from storm.models import Article
from .forms import CommentForm

#文章评论部分的视图函数
@login_required(login_url='/accounts/login/')
def post_comment(request,pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("评论填写有误，请重新填写")
    else:
        return HttpResponse("发表评论只接受post请求")

