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
