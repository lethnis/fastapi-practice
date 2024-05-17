import pytest
from app.schemas import PostVote, PostResponse
from app.models import VotesTable


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = VotesTable(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()
    return new_vote


def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "direction": 1})
    assert response.status_code == 201
    assert response.json() == {"message": "successfully added vote"}


def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/vote/", json={"post_id": test_vote.post_id, "direction": 1})
    assert response.status_code == 403
    assert response.json() == {"detail": f"User {test_vote.user_id} has already voted on post {test_vote.post_id}"}


def test_unvote_on_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/vote/", json={"post_id": test_vote.post_id, "direction": 0})
    assert response.status_code == 201
    assert response.json() == {"message": "successfully deleted vote"}


def test_unvote_on_post_not_voted(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "direction": 0})
    assert response.status_code == 403
    assert response.json() == {"detail": "you can't unlike post you didn't like in the first place"}


def test_vote_post_not_exist(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": 999999, "direction": 1})
    assert response.status_code == 404
    assert response.json() == {"detail": "Post with id 999999 not found"}


def test_vote_unauthorized(client, test_posts):
    response = client.post("/vote/", json={"post_id": test_posts[0].id, "direction": 1})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
