import pytest


@pytest.fixture
def create_user_and_post():
    from fbposts.models import User, Post

    User.objects.create(id=1, username='rachana', pic_url='samlple.png')
    Post.objects.create(id=1, posted_by_id=1, post_content="post")


@pytest.fixture
def create_user_post_comment():
    from fbposts.models import User, Post, Comment

    User.objects.create(id=1, username='rachana', pic_url='samlple.png')
    Post.objects.create(id=1, posted_by_id=1, post_content="post")
    Comment.objects.create(id=1, post_id=1, commenter_id=1, comment_content="comment")


@pytest.fixture
def create_user_post_reaction():
    from fbposts.models import User, Post, Reaction

    User.objects.create(id=1, username='rachana', pic_url='samlple.png')
    Post.objects.create(id=1, posted_by_id=1, post_content="post")
    Reaction.objects.create(id=1, reactor_id=1, post_id=1, reaction_type="LIKE")


@pytest.fixture
def create_user_post_comment_reaction():
    from fbposts.models import User, Post, Comment, Reaction

    User.objects.create(id=1, username='rachana', pic_url='samlple.png')
    Post.objects.create(id=1, posted_by_id=1, post_content="post")
    Comment.objects.create(id=1, post_id=1, commenter_id=1, comment_content="comment")
    Reaction.objects.create(id=1, reactor_id=1, comment_id=1, reaction_type="LIKE")


@pytest.fixture
def create_two_users_two_posts_each_and_comments_replies_to_posts_and_reactions_to_posts_comments_replies():
    from fbposts.models import User, Post, Reaction, Comment

    User.objects.create(id=1, username='user1', pic_url='samlple1.png')
    User.objects.create(id=2, username='user2', pic_url='samlple2.png')

    Post.objects.create(id=1, posted_by_id=1, post_content="post1-user1")
    Post.objects.create(id=2, posted_by_id=1, post_content="post2-user2")
    Post.objects.create(id=3, posted_by_id=2, post_content="post1-user2")
    Post.objects.create(id=4, posted_by_id=2, post_content="post2-user2")

    Reaction.objects.create(id=1, reactor_id=1, post_id=1, reaction_type='LIKE')
    Reaction.objects.create(id=2, reactor_id=2, post_id=1, reaction_type='WOW')

    Reaction.objects.create(id=3, reactor_id=2, post_id=2, reaction_type='WOW')

    Reaction.objects.create(id=4, reactor_id=1, post_id=3, reaction_type='LIKE')
    Reaction.objects.create(id=5, reactor_id=2, post_id=3, reaction_type='WOW')

    Reaction.objects.create(id=6, reactor_id=1, post_id=4, reaction_type='WOW')

    Comment.objects.create(id=1, post_id=1, commenter_id=2, comment_content="comment")
    Comment.objects.create(id=2, comment_id=1, commenter_id=2, comment_content="reply")
    Comment.objects.create(id=5, comment_id=1, commenter_id=1, comment_content="reply2")

    Comment.objects.create(id=3, post_id=1, commenter_id=1, comment_content="comment")
    Comment.objects.create(id=4, comment_id=3, commenter_id=2, comment_content="reply")

    Reaction.objects.create(id=7, reactor_id=1, comment_id=1, reaction_type='LIKE')
    Reaction.objects.create(id=8, reactor_id=2, comment_id=1, reaction_type='LIKE')
    Reaction.objects.create(id=9, reactor_id=1, comment_id=2, reaction_type='LIKE')
    Reaction.objects.create(id=10, reactor_id=2, comment_id=2, reaction_type='LIKE')


def create_ten_users():
    from fbposts.models import User

    for i in range(1, 11):
        username = "user" + str(i)
        pic_url = "sample" + str(i) + ".png"
        User.objects.create(username=username, pic_url=pic_url)


def create_three_posts():
    from fbposts.models import Post, Reaction

    for i in range(1, 4):
        Post.objects.create(posted_by_id=i, post_content="post" + str(i))


