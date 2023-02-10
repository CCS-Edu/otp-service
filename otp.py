import random
import time


# ham sinh otp
def set_random_otp():
    digit = "123456789"
    length = 6
    otp = "".join(random.sample(digit, length))
    return int(otp)


# ham xoa otp sau 5 giay
def destroy_otp(otp):
    for sec in range(5, 0, -1):
        print(sec)
        time.sleep(1)
    del otp
    print("The OTP has been destroyed.")


# ham kiem tra otp
def verify_otp(user_otp, otp):
    if not otp:
        print("Invalid OTP")
    if otp == user_otp:
        print("Welcome user!")
    else:
        print("Access Denied!")

    destroy_otp(otp)


otp = set_random_otp()
print("Hello, your OTP is:", str(otp))
user_otp = int(input("Enter your OTP: "))
verify_otp(user_otp, otp)
