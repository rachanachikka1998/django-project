from fbposts.models import Comment, User, Post
from fbposts.views import get_user_to_dict


def add_comment(post_id, comment_user_id, comment_text):
    try:
        comment = Comment.objects.create(post_id=post_id, commenter_id=comment_user_id, comment_content=comment_text)
    except User.DoesNotExist:
        return "enter appropriate user_id"
    except Post.DoesNotExist:
        return "enter appropriate post id"

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
    comment = Comment.objects.get(pk=comment_id)
    replies = get_replies(comment)
    for r in replies:
        del r["reactions"]
    return replies


def get_replies(comment):
    comments = Comment.objects.filter(comment=comment).select_related('commenter')
    return get_comments(comments)


def get_comments(comments):
    from fbposts.reactions import get_comment_reaction_details

    list_of_comments = []

    for comment in comments:
        comment_dict = dict()
        comment_dict["comment_id"] = comment.id
        comment_dict["commenter"] = get_user_to_dict(comment.commenter)
        comment_dict["commented_at"] = comment.commented_at.strftime("%y-%m-%d %H:%M:%S.%f")
        comment_dict["comment_content"] = comment.comment_content
        comment_dict["reactions"] = get_comment_reaction_details(comment)
        if comment.post is not None:
            replies = get_replies(comment)
            comment_dict["replies_count"] = len(replies)
            comment_dict["replies"] = replies
        list_of_comments.append(comment_dict)

    return list_of_comments


def get_post_comments(post):
    comments = Comment.objects.filter(post=post)
    return get_comments(comments)
