# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Post
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views import generic
from .forms import EmailPostForm
from .forms import TestingForm
from django.core.mail import send_mail
from .models import Comment
from .forms import CommentForm
from .forms import RepliesForm
from .models import Replies
import requests
import json

# Create your views here.
def post_list(request):
    post = Post.objects.all()
    nop = 3

    splitcounter = 0
    split = []
    indexcounter = 0
    splitlist = []
    last = None
    for p in post:
        splitcounter+= 1
        split.append(p)
        if splitcounter == nop:
            indexcounter += nop
            splitlist.append(split)
            splitcounter = 0
            split = []
    last = slice(indexcounter, len(post))
    splitlist.append(post[last])

    numofpages = range(1, len(splitlist)+1)
    firstpage = splitlist[0]
    postpage = int(request.GET.get('page', 0))
    page = splitlist[postpage -1]
    return render(request, 'blog/post/list.html', {'firstpage':firstpage,
                                                   'page': page,
                                                    'postpage': postpage,
                                                   'numofpages': numofpages,
                                                   })

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )
    replies_form = RepliesForm()
    comments = post.comments.filter(active=True)
    comment_form = CommentForm()
    mainrender = {'post': post,
                  'comments': comments,
                  'comment_form': comment_form,
                  'replies_form': replies_form
                  }
    if request.method == 'POST':
        try:
            request.POST['comment-id']
            commentid = comments.get(pk=request.POST['comment-id'])
            replies_form = RepliesForm(data=request.POST)
            if replies_form.is_valid():
                reply_to_comment = replies_form.save(commit=False)
                reply_to_comment.To = commentid
                reply_to_comment.rep_tag = '@' + commentid.name
                reply_to_comment.save()
                return render(request, 'blog/post/detail.html', {'comments':comments,'post':post,'comment_form':comment_form,'replies_form':replies_form,'is_reply':reply_to_comment})
            else:
                return render(request, 'blog/post/detail.html', {'comments':comments,
                                                                 'post':post,
                                                                 'comment_form':comment_form,
                                                                 'replies_form':replies_form
                                                                 })
        except:
            try:
                request.POST['for_reply']
                commentid = comments.get(pk=request.POST['comment_id_for_rep'])
                reply_id = commentid.repliesto.get(pk=request.POST['reply-id'])
                replies_form = RepliesForm(data=request.POST)
                if replies_form.is_valid():
                    for_reply = replies_form.save(commit=False)
                    for_reply.To = commentid
                    for_reply.rep_tag = '@' + reply_id.name
                    for_reply.save()
                    return render(request, 'blog/post/detail.html', mainrender)
                else:
                    return render(request, 'blog/post/detail.html', mainrender)
            except:
                comment_form = CommentForm(data=request.POST)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.post = post
                    new_comment.save()
                    return render(request, 'blog/post/detail.html', {'comments':comments,'post':post,'comment_form':comment_form,'new_comment':new_comment,'replies_form':replies_form})
                else:
                    return render(request, 'blog/post/detail.html', {'comments':comments,'post':post,'comment_form':comment_form,'replies_form':'replies_form'})
    return render(request, 'blog/post/detail.html', mainrender)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
            return render(request, 'share.html', {'sent':sent})
        else:
            return render(request, 'share.html', {'post': post, 'form': form, 'sent': sent})
    form = EmailPostForm()
    return render(request, 'share.html', {'post':post, 'form':form, 'sent':sent})


def testing(request):
    if request.method == 'POST':
        form = TestingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponse(request.POST.get('comment-id'))
        elif form.errors:
            return render(request, 'blog/post/test.html', {'form': form})
    else:
        form = TestingForm()
        return render(request, 'blog/post/test.html', {'form': form})