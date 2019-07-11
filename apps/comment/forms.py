#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from django import forms
from .models import Articlecomment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Articlecomment
        fields = ['content']
