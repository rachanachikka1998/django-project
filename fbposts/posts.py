from django.db.models import Count, Q, F

from fbposts.comments import get_comments
from fbposts.constants import Reactions
from fbposts.reactions import get_reaction_details, get_post_reaction_metrics, get_all_comments_reaction_details, \
    get_all_posts_reaction_details
from fbposts.views import get_user_to_dict
from .models import Post, Reaction


def get_post_by_object(post, reactions, comment_reactions):
    user = get_user_to_dict(post.posted_by)
    comments = get_comments(post.comments.all(), comment_reactions)

    post_json = dict()
    post_json["post_id"] = post.id
    post_json["posted_by"] = user
    post_json["posted_at"] = post.posted_at.strftime("%y-%m-%d %H:%M:%S.%f")
    post_json["post_content"] = post.post_content
    post_json["reactions"] = reactions[post.id]
    post_json["comments"] = comments
    post_json["comments_count"] = len(comments)
    return post_json


def delete_post(post_id):
    post= Post.objects.filter(pk=post_id)
    if len(post)==0:
        raise (Post.DoesNotExist)
    post.delete()
    # post.delete()


def get_post(post_id):
    result_post = Post.objects.filter(pk=post_id).select_related('posted_by') \
        .prefetch_related('comments', 'reactions', 'comments__reactions', 'comments__replies',
                          'comments__replies__reactions', 'comments__commenter', 'comments__replies__commenter')
    comment_ids = get_all_comment_ids_for_post(result_post[0])
    post_reactions = get_all_posts_reaction_details([post_id])
    comment_reactions = get_all_comments_reaction_details(comment_ids)
    result = get_post_by_object(result_post[0], post_reactions, comment_reactions)

    return result


def create_post(user_id, post_content):
    if post_content == "" :
        raise(ValueError)
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
    comment_ids = []

    post_ids = []
    for post in posts:
        post_ids.append(post.id)
        comment_ids += get_all_comment_ids_for_post(post)

    post_reactions = get_all_posts_reaction_details(post_ids)
    comment_reactions = get_all_comments_reaction_details(comment_ids)
    result = [
        get_post_by_object(post, post_reactions, comment_reactions)
        for post in posts
    ]
    return result


def get_all_comment_ids_for_post(post):
    comment_ids = []
    for comment in post.comments.all():
        comment_ids.append(comment.id)
        for reply in comment.replies.all():
            comment_ids.append(reply.id)

    return comment_ids


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
    posts = Post.objects.filter(reactions__reactor__id=user_id).select_related('posted_by').prefetch_related('comments',
                                                                                                             'reactions',
                                                                                                             'comments__reactions',
                                                                                                             'comments__replies',
                                                                                                             'comments__replies__reactions',
                                                                                                             'comments__commenter',
                                                                                                             'comments__replies__commenter')
    post_ids = []
    comment_ids = []
    for post in posts:
        post_ids.append(post.id)
        comment_ids += get_all_comment_ids_for_post(post)

    post_reactions = get_all_posts_reaction_details(post_ids)
    comment_reactions = get_all_comments_reaction_details(comment_ids)
    result = [
        get_post_by_object(post, post_reactions, comment_reactions)
        for post in posts
    ]

    return result


def get_reactions_to_post(post_id):
    reactions_to_post = Reaction.objects.filter(post_id=post_id).select_related('reactor')
    reaction_list = []
    for reaction in reactions_to_post:
        user_dict = get_user_to_dict(reaction.reactor)
        user_dict["reaction"] = reaction.reaction_type
        reaction_list.append(user_dict)

    return reaction_list
