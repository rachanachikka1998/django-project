import pytest
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


@pytest.mark.django_db
def test_get_post_returns_same_values_in_db(create_two_users_two_posts_each_and_comments_replies_to_posts_and_reactions_to_posts_comments_replies):
    from fbposts.models import Post, Comment, Reaction
    from fbposts.posts import get_post
    post = Post.objects.get(pk=1)
    post_json = get_post(1)
    assert post.id == post_json["post_id"]
    assert post.posted_by_id == post_json["posted_by"]["user_id"]
    assert post.post_content == post_json["post_content"]
    assert post.posted_at.strftime("%y-%m-%d %H:%M:%S.%f") == post_json["posted_at"]

    reactions = Reaction.objects.filter(post_id=1).order_by('-id')
    comments = Comment.objects.filter(post_id=1).order_by('-id')

    db_reaction_list = []
    for reaction in reactions:
        db_reaction_list.append(reaction.reaction_type)
    json_reaction_list = (post_json["reactions"]["type"])
    db_reaction_list.sort()
    assert db_reaction_list == json_reaction_list
