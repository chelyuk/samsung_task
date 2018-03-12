# !/usr/bin/env python

from ptest.decorator import TestClass, Test, BeforeSuite, AfterSuite
from ptest.assertion import assert_equals
import server
import client


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

    # positive
    @Test(data_provider=[("127.0.0.1", "localhost"), ("POST", "GET")])
    def test1(self, address, request):
        args = Namespace(host=address, port=80, request=request)
        client.main(args)
        assert_equals()

    # negative
    @Test(data_provider=[("8.8.8.8", "500.500.500.50"), ("POST", "GET")])
    def test1_2(self, address, request):
        args = Namespace(host=address, port=80, request=request)
        client.main(args)
        assert_equals()

    # positive
    @Test(data_provider=[(0, 80, 8080, 65535), ("POST", "GET")])
    def test_2(self, port, request):
        args = Namespace(port=port, request=request)
        client.main(args)
        assert_equals()

    # negative
    @Test(data_provider=[(80, 8080, 500000, -545), ("POST", "GET")])
    def test_2_2(self, port, request):
        args = Namespace(port=port, request=request)
        client.main(args)
        assert_equals()

    # positive
    @Test(data_provider=["message1", "!@#$%^&*()", "Совсем другой язык"])
    def test_3(self, message):
        args = Namespace(request="POST", message=message)
        client.main(args)
        assert_equals()

    # negative
    @Test(data_provider=["", 123])
    def test_3_2(self, message):
        args = Namespace(request="POST", message=message)
        client.main(args)
        assert_equals()

    @Test(data_provider=[0, 10000])
    def test_4(self, number):
        args = Namespace(equest="POST", message="test_message", qnumber=number)
        client.main(args)
        assert_equals()

    @Test(data_provider=[-1, 10001])
    def test_4_2(self, number):
        args = Namespace(equest="POST", message="test_message", qnumber=number)
        client.main(args)
        assert_equals()

    # TBD need to close server after tests complete
    # @AfterSuite(always_run=True, description="Clean up")
    # def after(self):
        # server.close_server()
