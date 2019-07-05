from django.db.models import Prefetch

from fbposts.models import Comment, Reaction, Post
from fbposts.reactions import get_reaction_details
from fbposts.views import get_user_to_dict


def add_comment(post_id, comment_user_id, comment_text):
    comment = Comment.objects.create(post_id=post_id, commenter_id=comment_user_id, comment_content=comment_text)
    return comment.id


def reply_to_comment(comment_id, reply_user_id, reply_text):
    parent_comment = Comment.objects.select_related('comment').get(pk=comment_id)
    new_comment = Comment()
    if parent_comment.post is None:
        new_comment.comment = parent_comment.comment
    else:
        new_comment.comment = parent_comment
    new_comment.commenter_id = reply_user_id
    new_comment.comment_content = reply_text
    new_comment.save()
    return new_comment.id


def get_replies_for_comment(comment_id):
    from django.db import connection
    initial_queries = len(connection.queries)
    comment = Comment.objects.all().filter(pk=comment_id).prefetch_related('reactions','replies','replies__reactions','commenter','replies__commenter')
    replies = get_comments(comment[0].replies.all())
    for r in replies:
        del r["reactions"]
    final_queries = len(connection.queries)
    print("get_post_by_object:", final_queries - initial_queries)
    return replies


def get_comments(comments,reactions):
    from django.db import connection


    list_of_comments = []
    initial_queries = len(connection.queries)

    for comment in comments:

        comment_dict = dict()

        comment_dict["comment_id"] = comment.id
        comment_dict["commenter"] = get_user_to_dict(comment.commenter)
        comment_dict["commented_at"] = comment.commented_at.strftime("%y-%m-%d %H:%M:%S.%f")

        comment_dict["comment_content"] = comment.comment_content
        comment_dict["reactions"] = get_reaction_details(reactions.filter(comment=comment))
        if comment.post is not None:
            replies = get_comments(comment.replies.all(),reactions)
            comment_dict["replies_count"] = len(replies)
            comment_dict["replies"] = replies
        list_of_comments.append(comment_dict)
    final_queries = len(connection.queries)
    print("get comments", final_queries - initial_queries)


    return list_of_comments


def get_post_comments(post):
    from django.db import connection
    initial_queries = len(connection.queries)

    comments = post.comments.all().select_related('commenter') .prefetch_related('replies__reactions', 'reactions', 'replies__commenter','replies')

    final_queries = len(connection.queries)
    result=get_comments(comments)
    print("get post comments", final_queries - initial_queries)
    return result
