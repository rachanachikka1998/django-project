from django.db.models import Count, Q, F

from fbposts.comments import get_post_comments
from fbposts.constants import Reactions
from fbposts.reactions import get_post_reaction_details
from fbposts.views import get_user_to_dict
from .models import Post, User, Reaction


def get_post_by_object(post):
    user = get_user_to_dict(post.posted_by)
    reactions = get_post_reaction_details(post)
    comments = get_post_comments(post)

    post_json = dict()
    post_json["post_id"] = post.id
    post_json["posted_by"] = user
    post_json["posted_at"] = post.posted_at.strftime("%y-%m-%d %H:%M:%S.%f")
    post_json["post_content"] = post.post_content
    post_json["reactions"] = reactions
    post_json["comments"] = comments
    post_json["comments_count"] = len(comments)
    return post_json


def delete_post(post_id):
    Post.objects.filter(pk=post_id).delete()
    # post.delete()


def get_post(post_id):
    post = Post.objects.select_related('posted_by').get(pk=post_id)
    return get_post_by_object(post)


def create_post(user_id, post_content):
    post = Post.objects.create(posted_by_id=user_id, post_content=post_content)
    return post.id


# correction
def get_user_posts(user_id):
    posts = Post.objects.filter(posted_by_id=user_id)
    return [
        get_post_by_object(post)
        for post in posts
    ]


def get_posts_with_more_positive_reactions():
    count_of_positive_and_negative_reactions = Reaction.objects.values('post').annotate(
        negative=Count('reaction_type', filter=Q(reaction_type__in=[Reactions.SAD.value, Reactions.ANGRY.value])),
        positive=Count('reaction_type',
                       filter=~(Q(reaction_type__in=[Reactions.SAD.value, Reactions.SAD.value])))).filter(~Q(post=None),
                                                                                                          positive__gt=F(
                                                                                                              'negative'))

    return [
        reaction['post']
        for reaction in count_of_positive_and_negative_reactions
    ]


def get_posts_reacted_by_user(user_id):
    reactions_by_user = Reaction.objects.filter(~(Q(post=None)), reactor_id=user_id).select_related('post')

    return [
        get_post_by_object(reaction.post)
        for reaction in reactions_by_user
    ]


def get_reactions_to_post(post_id):
    post = Post.objects.get(pk=post_id)
    reactions_to_post = post.reactions.all().select_related('reactor')
    reaction_list = []
    for reaction in reactions_to_post:
        user_dict = get_user_to_dict(reaction.reactor)
        user_dict["reaction"] = reaction.reaction_type
        reaction_list.append(user_dict)
    return reaction_list
