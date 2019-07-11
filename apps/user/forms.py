from django import forms
from .models import Ouser
from storm.models import Article



class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)


class loginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Ouser
        fields = ['link', 'avatar']

# 写文章的表单类
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # 自定义表单包含的字段
        # fields = ('title','summary','body','img_link','slug','category','tags')
        fields = ('title', 'body','category','slug','summary')
        # fields = ('title', 'body', 'category','summary')
