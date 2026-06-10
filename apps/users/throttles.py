from rest_framework.throttling import AnonRateThrottle

class SignupThrottle(AnonRateThrottle):
    scope = 'signup'

class OtpThrottle(AnonRateThrottle):
    scope = 'otp'

