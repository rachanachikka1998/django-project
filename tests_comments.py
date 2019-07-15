import pytest
from fixtures import create_user_and_post, create_user_post_comment, \
    create_two_users_two_posts_each_and_comments_replies_to_posts_and_reactions_to_posts_comments_replies


@pytest.mark.django_db
def test_add_comment_created_with_same_parameters_in_db(create_user_and_post):
    from fbposts.comments import add_comment
    from fbposts.models import Comment

    comment_id = add_comment(1, 1, "comment")
    comment = Comment.objects.get(pk=comment_id)
    assert len(Comment.objects.all()) == 1
    assert comment.post_id == 1
    assert comment.commenter_id == 1
    assert comment.comment_content == "comment"


@pytest.mark.django_db
def test_add_comment_with_non_existing_user_raises_integrity_error(create_user_and_post):
    from fbposts.comments import add_comment
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        comment_id = add_comment(1, 0, "comment")


@pytest.mark.django_db
def test_add_comment_with_non_existing_post_raises_integrity_error(create_user_and_post):
    from fbposts.comments import add_comment
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        comment_id = add_comment(0, 1, "comment")


@pytest.mark.django_db
def test_add_comment_with_empty_comment_content_raises_value_error(create_user_and_post):
    from fbposts.comments import add_comment

    with pytest.raises(ValueError):
        post_id = add_comment(1, 1, "")


@pytest.mark.django_db
def test_reply_to_comment_saved_with_same_parameters(create_user_post_comment):
    from fbposts.comments import reply_to_comment
    from fbposts.models import Comment

    reply_id = reply_to_comment(1, 1, "reply")
    reply = Comment.objects.get(pk=reply_id)
    assert reply.comment_id == 1
    assert reply.post is None
    assert reply.commenter_id == 1
    assert reply.comment_content == "reply"


@pytest.mark.django_db
def test_reply_to_comment_with_non_existing_user_raises_integrity_error(create_user_post_comment):
    from fbposts.comments import reply_to_comment
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        comment_id = reply_to_comment(1, 0, "reply")


@pytest.mark.django_db
def test_reply_to_comment_with_non_existing_comment_raises_integrity_error(create_user_post_comment):
    from fbposts.comments import add_comment
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        comment_id = add_comment(0, 1, "reply")


@pytest.mark.django_db
def test_reply_to_comment_with_empty_reply_content_raises_value_error(create_user_and_post):
    from fbposts.comments import reply_to_comment

    with pytest.raises(ValueError):
        post_id = reply_to_comment(1, 1, "")


@pytest.mark.django_db
def test_reply_to_comment_when_replyting_to_reply_created_as_reply_to_comment(create_user_post_comment):
    from fbposts.comments import reply_to_comment
    from fbposts.models import Comment

    reply_id = reply_to_comment(1, 1, "reply")
    nested_reply_id = reply_to_comment(reply_id, 1, "nested reply")
    reply = Comment.objects.get(pk=reply_id)
    nested_reply = Comment.objects.get(pk=nested_reply_id)
    assert nested_reply.comment_id == reply.comment_id
    assert reply.post is None
    assert nested_reply.commenter_id == 1
    assert nested_reply.comment_content == "nested reply"


@pytest.mark.django_db
def test_replies_for_comment_with_non_existing_comment_id_raises_integrity_error():
    from fbposts.comments import get_replies_for_comment
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        replies = get_replies_for_comment(0)


@pytest.mark.django_db
def test_replies_for_comment_returns_replies_of_corresponding_comment(
        create_two_users_two_posts_each_and_comments_replies_to_posts_and_reactions_to_posts_comments_replies):
    from fbposts.comments import get_replies_for_comment
    from fbposts.models import Comment

    replies_json = get_replies_for_comment(1)
    replies = Comment.objects.filter(comment_id=1)

    for reply_json, reply in zip(replies_json, replies):
        assert reply_json["comment_id"] == reply.id
        assert reply_json["commenter"]["user_id"] == reply.commenter_id
        assert reply_json["comment_content"] == reply.comment_content
        assert reply_json["commented_at"] == reply.commented_at.strftime("%y-%m-%d %H:%M:%S.%f")