@pytest.fixture
def create_users_posts_reactions_data():
    from fbposts.reactions import react_to_post

    create_ten_users()
    create_three_posts()
    react_to_post(1, 1, 'LIKE')
    react_to_post(2, 1, 'ANGRY')
    react_to_post(3, 1, 'SAD')
    react_to_post(4, 1, 'ANGRY')
    react_to_post(5, 1, 'SAD')

    react_to_post(1, 2, 'LIKE')
    react_to_post(2, 2, 'LOVE')
    react_to_post(3, 2, 'WOW')

    react_to_post(1, 3, 'LIKE')


@pytest.mark.django_db
def test_create_post_saved_with_same_parameters_in_db(create_user_and_post):
    from fbposts.posts import create_post
    from fbposts.models import Post

    post_id = create_post(1, "post1")
    assert len(Post.objects.all()) == 2
    post = Post.objects.get(id=post_id)
    assert post.posted_by_id == 1
    assert post.post_content == "post1"


@pytest.mark.django_db
def test_create_post_with_empty_post_content_raises_value_error(create_user_and_post):
    from fbposts.posts import create_post

    with pytest.raises(ValueError):
        post_id = create_post(1, "")


@pytest.mark.django_db
def test_create_post_with_non_existing_user_raises_integrity_error():
    from fbposts.posts import create_post
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        post_id = create_post(0, "post1")


@pytest.mark.django_db
def test_add_comment_saved_with_same_parameters_in_db(create_user_and_post):
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
def test_reply_to_comment_reply_to_reply_saved_as_reply_to_comment(create_user_post_comment):
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
def test_react_to_post_with_non_existing_user_raises_integrity_error(create_user_and_post):
    from fbposts.reactions import react_to_post
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        reaction = react_to_post(0, 1, "HAHA")


@pytest.mark.django_db
def test_react_to_post_with_non_existing_post_raises_integrity_error(create_user_and_post):
    from fbposts.reactions import react_to_post
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        reaction = react_to_post(1, 0, "HAHA")


@pytest.mark.django_db
def test_react_to_post_with_invalid_reaction_type_raises_value_error(create_user_and_post):
    from fbposts.reactions import react_to_post

    with pytest.raises(ValueError):
        reaction = react_to_post(1, 1, "HELLO")


@pytest.mark.django_db
def test_react_to_post_for_first_time_saved_with_same_parameters(create_user_and_post):
    from fbposts.reactions import react_to_post
    from fbposts.models import Reaction

    react_to_post(1, 1, "LIKE")
    reaction = Reaction.objects.get(reactor_id=1, post_id=1)
    assert reaction.reaction_type == "LIKE"


@pytest.mark.django_db
def test_react_to_post_second_time_reaction_with_different_reaction_type_updates_reaction_type_in_db(
        create_user_post_reaction):
    from fbposts.reactions import react_to_post
    from fbposts.models import Reaction

    react_to_post(1, 1, "WOW")
    reaction = Reaction.objects.get(reactor_id=1, post_id=1)
    assert reaction.reaction_type == "WOW"


@pytest.mark.django_db
def test_react_to_post_second_time_reaction_with_same_reaction_type_deletes_entry_in_db(create_user_post_reaction):
    from fbposts.reactions import react_to_post
    from fbposts.models import Reaction

    react_to_post(1, 1, "LIKE")
    with pytest.raises(Reaction.DoesNotExist):
        reaction = Reaction.objects.get(reactor_id=1, post_id=1)


@pytest.mark.django_db
def test_react_to_comment_with_non_existing_user_raises_integrity_error(create_user_post_comment):
    from fbposts.reactions import react_to_comment
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        reaction = react_to_comment(0, 1, "HAHA")


@pytest.mark.django_db
def test_react_to_comment_with_non_existing_post_raises_integrity_error(create_user_post_comment):
    from fbposts.reactions import react_to_comment
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        reaction = react_to_comment(1, 0, "HAHA")


@pytest.mark.django_db
def test_react_to_comment_with_invalid_reaction_type_raises_value_error(create_user_post_comment):
    from fbposts.reactions import react_to_comment

    with pytest.raises(ValueError):
        reaction = react_to_comment(1, 1, "HELLO")


