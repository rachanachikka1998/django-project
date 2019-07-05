from django.db.models import Count, Q

from fbposts.constants import Reactions
from fbposts.models import Reaction


def react_to_post(user_id, post_id, reaction_type):
    reactions_list = [Reactions.LIKE.value, Reactions.LOVE.value, Reactions.HAHA.value, Reactions.WOW.value,
                      Reactions.SAD.value, Reactions.ANGRY.value]
    if reaction_type not in reactions_list:
        return "enter appropriate reaction"

    try:
        user_reaction = Reaction.objects.get(post_id=post_id, reactor_id=user_id)
    except Reaction.DoesNotExist:
        Reaction.objects.create(reactor_id=user_id, post_id=post_id, reaction_type=reaction_type)
        return
    delete_or_update_user_reaction(user_reaction, reaction_type)


def react_to_comment(user_id, comment_id, reaction_type):
    reactions_list = [Reactions.LIKE.value, Reactions.LOVE.value, Reactions.HAHA.value, Reactions.WOW.value,
                      Reactions.SAD.value, Reactions.ANGRY.value]
    if reaction_type not in reactions_list:
        return "enter appropriate reaction"

    try:
        user_reaction = Reaction.objects.get(comment_id=comment_id, reactor_id=user_id)
    except Reaction.DoesNotExist:
        Reaction.objects.create(reactor_id=user_id, comment_id=comment_id, reaction_type=reaction_type)
        return
    delete_or_update_user_reaction(user_reaction, reaction_type)


def delete_or_update_user_reaction(user_reaction, reaction_type):
    if user_reaction.reaction_type == reaction_type:
        user_reaction.delete()
    else:
        user_reaction.update(reaction_type=reaction_type)


def get_reaction_details(reactions):
    reactions_post=reactions.values('reaction_type').annotate(Count('reaction_type'))
    result=dict()
    for reaction in reactions_post:
        result[reaction['reaction_type']]=reaction['reaction_type__count']
    return result




def get_reaction_metrics(post_id):
    from django.db import connection
    initial_queries = len(connection.queries)
    result = Reaction.objects.all().filter(post__id=post_id).values('reaction_type').annotate(count=Count('post'))
    reactions_dict = dict()
    for res in result:
        reactions_dict[res['reaction_type']] = res['count']
    final_queries = len(connection.queries)
    print("complete:", final_queries - initial_queries)
    return reactions_dict


def get_total_reaction_count():
    from django.db import connection
    initial_queries = len(connection.queries)
    reactions_dict = dict()
    result = Reaction.objects.values('post__id').filter(~(Q(post__id=None))).annotate(count=Count('reaction_type'))
    for post in result:
        reactions_dict[post['post__id']] = post['count']
    final_queries = len(connection.queries)
    print("complete:", final_queries - initial_queries)
    return reactions_dict


def get_post_reaction_metrics(post):
    reactions_dict = dict()
    result = post.reactions.all().values('reaction_type').annotate(count=Count('post'))
    for res in result:
        reactions_dict[res['reaction_type']] = res['count']
    return reactions_dict


def get_all_posts_reaction_details():
    reactions=Reaction.objects.filter(~Q(comment = None)).values('post__id','reaction_type').annotate(count=Count('reaction_type'))
    result=dict()

    for reaction in reactions:
        result[reaction['post__id']]=dict()
    for reaction in reactions:
        result[reaction['post__id']].add(reaction['reaction_type'],reaction['reaction__type__count'])
    return result

