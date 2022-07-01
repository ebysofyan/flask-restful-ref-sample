from flask.testing import FlaskClient

from movie_api.entity.movie import MovieEntity


def test_get_movies(client: FlaskClient):
    r = client.get("/api/movies")
    assert r.status_code == 200


def test_create_movie_invalid_payload(client: FlaskClient):
    r = client.post("/api/movies", json={"name": "new title"})
    assert r.status_code == 400


def test_create_movie_valid_payload(client: FlaskClient):
    r = client.post(
        "/api/movies",
        json=MovieEntity(
            title="Hanyalah title",
            description="Yaa gitu...",
        ).asdict(),
    )
    assert r.status_code in [200, 201]
