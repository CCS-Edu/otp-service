import math
import random
import time


# random number with 6 characters
def create_otp():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
        # print(random.random())
    return OTP


def verify_otp(opt, input: str):
    return opt == input.strip()


def run_otp(start_time, OTP):
    while True:
        if time.perf_counter() - start_time > 10:
            print("OPT was expired")
            return False

        otp_input = input("Enter Your OTP >>: ")

        if verify_otp(otp_input, OTP):
            print("Verified\n")
            return False
        else:
            print("Please Check your OTP again\n")


def run():
    run = True
    while run:
        print("Enter 1 to send OTP \nEnter q to Quit")
        choice = input()

        if choice == "1":
            OPT = create_otp()
            print(OPT)
            start_time = time.perf_counter()

            active_opt = True
            while active_opt:
                active_opt = run_otp(start_time, OPT)

        elif choice == "q":
            run = False


if __name__ == "__main__":
    run()
