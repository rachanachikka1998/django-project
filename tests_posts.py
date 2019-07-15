import pytest
from fixtures import *


@pytest.mark.django_db
def test_create_post_with_empty_post_content_raises_value_error(create_user_and_post):
    from fbposts.posts import create_post

    with pytest.raises(ValueError):
        post_id = create_post(1, "")


@pytest.mark.django_db
def test_create_post_created_with_same_parameters_in_db(create_user_and_post):
    from fbposts.posts import create_post
    from fbposts.models import Post

    post_id = create_post(1, "post1")
    assert len(Post.objects.all()) == 2
    post = Post.objects.get(id=post_id)
    assert post.posted_by_id == 1
    assert post.post_content == "post1"


@pytest.mark.django_db
def test_create_post_with_non_existing_user_raises_integrity_error():
    from fbposts.posts import create_post
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        post_id = create_post(0, "post1")


@pytest.mark.django_db
def test_get_post_with_non_existing_post_id_raises_integrity_error():
    from fbposts.posts import get_post
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        post_json = get_post(0)


@pytest.mark.django_db
def test_get_post_returns_same_values_in_db(
        create_two_users_two_posts_each_and_comments_replies_to_posts_and_reactions_to_posts_comments_replies):
    from fbposts.models import Post, Comment, Reaction
    from fbposts.posts import get_post

    post = Post.objects.get(pk=1)
    post_json = get_post(1)
    assert post.id == post_json["post_id"]
    assert post.posted_by_id == post_json["posted_by"]["user_id"]
    assert post.post_content == post_json["post_content"]
    assert post.posted_at.strftime("%y-%m-%d %H:%M:%S.%f") == post_json["posted_at"]

    reactions = Reaction.objects.filter(post_id=1).order_by('id')
    comments = Comment.objects.filter(post_id=1).order_by('id')

    db_reaction_list = create_reactions_list(reactions)
    json_reaction_list = (post_json["reactions"]["type"])
    assert db_reaction_list == json_reaction_list

    assert len(reactions) == post_json["reactions"]["count"]
    assert len(comments) == post_json["comments_count"]

    comments_json_list = []
    for comment_json, comment in zip(post_json["comments"], comments):

        comments_db_json = dict()
        comments_db_json["comment_id"] = comment.id
        comments_db_json["commenter"] = dict()
        comments_db_json["commenter"]["user_id"] = comment.commenter_id
        comments_db_json["commenter"]["name"] = comment.commenter.username
        comments_db_json["commenter"]["profile_pic_url"] = comment.commenter.pic_url
        comments_db_json["commented_at"] = comment.commented_at.strftime("%y-%m-%d %H:%M:%S.%f")
        comments_db_json["comment_content"] = comment.comment_content

        reactions = Reaction.objects.filter(comment_id=comment.id).order_by('id')
        replies = Comment.objects.filter(comment_id=comment.id).order_by('id')

        db_reaction_list = create_reactions_list(reactions)

        comments_db_json["reactions"] = dict()

        comments_db_json["reactions"]["type"] = db_reaction_list
        comments_db_json["reactions"]["count"] = len(reactions)

        comments_db_json["replies_count"] = len(replies)

        replies_json_list = []
        for reply, reply_json in zip(replies, comment_json["replies"]):
            replies_db_json = dict()
            replies_db_json["comment_id"] = reply.id
            replies_db_json["commenter"] = dict()
            replies_db_json["commenter"]["user_id"] = reply.commenter_id
            replies_db_json["commenter"]["name"] = reply.commenter.username
            replies_db_json["commenter"]["profile_pic_url"] = reply.commenter.pic_url
            replies_db_json["commented_at"] = reply.commented_at.strftime("%y-%m-%d %H:%M:%S.%f")
            replies_db_json["comment_content"] = reply.comment_content

            reactions = Reaction.objects.filter(comment_id=reply.id).order_by('id')

            db_reaction_list = create_reactions_list(reactions)

            replies_db_json["reactions"] = dict()
            replies_db_json["reactions"]["count"] = len(reactions)
            replies_db_json["reactions"]["type"] = db_reaction_list

            replies_json_list.append(replies_db_json)
        comments_db_json["replies"] = replies_json_list
        comments_json_list.append(comments_db_json)
    assert comments_json_list == post_json["comments"]


