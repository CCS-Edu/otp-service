from flask import Flask, request, session, jsonify
import random

# from twilio.rest import Client
import jwt
import datetime

app = Flask(__name__)
app.secret_key = "helloworld"

# khoi tao username va password ban dau
users = [
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"},
    {"username": "user3", "password": "pass3"},
]


# ham tao token tu username va phut, gio, ngay, thang, hien tai
def generate_token(username):
    now = datetime.datetime.now()
    time = (
        str(now.hour)
        + "h"
        + str(now.minute)
        + "m,"
        + str(now.day)
        + "/"
        + str(now.month)
        + "/"
        + str(now.year)
    )
    payload = {"username": username, "time": time}
    secret = app.secret_key
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


# otpgenerator class
class OTPGenerator:
    def __init__(self, length=6):
        self.length = length

    def generate_otp(self):
        # Generate a random string of digits of specified length
        digits = [str(random.randint(0, 9)) for i in range(self.length)]
        otp = "".join(digits)
        return otp


"""
class otp_verifier:
    def __init__(self):
        otp = generate_otp()
        self.n = otp
        self.client = Client(
            "AC0998d21a1fff603fa3013bc3f7f55dba", "b030bb32576df29484b80130a66e685f"
        )
        self.client.messages.create(
            to=["+84384095791"], from_="+19206955933", body=self.n
        )
        session["response"] = str(otp)
"""
otp_generator = OTPGenerator(4)


@app.route("/", methods=["GET"])
def index():
    otp = otp_generator.generate_otp()
    # print(type(otp))
    # print(otp)
    session["response"] = str(
        otp
    )  # su dung session de luu bien response qua cac request khac nhau
    response = jsonify({"Your otp is": otp})
    response.status_code = 201
    return response


@app.route("/verifyotp", methods=["POST"])
def verifyotp():
    otp_usn_pwd = request.get_json()
    _otp = otp_usn_pwd["otp"]
    if otp_usn_pwd and request.method == "POST":
        s = session["response"]
        # session.pop("response", None)  # xoa response khoi session
        if s == _otp:
            username = otp_usn_pwd["username"]
            password = otp_usn_pwd["password"]
            for user in users:
                if user["username"] == username and user["password"] == password:
                    token = generate_token(username)
                    response = jsonify({"token": token})
                    response.status_code = 201
                    return response
                return jsonify("Your username or password is incorrect")
        else:
            response = jsonify("You are not authorized, Sorry")
            response.status_code = 401
            return response

    return jsonify("Please enter all otp and username and password")


if __name__ == "__main__":
    app.run(debug=True)
