from ptest.decorator import TestClass, Test, BeforeSuite
from ptest.assertion import fail, assert_true
from ptest.plogger import preporter
from ptest import config
import server
import client



@TestClass(run_mode="parallel")  # the test cases in this class will be executed by multiple threads
class PTestClass:
    @BeforeSuite()
    def before_suite(self):
        server.main()

    @Test()
    def test_1(self):
        client.run()

    @Test()
    def test_2():


    @Test(enabled=False)  # won't be run
    def test_3(self):


    # @AfterMethod(always_run=True, description="Clean up")
    # def after(self):
    #     preporter.info
