# !/usr/bin/env python

from ptest.decorator import TestClass, Test, BeforeSuite, AfterSuite, AfterMethod
from ptest.assertion import assert_equals
import server
import pycurl


def request_get(url, port):
    self = pycurl.Curl()
    self.setopt(self.URL, url)
    self.setopt(self.HTTPGET, True)
    self.setopt(self.PROXYPORT, port)
    self.setopt(self.HTTPHEADER, ['Content-type: application/json'])
    return self


def request_post(url, port, message):
    self = pycurl.Curl()
    self.setopt(self.URL, url)
    self.setopt(self.POST, True)
    self.setopt(self.WRITEDATA, message)
    self.setopt(self.PROXYPORT, port)
    self.setopt(self.HTTPHEADER, ['Content-type: application/json'])
    return self


def request_perform(request):
    try:
        request.perform()
    except pycurl.error as error:
        errno, errstr = error
        print('An error occurred: ', errstr)
    return request


def close_session(self):
    self.close()


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@TestClass(run_mode="singleline")
class PTestClass:
    @BeforeSuite()
    def before_suite(self):
        args = Namespace(host="127.0.0.1", port='80')
        print("Arguments = ", args)
        server.main(args)

    @Test(data_provider=[("127.0.0.1", "localhost"), (80, 8080, 65535), ("message1", "message123123213123", "1231232")])
    def test1(self, host, port, message):
        self = request_perform(request_post(host, port))
        assert_equals(self.getinfo(self.RESPONSE_CODE), 200)

    @Test(data_provider=[("127.0.0.1", "localhost"), (80, 8080, 65535)])
    def test1_2(self, host, port):
        self = request_perform(request_get(host, port))
        assert_equals(self.getinfo(self.RESPONSE_CODE), 200)

    @Test(data_provider=[("127.0.0.1", "localhost"), (8, 8080, 65535)])
    def test_2(self, host, port):
        self = request_perform(request_get(host, port))
        assert_equals(self.getinfo(self.RESPONSE_CODE), 400)

    @AfterMethod
    def after_method(self):
        close_session(self)

    # TBD need to close server after tests complete
    # @AfterSuite(always_run=True, description="Clean up")
    # def after(self):
        # server.close_server()
