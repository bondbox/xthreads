# coding:utf-8

import unittest

from xkits_thread.lock import NamedLock


class TestNamedLock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.namedlock: NamedLock[str] = NamedLock()
        cls.lockname: str = "test"

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_lock(self):
        self.assertEqual(len(self.namedlock), 0)
        self.assertNotIn(self.lockname, self.namedlock)
        self.assertIsInstance(self.namedlock.lookup(self.lockname), NamedLock.LockItem)  # noqa:E501
        self.assertEqual(len(self.namedlock), 1)
        self.assertIn(self.lockname, self.namedlock)
        for lock in self.namedlock:
            with lock.lock:
                self.assertIs(self.namedlock[lock.name], lock.lock)


if __name__ == "__main__":
    unittest.main()
