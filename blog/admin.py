# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post
from .models import Comment
from .models import Replies


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
                    'status')
    list_filter = ('author','publish','status')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title','body')
admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','body','created','active','post')
    list_filter = ('active','created','update')
    search_fields = ('name','email','body')

admin.site.register(Comment,CommentAdmin)


class RepliesAdmin(admin.ModelAdmin):
    list_display = ('name','email','body','created','active','To')
    list_filter = ('active','created','update')
    search_fields = ('name','email','body')

admin.site.register(Replies, RepliesAdmin)