@pytest.mark.django_db
def test_react_to_comment_for_first_time_saved_with_same_parameters(create_user_post_comment):
    from fbposts.reactions import react_to_comment
    from fbposts.models import Reaction

    with pytest.raises(Reaction.DoesNotExist):
        Reaction.objects.get(reactor_id=1, comment_id=1)

    react_to_comment(1, 1, "LIKE")
    reaction = Reaction.objects.get(reactor_id=1, comment_id=1)
    assert reaction.reaction_type == "LIKE"


@pytest.mark.django_db
def test_react_to_comment_second_time_reaction_with_different_reaction_type_updates_reaction_type_in_db(
        create_user_post_comment_reaction):
    from fbposts.reactions import react_to_comment
    from fbposts.models import Reaction

    reaction = Reaction.objects.get(reactor_id=1, comment_id=1)
    assert reaction.reaction_type == "LIKE"

    react_to_comment(1, 1, "WOW")
    reaction = Reaction.objects.get(reactor_id=1, comment_id=1)
    assert reaction.reaction_type == "WOW"


@pytest.mark.django_db
def test_react_to_comment_second_time_reaction_with_same_reaction_type_deletes_entry_in_db(
        create_user_post_comment_reaction):
    from fbposts.reactions import react_to_comment
    from fbposts.models import Reaction

    react_to_comment(1, 1, "LIKE")
    with pytest.raises(Reaction.DoesNotExist):
        reaction = Reaction.objects.get(reactor_id=1, comment_id=1)


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

    reactions = Reaction.objects.filter(post_id=1)
    comments = Comment.objects.filter(post_id=1)

    db_reaction_list = []
    json_reaction_list = []
    for reaction in reactions:
        db_reaction_list.append(reaction.reaction_type)
        json_reaction_list(post_json["reactions"]["type"])
    assert db_reaction_list == json_reaction_list

    assert len(reactions) == post_json["reactions"]["count"]
    assert len(comments) == post_json["comments_count"]

    for comment_json, comment in zip(post_json["comments"], comments):
        assert comment.id == comment_json["comment_id"]
        assert comment.commenter_id == comment_json["commenter"]["user_id"]
        assert comment.commented_at.strftime("%y-%m-%d %H:%M:%S.%f") == comment_json["commented_at"]

        reactions = Reaction.objects.filter(comment_id=comment.id)
        replies = Comment.objects.filter(comment_id=comment.id)

        for reaction in reactions:
            assert reaction.reaction_type in comment_json["reactions"]["type"]

        assert len(reactions) == comment_json["reactions"]["count"]
        assert comment_json["replies_count"] == len(replies)

        for reply, reply_json in zip(replies, comment_json["replies"]):
            assert reply.id == reply_json["comment_id"]
            assert reply.commenter_id == reply_json["commenter"]["user_id"]
            assert reply.commented_at.strftime("%y-%m-%d %H:%M:%S.%f") == reply_json["commented_at"]
            assert reply.comment_content == reply_json["comment_content"]

            reactions = Reaction.objects.filter(comment_id=reply.id)

            for reaction in reactions:
                assert reaction.reaction_type in reply_json["reactions"]["type"]

            assert len(reactions) == reply_json["reactions"]["count"]


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
def test_reaction_metrics_to_post_with_non_existing_post_id_raises_integrity_error(create_users_posts_reactions_data):
    from fbposts.reactions import get_reaction_metrics
    from django.db.utils import IntegrityError

    with pytest.raises(IntegrityError):
        metrics = get_reaction_metrics(0)


@pytest.mark.django_db
def test_get_reaction_metrics_returns_correct_results(create_users_posts_reactions_data):
    from fbposts.reactions import get_reaction_metrics

    metrics_dict = get_reaction_metrics(1)
    assert metrics_dict["LIKE"] == 1
    assert metrics_dict["SAD"] == 2
    assert metrics_dict["ANGRY"] == 2


@pytest.mark.django_db
def test_get_total_reaction_count_returns_correct_results(create_users_posts_reactions_data):
    from fbposts.reactions import get_total_reaction_count

    total_count_dict = get_total_reaction_count()
    assert total_count_dict[1] == 5
    assert total_count_dict[2] == 3
    assert total_count_dict[3] == 1


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
