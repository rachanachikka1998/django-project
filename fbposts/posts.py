from django.db.models import Count, Q, F

from fbposts.comments import get_comments
from fbposts.constants import Reactions
from fbposts.reactions import get_all_reaction_metrics, get_reaction_details
from fbposts.views import get_user_to_dict
from .models import Post, Reaction


def get_post_by_object(post,reactions):
    user = get_user_to_dict(post.posted_by)
    reactions_dict = get_reaction_details(reactions.filter(post=post))
    comments = get_comments(post.comments.all(),reactions)

    post_json = dict()
    post_json["post_id"] = post.id
    post_json["posted_by"] = user
    post_json["posted_at"] = post.posted_at.strftime("%y-%m-%d %H:%M:%S.%f")
    post_json["post_content"] = post.post_content
    post_json["reactions"] = reactions_dict
    post_json["comments"] = comments
    post_json["comments_count"] = len(comments)
    return post_json


def delete_post(post_id):
    Post.objects.filter(pk=post_id).delete()
    # post.delete()


def get_post(post_id):
    from django.db import connection
    initial_queries = len(connection.queries)
    result_post = Post.objects.filter(pk=post_id).select_related('posted_by') \
        .prefetch_related('comments', 'reactions', 'comments__reactions', 'comments__replies',
                          'comments__replies__reactions', 'comments__commenter', 'comments__replies__commenter')

    reactions = get_all_reaction_metrics()
    result = get_post_by_object(result_post[0],reactions)

    final_queries = len(connection.queries)
    print("complete:", final_queries - initial_queries)
    return result


def create_post(user_id, post_content):
    post = Post.objects.create(posted_by_id=user_id, post_content=post_content)
    return post.id


def get_user_posts(user_id):
    posts = Post.objects.filter(posted_by_id=user_id).select_related('posted_by')
    posts = posts.prefetch_related(
        'comments',
        'reactions',
        'comments__reactions',
        'comments__replies',
        'comments__replies__reactions',
        'comments__commenter',
        'comments__replies__commenter'
    )
    reactions = get_all_reaction_metrics()
    result = [
        get_post_by_object(post, reactions)
        for post in posts
    ]
    return result


def get_posts_with_more_positive_reactions():
    negative_reactions = [Reactions.SAD.value, Reactions.ANGRY.value]

    negative_reactions_count = Count('reaction_type', filter=Q(reaction_type__in=negative_reactions))
    positive_reactions_count = Count('reaction_type', filter=~(Q(reaction_type__in=negative_reactions)))

    count_of_positive_and_negative_reactions = Reaction.objects.values('post').annotate(
        negative=negative_reactions_count,
        positive=positive_reactions_count).filter(~Q(post=None), positive__gt=F('negative'))

    result = [
        reaction['post']
        for reaction in count_of_positive_and_negative_reactions
    ]
    return result


def get_posts_reacted_by_user(user_id):
    from django.db import connection
    initial_queries = len(connection.queries)
    posts = Post.objects.filter(reactions__reactor__id=user_id).select_related('posted_by').prefetch_related('comments',
                                                                                                             'reactions',
                                                                                                             'comments__reactions',
                                                                                                             'comments__replies',
                                                                                                             'comments__replies__reactions',
                                                                                                             'comments__commenter',
                                                                                                             'comments__replies__commenter')

    result = [
        get_post_by_object(post)
        for post in posts
    ]
    final_queries = len(connection.queries)
    print("complete:", final_queries - initial_queries)
    return result


def get_reactions_to_post(post_id):
    from django.db import connection
    initial_queries = len(connection.queries)
    reactions_to_post = Reaction.objects.filter(post_id=post_id).select_related('reactor')
    reaction_list = []
    for reaction in reactions_to_post:
        user_dict = get_user_to_dict(reaction.reactor)
        user_dict["reaction"] = reaction.reaction_type
        reaction_list.append(user_dict)
    final_queries = len(connection.queries)
    print("complete:", final_queries - initial_queries)
    return reaction_list

