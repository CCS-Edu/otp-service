import pytest
from Scripts import app


@pytest.fixture  # define a function can be used in all the tests
def client():
    with app.test_client() as client:
        yield client  # similar to use return, but this makes the client clean up after the complete test

#  when a function call "client" fixture, the function above is called automatic
#  the test function can use the test client to make requests and test its behaviour


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 201
    assert b"Your otp is" in response.data


def test_invalid_otp_submission(client):
    with client.session_transaction() as session:  # Create a context that the client can interact with the session object
        session["response"] = "1234"  # Set the session response to an expected value
    data = {"otp": "4321", "username": "user1", "password": "pass1"}
    response = client.post("/verifyotp", json=data)
    assert response.status_code == 401
    assert b"You are not authorized, Sorry" in response.data


# def test_valid_otp_submission(client):
#     with client.session_transaction() as session:
#         session["response"] = "1234"
#     data = {"otp": "1234", "username": "user1", "password": "pass1"}
#     response = client.post("/verifyotp", json=data)
#     assert response.status_code == 201
#     assert b"" in response.data


def test_valid_login(client):
    with client.session_transaction() as session:
        session["response"] = "1234"
    data = {"otp": "1234", "username": "user1", "password": "pass1"}
    response = client.post("/verifyotp", json=data)
    assert response.status_code == 201
    assert b"token" in response.data


def test_invalid_login(client):
    with client.session_transaction() as session:
        session["response"] = "1234"
    data = {"otp": "1234", "username": "user1", "password": "pass2"}
    response = client.post("/verifyotp", json=data)
    assert response.status_code == 200
    assert b"Your username or password is incorrect" in response.data


def test_invalid_json(client):
    # with client.session_transaction() as session:
    #     session["response"] = "1234"
    data = {"otp": "1234", "password": "pass2"}
    response = client.post("/verifyotp", json=data)
    assert response.status_code == 500
    # assert b"Your username or password is incorrect" in response.data


def test_invalid_link(client):
    response = client.post("/dsadasd")
    assert response.status_code == 404
