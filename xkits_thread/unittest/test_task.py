# coding:utf-8

from time import sleep
from time import time
import unittest

from xkits_thread.executor import ThreadPool
from xkits_thread.task import DaemonTaskJob
from xkits_thread.task import DelayTaskJob
from xkits_thread.task import TaskJob
from xkits_thread.task import TaskPool


class TestTaskPool(unittest.TestCase):

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

    def test_job(self):
        def handle(value: bool) -> bool:
            return value

        def result(job: TaskJob):
            return job.result

        self.assertIsInstance(DelayTaskJob.create_task(handle, False), TaskJob)
        job: DelayTaskJob = DelayTaskJob.create_delay_task(0.01, handle, False)
        self.assertIsInstance(job, DelayTaskJob)
        self.assertRaises(LookupError, result, job)
        self.assertLess(job.running_timer.created_time, time())
        self.assertEqual(job.running_timer.started_time, 0.0)
        self.assertEqual(job.running_timer.stopped_time, 0.0)
        self.assertFalse(job.running_timer.started)
        self.assertFalse(job.running_timer.stopped)
        self.assertEqual(job.id, -1)
        self.assertTrue(job.run())
        self.assertFalse(job.result)
        self.assertIsNone(job.renew(1.0))
        self.assertLess(job.running_timer.created_time, time())
        self.assertLess(job.running_timer.started_time, time())
        self.assertLess(job.running_timer.stopped_time, time())
        self.assertFalse(job.running_timer.started)
        self.assertTrue(job.running_timer.stopped)
        self.assertIsNone(job.barrier())
        self.assertIsNone(job.restart())
        job.running_timer.startup()
        self.assertTrue(job.running_timer.started)
        self.assertFalse(job.running_timer.stopped)
        self.assertFalse(job.run())
        self.assertFalse(job.running_timer.started)
        self.assertTrue(job.running_timer.stopped)

        def sleep_task(seconds: float = 1.0):
            sleep(seconds)

        def run_job(job: TaskJob):
            job.run()

        with ThreadPool(1) as pool:
            task: TaskJob = TaskJob.create_task(sleep_task, 0.5)
            pool.submit(run_job, task)
            task.shutdown()

    def test_daemon_job_1(self):
        def handle():
            sleep(0.01)

        job: DaemonTaskJob = DaemonTaskJob.create_daemon_task(handle)
        self.assertLess(job.running_timer.created_time, time())
        self.assertEqual(job.running_timer.started_time, 0.0)
        self.assertEqual(job.running_timer.stopped_time, 0.0)
        self.assertEqual(job.daemon_counter.total, 0)
        self.assertEqual(job.daemon_counter.success, 0)
        self.assertEqual(job.daemon_counter.failure, 0)
        self.assertFalse(job.daemon_running)
        job.run_in_background()
        self.assertLess(job.running_timer.created_time, time())
        self.assertLess(job.running_timer.started_time, time())
        self.assertTrue(job.daemon_running)
        job.barrier()
        self.assertLess(job.running_timer.created_time, time())
        self.assertLess(job.running_timer.started_time, time())
        self.assertGreater(job.daemon_counter.total, 0)
        self.assertGreater(job.daemon_counter.success, 0)
        self.assertEqual(job.daemon_counter.failure, 0)
        self.assertTrue(job.daemon_running)
        job.shutdown()
        self.assertLess(job.running_timer.created_time, time())
        self.assertLess(job.running_timer.started_time, time())
        self.assertLess(job.running_timer.stopped_time, time())
        self.assertGreater(job.daemon_counter.total, 0)
        self.assertGreater(job.daemon_counter.success, 0)
        self.assertEqual(job.daemon_counter.failure, 0)
        self.assertFalse(job.daemon_running)

    def test_daemon_job_2(self):
        def handle():
            raise Exception("test")

        job: DaemonTaskJob = DaemonTaskJob.create_daemon_task(handle)
        self.assertLess(job.running_timer.created_time, time())
        self.assertEqual(job.running_timer.started_time, 0.0)
        self.assertEqual(job.running_timer.stopped_time, 0.0)
        self.assertEqual(job.daemon_counter.total, 0)
        self.assertEqual(job.daemon_counter.success, 0)
        self.assertEqual(job.daemon_counter.failure, 0)
        self.assertFalse(job.daemon_running)
        job.run_in_background()
        self.assertLess(job.running_timer.created_time, time())
        self.assertLess(job.running_timer.started_time, time())
        self.assertTrue(job.daemon_running)
        job.barrier()
        self.assertLess(job.running_timer.created_time, time())
        self.assertLess(job.running_timer.started_time, time())
        self.assertGreater(job.daemon_counter.total, 0)
        self.assertEqual(job.daemon_counter.success, 0)
        self.assertGreater(job.daemon_counter.failure, 0)
        self.assertTrue(job.daemon_running)
        job.shutdown()
        self.assertLess(job.running_timer.created_time, time())
        self.assertLess(job.running_timer.started_time, time())
        self.assertLess(job.running_timer.stopped_time, time())
        self.assertGreater(job.daemon_counter.total, 0)
        self.assertEqual(job.daemon_counter.success, 0)
        self.assertGreater(job.daemon_counter.failure, 0)
        self.assertFalse(job.daemon_running)

    def test_task(self):
        def lock(tasker: TaskPool, index: int):
            if index % 2 == 1:
                raise Exception(f"task{index}")

        with TaskPool(8) as tasker:
            tasker.submit_job(TaskJob(123456, lock, tasker, 0))
            tasker.submit_delay_task(0.01, lock, tasker, 1)
            tasker.submit_delay_task(0.1, lock, tasker, 2)
            tasker.submit_task(lock, tasker, 3)
            tasker.submit_task(lock, tasker, 4)
            tasker.startup()
            sleep(0.1)
            tasker.barrier()
            self.assertEqual(tasker.status_counter.total, 5)
            self.assertEqual(tasker.status_counter.success, 3)
            self.assertEqual(tasker.status_counter.failure, 2)
            self.assertTrue(tasker.running)
            tasker.shutdown()
            self.assertFalse(tasker.running)
            tasker.startup()
            self.assertTrue(tasker.running)


if __name__ == "__main__":
    unittest.main()
