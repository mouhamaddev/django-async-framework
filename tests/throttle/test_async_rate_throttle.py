import pytest
import time
from async_framework.throttle import AsyncRateThrottle

from tests import django_config
django_config.configure()


class DummyRequest:
    def __init__(self, ip="127.0.0.1"):
        self.META = {'REMOTE_ADDR': ip}


def test_parse_rate():
    throttle = AsyncRateThrottle("5/second")
    assert throttle.num_requests == 5
    assert throttle.duration == 1

    throttle = AsyncRateThrottle("10/minute")
    assert throttle.num_requests == 10
    assert throttle.duration == 60

    throttle = AsyncRateThrottle("100/hour")
    assert throttle.num_requests == 100
    assert throttle.duration == 3600

    with pytest.raises(ValueError):
        AsyncRateThrottle("10/day")


@pytest.mark.asyncio
async def test_allows_under_limit():
    throttle = AsyncRateThrottle("3/second")
    request = DummyRequest()

    assert await throttle.allow_request(request)
    assert await throttle.allow_request(request)
    assert await throttle.allow_request(request)


@pytest.mark.asyncio
async def test_blocks_over_limit():
    throttle = AsyncRateThrottle("2/second")
    request = DummyRequest()

    assert await throttle.allow_request(request)
    assert await throttle.allow_request(request)
    assert not await throttle.allow_request(request)


@pytest.mark.asyncio
async def test_expires_old_requests(monkeypatch):
    throttle = AsyncRateThrottle("2/second")
    request = DummyRequest()

    now = time.time()

    monkeypatch.setattr(time, "time", lambda: now)
    assert await throttle.allow_request(request)
    assert await throttle.allow_request(request)

    # Now simulate 2 seconds later
    monkeypatch.setattr(time, "time", lambda: now + 2)
    assert await throttle.allow_request(request)


@pytest.mark.asyncio
async def test_different_ips_have_separate_limits():
    throttle = AsyncRateThrottle("1/second")

    req1 = DummyRequest(ip="1.1.1.1")
    req2 = DummyRequest(ip="2.2.2.2")

    assert await throttle.allow_request(req1)
    assert not await throttle.allow_request(req1)

    assert await throttle.allow_request(req2)


@pytest.mark.asyncio
async def test_default_identifier_when_no_ip():
    throttle = AsyncRateThrottle("1/second")
    request = DummyRequest(ip=None)
    request.META.pop('REMOTE_ADDR', None)

    assert await throttle.allow_request(request)
    assert not await throttle.allow_request(request)
