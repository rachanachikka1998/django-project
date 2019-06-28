from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import User
from .models import Post
from .models import Comment
from .models import Reaction

from django.template import loader
import json
import datetime


# Create your views here.
def index(request):
    users_list = User.objects.all()
    template = loader.get_template('fbposts/index.html')
    context = {
        'users_list': users_list,
    }
    return HttpResponse(template.render(context, request))


def get_user(user_id):
    user = User.objects.get(pk=user_id)
    return user


def create_post(user_id, post_content):
    post = Post()
    try:
        post.posted_by = User.objects.get(pk=user_id)
        post.post_content = post_content
        post.posted_at = datetime.datetime.now()
        post.save()
        return post.post_id
    except(Exception):
        return "enter a valid user id"


def add_comment(post_id, commenter_id, comment_text):
    comment = Comment()

    try:
        comment.id1 = Post.objects.get(post_id=post_id)
        comment.commenter_id = User.objects.get(user_id=commenter_id)
        comment.comment_content = comment_text
        comment.id2 = None
        comment.type = True
        comment.save()
        return comment.comment_id

    except(Exception):
        return "enter appropriate arguments"


def reply_to_comment(comment_id, reply_user_id, reply_text):
    comment = Comment()

    try:
        comment.id2 = Comment.objects.get(comment_id=comment_id)
        comment.commenter_id = User.object.get(user_id=reply_user_id)
        comment.comment_content = reply_text
        comment.id1 = None
        comment.type = False
        comment.save()
        return comment.comment_id

    except(Exception):
        return "enter appropriate arguments"


def react_to_post(user_id, post_id, reaction_type):
    reactions_list=['HAHA','WOW','SAD','LOVE','LIKE','ANGRY']
    if reaction_type not in reactions_list:
        return "enter appropriate reaction"
    reaction = Reaction()
    try:
        reaction.reactor_id = User.objects.get(user_id=user_id)
        post = Post.objects.get(post_id=post_id)
    except(Exception):
        return "enter existing user and post IDs"

    reactions = Reaction.objects.all()
    if len(reactions) > 0:
        for r in reactions:
            if r.reactor_id.user_id == reaction.reactor_id.user_id:
                if post.post_id == post_id:
                    if r.reaction_type == reaction_type:
                        r.delete()
                        break
                    else:
                        reaction.reacted_to_post = post
                        reaction.reacted_to_comment = None
                        reaction.type = True
                        reaction.reaction_type = reaction_type
                        reaction.save()
                        r.delete()
                        break
    else:
        reaction.reacted_to_post = post
        reaction.reacted_to_comment = None
        reaction.type = True
        reaction.reaction_type = reaction_type
        reaction.save()


def react_to_comment(user_id, comment_id, reaction_type):
    reactions_list = ['HAHA', 'WOW', 'SAD', 'LOVE', 'LIKE', 'ANGRY']
    if reaction_type not in reactions_list:
        return "enter appropriate reaction"
    reaction = Reaction()
    try:
        reaction.reactor_id = User.objects.get(user_id=user_id)
        comment = Comment.objects.get(comment_id=comment_id)
    except(Exception):
        return "enter existing user and post IDs"

    reactions = Reaction.objects.all()
    if len(reactions) > 0:
        for r in reactions:
            if r.reactor_id.user_id == reaction.reactor_id.user_id:
                if comment.comment_id == comment_id:
                    if r.reaction_type == reaction_type:
                        r.delete()
                        break
                    else:
                        reaction.reacted_to_post = None
                        reaction.reacted_to_comment = comment
                        reaction.type = False
                        reaction.reaction_type = reaction_type
                        reaction.save()
                        r.delete()
                        break
    else:
        reaction.reacted_to_post = None
        reaction.reacted_to_comment = comment
        reaction.type = True
        reaction.reaction_type = reaction_type
        reaction.save()


def check():
    b = User.objects.get(user_id=2)
    print(b)
