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


def delete_post(post_id):
    post=Post.objects.get(pk=post_id)
    post.delete()

def get_replies_for_comment(comment_id):
    list_of_replies = dict()
    comment=Comment.objects.get(pk=comment_id)
    replies = get_comments(comment, 'comment')
    for r in replies:
        del r["reactions"]

    return replies

def get_reaction_metrics(post_id):
    return get_count_of_each_reaction(Post.objects.get(pk=post_id), 'post')


def get_total_reaction_count():
    posts = Post.objects.all()
    result = dict()
    for post in posts:
        dictionary = get_count_of_each_reaction(post, 'post')
        list_of_reaction_count = dictionary.values()
        sum = 0
        for num in list_of_reaction_count:
            sum += num
        result[post.post_id] = sum
    return result


def get_reactions_to_post(post_id):
    post = Post.objects.get(pk=post_id)
    reactions = Reaction.objects.filter(reacted_to_post=post)
    reaction_list = []
    for reaction in reactions:
        result = get_user_to_dict(reaction.reactor_id)
        result["reaction"] = reaction.reaction_type
        reaction_list.append(result)
    return reaction_list


def get_user_posts(user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(posted_by=user)
    list_of_posts = []
    for post in posts:
        list_of_posts.append(get_post(post.post_id))
    return list_of_posts


def get_posts_with_more_positive_reactions():
    reactions_list = ['HAHA', 'LIKE', 'WOW', 'ANGRY', 'SAD', 'LOVE']
    posts = Post.objects.all()
    list_of_posts = []
    for post in posts:
        each_reaction_count = get_count_of_each_reaction(post, 'post')
        positive = 0
        negative = 0
        for reaction in reactions_list:
            r = each_reaction_count[reaction]
            if r == 'SAD' or r == 'ANGRY':
                negative += 1
            else:
                positive += 1
        if positive > negative:
            list_of_posts.append(post.post_id)
    return list_of_posts


def get_posts_reacted_by_user(user_id):
    user = User.objects.get(pk=user_id)
    reactions = Reaction.objects.filter(reactor_id=user)
    list_of_posts = []
    for reaction in reactions:
        if reaction.reacted_to_post != None:
            list_of_posts.append(get_post(reaction.reacted_to_post.post_id))
    return list_of_posts


def get_count_of_each_reaction(id_object, type):
    reactions_dict = dict()
    reactions_list = ['HAHA', 'LIKE', 'WOW', 'ANGRY', 'SAD', 'LOVE']
    for reaction in reactions_list:
        reactions_dict[reaction] = 0
    try:
        if type == True:
            reactions = Reaction.objects.filter(reacted_to_post=id_object)

        else:
            reactions = Reaction.objects.filter(reacted_to_comment=id_object)
    except(Exception):
        return {"count": 0, "type": []}
    for reaction in reactions:
        reactions_dict[reaction.reaction_type] += 1
    return reactions_dict


def get_user_to_dict(user_object):
    user = dict()
    user["user_id"] = user_object.user_id
    user["name"] = user_object.username
    user["profile_pic_url"] = user_object.pic_url
    return user


def get_reaction_details(id_object, type):
    reactions_dict = dict()
    reactions_list = ['HAHA', 'LIKE', 'WOW', 'ANGRY', 'SAD', 'LOVE']
    for reaction in reactions_list:
        reactions_dict[reaction] = 0
    try:
        if type == True:
            reactions = Reaction.objects.filter(reacted_to_post=id_object)

        else:
            reactions = Reaction.objects.filter(reacted_to_comment=id_object)
    except(Exception):
        return {"count": 0, "type": []}
    for reaction in reactions:
        reactions_dict[reaction.reaction_type] += 1

    count = 0
    final = []
    for reaction in reactions_list:
        count += reactions_dict[reaction]
        if reactions_dict[reaction] != 0:
            final.append(reaction)

    reactions = dict()
    reactions["count"] = count
    reactions["type"] = final
    return reactions
def get_post_comments(post):
    comments = Comment.objects.filter(id1=)
    comments = Comment.objects.filter(id1=id_object)


def get_comments(id_object, type):
    list_of_comments = []
    if type == 'post':
        comments = Comment.objects.filter(id1=id_object)
    else:
        comments = Comment.objects.filter(id2=id_object)
    for comment in comments:
        comment_dict = dict()
        comment_dict["comment_id"] = comment.comment_id
        comment_dict["commenter"] = get_user_to_dict(comment.commenter_id)
        comment_dict["commented_at"] = comment.commented_at
        comment_dict["comment_content"] = comment.comment_content
        comment_dict["reactions"] = get_reaction_details(comment, 'commment')
        if type == 'post':
            replies = get_comments(comment, 'comment')
            comment_dict["replies_count"] = len(replies)
            comment_dict["replies"] = replies
        list_of_comments.append(comment_dict)

    return list_of_comments


def get_post(post_id):
    post = Post.objects.get(pk=post_id)
    post_json = dict()
    post_json["post_id"] = post_id
    user = get_user_to_dict(post.posted_by)
    post_json["posted_by"] = user
    post_json["posted_at"] = str(post.posted_at)
    post_json["post_content"] = post.post_content
    reactions = get_reaction_details(post, 'post')
    post_json["reactions"] = reactions
    comments = get_comments(post, 'post')
    post_json["comments"] = comments
    post_json["comments_count"] = len(comments)
    return post_json


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
        post.posted_at = str(datetime.datetime.now())
        post.save()
        return post.post_id
    except(Exception):
        return "enter a valid user id"


def add_comment(post_id, commenter_id, comment_text):
    comment = Comment()

    try:
        comment.post = Post.objects.get(pk=post_id)
        comment.commenter_id = User.objects.get(pk=commenter_id)
        comment.comment_content = comment_text
        comment.comment = None
        comment.type = True
        comment.commented_at = str(datetime.datetime.now())
        comment.save()
        return comment.comment_id

    except(Exception):
        return "enter appropriate arguments"


def reply_to_comment(comment_id, reply_user_id, reply_text):
    comment = Comment()

    try:
        comment.comment = Comment.objects.get(pk=comment_id)
        comment.commenter_id = User.objects.get(pk=reply_user_id)
        comment.comment_content = reply_text
        comment.post = None
        comment.commented_at = str(datetime.datetime.now())
        comment.save()
        return comment.comment_id

    except(Exception):
        return "enter appropriate arguments"


def react_to_post(user_id, post_id, reaction_type):
    reactions_list = ['HAHA', 'WOW', 'SAD', 'LOVE', 'LIKE', 'ANGRY']
    if reaction_type not in reactions_list:
        return "enter appropriate reaction"
    reaction = Reaction()
    try:
        user = User.objects.get(pk=user_id)
        post = Post.objects.get(pk=post_id)
    except(Exception):
        return "enter existing user and post IDs"
    reactions = Reaction.objects.all()
    flag = 0
    if len(reactions) > 0:
        for r in reactions:
            if r.reactor_id == user:
                if r.reacted_to_post == post_id:
                    if r.reaction_type == reaction_type:
                        flag = 1
                        r.delete()
                        break
                    else:
                        flag = 1
                        add_new_reaction(user, post, reaction_type, 'post')
                        r.delete()
                        break
        if flag == 0:
            add_new_reaction(user, post, reaction_type,'post')
    else:
        add_new_reaction(user, post, reaction_type, 'post')


def add_new_reaction(user, id_object, reaction_type, type):
    if type == 'post':
        reaction = Reaction()
        reaction.reactor = user
        reaction.post = id_object
        reaction.comment = None
        reaction.reaction_type = reaction_type
        reaction.save()
    else:
        reaction = Reaction()
        reaction.reactor = user
        reaction.post = None
        reaction.comment = id_object
        reaction.reaction_type = reaction_type
        reaction.save()


def react_to_comment(user_id, comment_id, reaction_type):
    reactions_list = ['HAHA', 'WOW', 'SAD', 'LOVE', 'LIKE', 'ANGRY']
    if reaction_type not in reactions_list:
        return "enter appropriate reaction"
    reaction = Reaction()
    try:
        user = User.objects.get(pk=user_id)
        comment = Comment.objects.get(pk=comment_id)
    except(Exception):
        return "enter existing user and post IDs"

    reactions = Reaction.objects.all()
    flag = 0
    if len(reactions) > 0:
        for r in reactions:
            if user == r.reactor_id:
                if r.reacted_to_comment == comment:
                    if r.reaction_type == reaction_type:
                        flag = 1
                        r.delete()
                        break
                    else:
                        flag = 1
                        add_new_reaction(user, comment, reaction_type, 'comment')
                        break
        if flag == 0:
            add_new_reaction(user, comment, reaction_type, 'comment')

    else:
        add_new_reaction(user, comment, reaction_type, 'comment')


def check():
    print(len({"a": 1, "b": 2}))