def create_reactions_list(reactions):
    db_reaction_list = []
    for reaction in reactions:
        if not (reaction.reaction_type in db_reaction_list):
            db_reaction_list.append(reaction.reaction_type)
    return db_reaction_list


@pytest.mark.django_db
def test_get_user_posts_with_non_existing_user_id_raises_integrity_error():
    from fbposts.posts import get_user_posts
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        get_user_posts(0)


@pytest.mark.django_db
def test_get_user_posts_returns_only_the_posts_of_given_user(
        create_two_users_two_posts_each_and_comments_replies_to_posts_and_reactions_to_posts_comments_replies):
    from fbposts.posts import get_user_posts
    from fbposts.models import Post

    posts_json = get_user_posts(1)
    posts = Post.objects.filter(posted_by_id=1)

    for post_json, post in zip(posts_json, posts):
        assert post_json["post_id"] == post.id

    posts_json = get_user_posts(2)
    posts = Post.objects.filter(posted_by_id=2)

    for post_json, post in zip(posts_json, posts):
        assert post_json["post_id"] == post.id


@pytest.mark.django_db
def test_get_posts_with_more_positive_reactions(create_users_posts_reactions_data):
    from fbposts.posts import get_posts_with_more_positive_reactions

    list_of_post_ids = get_posts_with_more_positive_reactions()
    list_of_post_ids.sort()
    verified_list = [2, 3]
    assert list_of_post_ids == verified_list


@pytest.mark.django_db
def test_get_posts_reacted_by_user_with_non_existing_user_id_raises_integrity_error(create_users_posts_reactions_data):
    from fbposts.posts import get_posts_reacted_by_user
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        get_posts_reacted_by_user(0)


@pytest.mark.django_db
def test_get_posts_reacted_by_user_returns_correct_results(create_users_posts_reactions_data):
    from fbposts.posts import get_posts_reacted_by_user
    from fbposts.models import Reaction

    posts_json = get_posts_reacted_by_user(1)
    post_list_1 = []
    post_list_2 = []
    posts = Reaction.objects.filter(reactor_id=1).filter(comment=None)

    for post_json, post in zip(posts_json, posts):
        post_list_1.append(post_json["post_id"])
        post_list_2.append(post.post_id)

    assert post_list_2.sort() == post_list_1.sort()


@pytest.mark.django_db
def test_get_reactions_to_post_with_non_existing_post_id_raises_integrity_error():
    from fbposts.posts import get_reactions_to_post
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        get_reactions_to_post(0)


@pytest.mark.django_db
def test_get_reactions_to_post_returns_correct_result(create_users_posts_reactions_data):
    from fbposts.posts import get_reactions_to_post
    from fbposts.models import Reaction

    reactions = Reaction.objects.filter(post_id=1)
    reactions_json = get_reactions_to_post(1)

    for reaction, reaction_json in zip(reactions, reactions_json):
        assert reaction.reactor_id == reaction_json["user_id"]
        assert reaction.reaction_type == reaction_json["reaction"]


@pytest.mark.django_db
def test_delete_post_deleting_post_does_not_exist_raises_error():
    from fbposts.posts import delete_post
    from fbposts.models import Post

    with pytest.raises(Post.DoesNotExist):
        delete_post(1)


@pytest.mark.django_db
def test_delete_post_deletes_row_in_db(create_user_and_post):
    from fbposts.posts import delete_post
    from fbposts.models import Post

    delete_post(1)
    assert len(Post.objects.filter(pk=1)) == 0
