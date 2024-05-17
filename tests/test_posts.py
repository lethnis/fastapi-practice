import pytest

from app.schemas import PostVote, PostResponse


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200

    response = [PostVote(**i) for i in response.json()]

    assert len(response) == len(test_posts)
    assert all([response[i].Post.id == test_posts[i].id for i in range(len(response))])
    assert all([response[i].Post.user_id == test_posts[i].user_id for i in range(len(response))])


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    response = authorized_client.get("posts/9999999")
    assert response.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    response = PostVote(**response.json())
    assert response.Post.id == test_posts[0].id
    assert response.Post.user_id == test_posts[0].user_id
    assert response.Post.content == test_posts[0].content
    assert response.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, is_published", [("test title", "test content", True)])
def test_create_post(authorized_client, test_user, title, content, is_published):
    response = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "is_published": is_published}
    )
    assert response.status_code == 201
    response = PostResponse(**response.json())
    assert response.title == title
    assert response.content == content
    assert response.is_published == is_published
    assert response.user_id == test_user["id"]


def test_unauthorized_create_post(client, test_user):
    response = client.post("/posts/", json={"title": "", "content": ""})
    assert response.status_code == 401, "Unauthorized user can't create posts."


def test_unauthorized_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401, "Unauthorized user can't delete posts."


def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204, "Authorized user can delete their own posts"


def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    response = authorized_client.delete("posts/9999999")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403, "One user can't delete other user's posts."


def test_update_post(authorized_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated content", "id": test_posts[0].id}
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    assert response.status_code == 200
    response = PostResponse(**response.json())
    assert response.content == "updated content"
    assert response.title == "updated title"


def test_update_other_user_post(authorized_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated content", "id": test_posts[3].id}
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403


def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {"title": "updated title", "content": "updated content", "id": test_posts[0].id}
    response = authorized_client.put("/posts/999999", json=data)
    assert response.status_code == 404


def test_unauthorized_update_post(client, test_user, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401, "Unauthorized user can't update posts."
