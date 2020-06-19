
from pypipe import Scheduler, MultiScheduler, FuncTask
from pypipe.task.base import Task
from pypipe.conditions import scheduler_cycles

Task.use_instance_naming = True

def myfunc():
    print("The task is running")

def failing():
    raise TypeError("Failed task")

def succeeding():
    print("Success")

def test_simple(tmpdir):
    with tmpdir.as_cwd() as old_dir:
        task_success = FuncTask(succeeding)
        task_fail = FuncTask(failing)
        scheduler = Scheduler(
            [
                task_success,
                task_fail
            ], shut_condition=scheduler_cycles >= 3
        )
        
        scheduler()

        history = task_success.get_history()
        assert 3 == (history["action"] == "run").sum()
        assert 3 == (history["action"] == "success").sum()
        assert 0 == (history["action"] == "fail").sum()

        history = task_fail.get_history()
        assert 3 == (history["action"] == "run").sum()
        assert 0 == (history["action"] == "success").sum()
        assert 3 == (history["action"] == "fail").sum()

def test_simple_multiprocess(tmpdir):
    with tmpdir.as_cwd() as old_dir:
        task_success = FuncTask(succeeding)
        task_fail = FuncTask(failing)
        scheduler = MultiScheduler(
            [
                task_success,
                task_fail
            ], shut_condition=scheduler_cycles >= 3
        )
        
        scheduler()

        history = task_success.get_history()
        assert 3 == (history["action"] == "run").sum()
        assert 3 == (history["action"] == "success").sum()
        assert 0 == (history["action"] == "fail").sum()

        history = task_fail.get_history()
        assert 3 == (history["action"] == "run").sum()
        assert 0 == (history["action"] == "success").sum()
        assert 3 == (history["action"] == "fail").sum()


def test_priority(tmpdir):
    with tmpdir.as_cwd() as old_dir:
        task_1 = FuncTask(succeeding, priority=1, name="first")
        task_2 = FuncTask(failing, priority=10, name="last")
        task_3 = FuncTask(failing, priority=5, name="second")
        scheduler = Scheduler(
            [
                task_1,
                task_2,
                task_3
            ], shut_condition=scheduler_cycles >= 1
        )
        
        scheduler()

        history = scheduler.get_history()
        history = history.set_index("action")

        task_1_start = history[(history["task_name"] == "first")].loc["run", "asctime"]
        task_3_start = history[(history["task_name"] == "second")].loc["run", "asctime"]
        task_2_start = history[(history["task_name"] == "last")].loc["run", "asctime"]
        
        assert task_1_start < task_3_start < task_2_start

