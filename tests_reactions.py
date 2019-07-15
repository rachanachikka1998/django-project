import pytest
from fixtures import create_user_and_post, create_user_post_reaction, create_user_post_comment, \
    create_users_posts_reactions_data, create_user_post_comment_reaction


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
