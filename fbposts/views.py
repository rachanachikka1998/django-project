from django.http import HttpResponse
from django.template import loader

from .models import Comment
from .models import User


def get_user_to_dict(user_object):
    from django.db import connection


    initial_queries = len(connection.queries)
    user = dict()
    user["user_id"] = user_object.id
    user["name"] = user_object.username
    user["profile_pic_url"] = user_object.pic_url
    final_queries = len(connection.queries)
    print("get comments sub call", final_queries - initial_queries)
    return user


# Create your views here.

def index(request):
    users_list = User.objects.all()
    template = loader.get_template('fbposts/index.html')
    context = {
        'users_list': users_list,
    }
    return HttpResponse(template.render(context, request))


def check():
    post = Comment.objects.get(pk=1)
    result = post.reactions.all()
    return result
