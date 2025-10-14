# coding:utf-8

from os import getpid
from unittest import TestCase
from unittest import main
from unittest import mock

from xkits_thread.proc import Process
from xkits_thread.proc import Processes


class TestProc(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.instance = Processes()

    def tearDown(self):
        pass

    def test_add(self):
        process: Process = self.instance[getpid()]
        with mock.patch.object(process, "is_running") as mock_running:
            mock_running.side_effect = [True, False, False]
            for proc in self.instance:
                self.assertIs(process, proc)
            self.instance.add(process)
            for proc in self.instance:
                self.assertIs(process, proc)
        self.assertEqual(len(self.instance), 0)

    def test_select(self):
        self.instance.select("python3")
        self.instance.select("systemd")
        self.instance.select("systemd")

    def test_search(self):
        for proc in Processes.search("systemd"):
            self.assertEqual(proc.name(), "systemd")


if __name__ == "__main__":
    main()
