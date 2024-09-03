

from rest_framework.throttling import UserRateThrottle


class UserRateThrottleByMinute(UserRateThrottle):
    rate = '3/minute'
