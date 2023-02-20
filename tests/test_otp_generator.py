# import pytest
from otp_generator import OTPGenerator


def test_generate_otp():
    # Create an instance of the OTPGenerator class with length=8
    otp_generator = OTPGenerator(length=8)

    # Generate an OTP
    otp = otp_generator.generate_otp()

    # Check that the length of the OTP is correct
    assert len(otp) == 8

    # Check that the OTP only contains digits
    assert otp.isnumeric()

    # Check that generating multiple OTPs does not produce the same OTP
    otp2 = otp_generator.generate_otp()
    assert otp != otp2
