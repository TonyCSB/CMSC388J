import pytest

from types import SimpleNamespace
import random
import string

from flask_app.forms import SearchForm, MovieReviewForm
from flask_app.models import User, Review


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200

    search = SimpleNamespace(search_query="guardians", submit="Search")
    form = SearchForm(formdata=None, obj=search)
    response = client.post("/", data=form.data, follow_redirects=True)

    assert b"Guardians of the Galaxy" in response.data


@pytest.mark.parametrize(
    ("query", "message"),
    (
        ("", b"This field is required"),
        ("s", b"Too many results"),
        ("Lorem ipsum dolor sit amet", b"Movie not found"),
        ("a" * 101, b"Field must be between 1 and 100 characters long"),
    )
)
def test_search_input_validation(client, query, message):
    search = SimpleNamespace(
        search_query=query,
        submit="Search",
    )
    form = SearchForm(formdata=None, obj=search)
    response = client.post("/", data=form.data, follow_redirects=True)

    print(response.data)
    assert message in response.data


def test_movie_review(client, auth):
    guardians_id = "tt2015381"
    url = f"/movies/{guardians_id}"
    resp = client.get(url)

    assert resp.status_code == 200

    auth.register()
    auth.login()

    randomReview = "".join(random.choice(string.ascii_letters) for i in range(10))
    review = SimpleNamespace(
        text=randomReview,
        submit="Enter Comment",
    )
    form = MovieReviewForm(formdata=None, obj=review)
    response = client.post(url, data=form.data, follow_redirects=True)

    assert str.encode(randomReview) in response.data

    assert Review.objects(content=randomReview).first()


@pytest.mark.parametrize(
    ("movie_id", "message"),
    (
        ("", b"404 - Page Not Found"),
        ("tt", b"Incorrect IMDb ID"),
        ("123456789", b"Incorrect IMDb ID"),
        ("tt000000000", b"Incorrect IMDb ID"),
    )
)
def test_movie_review_redirects(client, movie_id, message):
    url = f"/movies/{movie_id}"
    response = client.get(url, follow_redirects=False)

    if "404" in message.decode():
        assert response.status_code == 404
    else:
        assert response.status_code == 302

    response = client.get(url, follow_redirects=True)

    assert message in response.data


@pytest.mark.parametrize(
    ("comment", "message"),
    (
        ("", b"This field is required"),
        ("a", b"Field must be between 5 and 500 characters long"),
        ("a" * 501, b"Field must be between 5 and 500 characters long"),
    )
)
def test_movie_review_input_validation(client, auth, comment, message):
    ironMan_id = "tt0371746"
    url = f"/movies/{ironMan_id}"
    resp = client.get(url)

    assert resp.status_code == 200

    auth.register()
    auth.login()

    review = SimpleNamespace(
        text=comment,
        submit="Enter Comment",
    )
    form = MovieReviewForm(formdata=None, obj=review)
    response = client.post(url, data=form.data, follow_redirects=True)

    assert message in response.data
