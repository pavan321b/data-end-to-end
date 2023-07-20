import pytest
from api import app


# file_path = 'example.html'
def open_html(file_path):
    with open(file_path, "r") as file:
        html_content = file.read()

    return html_content.encode("utf-8").strip(b"\n")


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get("/")
    # print(response.data)

    assert response.status_code == 200
    assert open_html("templates/index.html") == response.data
    # assert response.data == b'Hello, World!'
