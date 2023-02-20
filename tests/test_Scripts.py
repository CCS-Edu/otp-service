import pytest
from Scripts import app


@pytest.fixture  # define a function can be used in all the tests
def client():
    with app.test_client() as client:
        yield client    # similar to use return, but this makes the client clean up after the
# complete test

#  when a function call "client" fixture, the function above is called automatic
#  the test function can use the test client to make requests and test its behaviour


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Enter your OTP" in response.data


def test_invalid_otp_submission(client):
    with client.session_transaction() as session:
        session["response"] = "1234"  # Set the session response to an expected value

    response = client.post("/validateotp", data={"otp": "4321"})
    assert response.status_code == 200
    assert b"You are not authorized, Sorry" in response.data


def test_valid_otp_submission(client):
    with client.session_transaction() as session:
        session["response"] = "1234"  # Set the session response to an expected value

    response = client.post("/validateotp", data={"otp": "1234"})
    assert response.status_code == 200
    assert b"" in response.data


def test_valid_login(client):
    response = client.post("/login", data={"username": "user1", "password": "pass1"})
    assert response.status_code == 200
    assert b"token" in response.data


def test_invalid_login(client):
    response = client.post(
        "/login", data={"username": "user1", "password": "pass2"}
    )
    assert response.status_code == 200
    assert b"Your username or password is incorrect" in response.data
