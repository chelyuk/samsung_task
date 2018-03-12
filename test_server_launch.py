# !/usr/bin/env python

from ptest.decorator import TestClass, Test, AfterSuite
from ptest.assertion import assert_true, assert_false
import server


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@TestClass(run_mode="singleline")
class PTestClass:

    # positive
    @Test(data_provider=["127.0.0.1", "localhost"])
    def test1(self, address):
        args = Namespace(host=address, port=80)
        server.main(args)
        assert_true()

    # negative
    @Test(data_provider=["8.8.8.8", "500.500.500.50"])
    def test1_2(self, address):
        args = Namespace(host=address, port=80)
        server.main(args)
        assert_false()

    # positive
    @Test(data_provider=[0, 80, 8080, 65535])
    def test_2(self, port, request):
        args = Namespace(port=port)
        server.main(args)
        assert_true()

    # negative
    @Test(data_provider=[(0, 500000, -545)])
    def test_2_2(self, port):
        args = Namespace(port=port)
        server.main(args)
        assert_false()

    # TBD need to close server after tests complete
    # @AfterSuite(always_run=True, description="Clean up")
    # def after(self):
        # server.close_server()
