# coding:utf-8

from time import sleep
import unittest

from xkits_thread.executor import ThreadPool
from xkits_thread.executor import hourglass


class TestExecute(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @hourglass(0.5)
    def fake_hourglass(self, value: float = 1.0):
        return sleep(value)

    def test_hourglass(self):
        self.assertRaises(TimeoutError, self.fake_hourglass)
        self.assertIsNone(self.fake_hourglass(0.1))


class TestThreadPool(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_join(self):
        def handle() -> bool:
            return True

        with ThreadPool(1) as pool:
            pool.submit(handle)
            pool.submit(handle)
            pool.submit(handle)
            pool.submit(handle)
            pool.submit(handle)
            pool.cmds.stdout("unittest")
            self.assertIsInstance(pool.alive_threads, set)
            self.assertIsInstance(pool.other_threads, set)
            self.assertIsInstance(pool.other_alive_threads, set)
            pool.shutdown()


if __name__ == "__main__":
    unittest.main()
