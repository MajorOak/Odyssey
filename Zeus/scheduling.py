#!/usr/bin/env python

# =================================================================== #
#                           TINY SCHEDULER                            #
# ------------------------------------------------------------------- #
#                  Eric - 2015 05 01  (labor's day)                   #
# ------------------------------------------------------------------- #
# Just a tiny sched to learn python and train myself again            #
# We will see how it"s going...                                       #
# =================================================================== #

# ----------------
#  IMPORTS
# ----------------

import time
import threading
from controller.models import *
from django.utils import timezone


# ----------------
#  FUNCTIONS
# ----------------

def log(who, function, message, log_file):
    """simple logging function"""
    # simple print
    msg = time.ctime() + "> " + who + "@" + function + "> " + message
    print(msg)
    # log to db
    new_log = Log(type='INFO', who=who, message=message)
    new_log.save()
    # log to file
    if log_file:
        ob_file = open(log_file, 'a+')
        ob_file.write(msg)
        ob_file.write('\n')
        ob_file.close()


def log_error(who, function, message, log_file):
    """error logging function"""
    # simple print
    msg = time.ctime() + "> " + who + "@" + function + "> ERROR> " + message
    print(msg)
    # log to db
    new_log = Log(type='ERROR', who=who, message=message)
    new_log.save()
    # log to file
    if log_file:
        ob_file = open(log_file, 'a+')
        ob_file.write(msg)
        ob_file.write('\n')
        ob_file.close()


# test functions

def test_line():
    print("DING DONG DING DONG DING DONG")


def test_line_2(args):
    print(args[0])


def test_delay(args):
    try:
        delay = float(args[0])
        repeat = int(args[1])

        i = 0
        while i < repeat:
            time.sleep(delay)
            i += 1
            print("TEST DELAY : " + i.__str__())
    except Exception as ex:
        print("BOOOOOOOOM > " + ex.__str__())
        raise


# ----------------
#  CLASSES
# ----------------

class TaskerThread(threading.Thread):
    """
    This class depends of the TinyScheduler Class.
    It is used to launch thread running the real task and wait for him
    and both start and end
    """
    
    def __init__(self, tiny_scheduler, task):
        """
        Prepare all variables to be ready when the thread is run
        """
        threading.Thread.__init__(self)
        self.name = task.name

        self.tiny_scheduler = tiny_scheduler
        self.task = task

    def run(self):
        """
        1) log the start
        2) launch the chosen function
        3) log the end
        """
        function = "run"
        try:
            # logging the start
            self.tiny_scheduler.thread_list.append(self)
            log(self.name, function, "Beginning", self.tiny_scheduler.log_file)
            self.task.status = "RUNNING"
            self.task.start_date = timezone.now()
            self.task.save()

            # launch function
            if self.task.argument_list:
                arg_list = self.task.argument_list.split(",")
                globals()[self.task.command_line](arg_list)
            else:
                globals()[self.task.command_line]()

            # log the end
            log(self.name, function, "Ending", self.tiny_scheduler.log_file)
            self.tiny_scheduler.thread_list.remove(self)
            self.task.end_date = timezone.now()
            elapsed = self.task.end_date - self.task.start_date
            self.task.status = "FINISHED (" + str(elapsed) + ")"
            self.task.save()

        except Exception as ex:
            log_error(self.name, function, ex.__str__(), self.tiny_scheduler.log_file)
            self.task.status = ("CRASHED (" + ex.__str__() + ")")[:500]
            self.task.save()
            if self.tiny_scheduler.thread_list.count(self):
                self.tiny_scheduler.thread_list.remove(self)


class TinyScheduler(threading.Thread):
    """
    This class is designed to launch tasks easily
    based on the information of the scheduling database
    """

    def __init__(self, delay=1):
        """
        Create the instance of the scheduler
        Check the connection to the database
        """
        function = "init"
        try:
            threading.Thread.__init__(self)
            self.name = "TinyScheduler"
            self.thread_list = []
            self.delay = delay

            self.tsched = Scheduler.objects.first()
            if not self.tsched:
                self.tsched = Scheduler()

            # log the initialization
            self.tsched.status = "READY"
            self.tsched.to_be_ended = False
            self.tsched.save()
            self.name += "(" + self.tsched.id.__str__() + ")"
            self.log_file = self.tsched.log_file
            log(self.name, function, "The scheduler has been initialized", self.log_file)

        except Exception as ex:
            print("Damn... Houston, we got problem!", ex.__str__())
            log_error(self.name, function, ex.__str__(), self.log_file)
            self.tsched.status = ("CRASHED (" + ex.__str__() + ")")[:500]
            self.tsched.to_be_ended = False
            self.tsched.save()
                        
    def run(self):
        """
        Main function of the Tiny Scheduler :
        1) log the start of the scheduler
        2) loop on (with delay)
            2.1) check the scheduler flag "to_be_ended"
            2.2) stop if the flag is on
            2.3) check what can be launched
            2.4) get the task to be launched
            2.5) launch it
            2.6) refresh flag "to_be_ended"
        """
        function = "run"
        try:
            self.name = "SchedulingThread"
            log(self.name, function, "The scheduler has started", self.log_file)
            self.tsched = Scheduler.objects.get(id=self.tsched.id)
            self.tsched.status = "ACTIVE"
            self.tsched.start_date = timezone.now()
            self.tsched.save()

            error_count = 0
            while not self.tsched.to_be_ended:
                try:
                    # pause
                    time.sleep(self.delay)

                    # get the first ready task
                    tasks = Task.objects.filter(status="READY")
                    if tasks:
                        task = tasks[0]
                        # launch the task
                        self.launch_task(task=task)

                    # refresh tiny_scheduler
                    self.tsched = Scheduler.objects.get(id=self.tsched.id)

                except Exception as ex:
                        log_error(self.name,
                                  function,
                                  "Error in the loop (no abort) :" + ex.__str__(),
                                  self.log_file)
                        error_count += 1
                        if error_count > 20:
                            print(self.name, "Too many errors, nice aborting")
                            break

            # scheduling will be over, should we kill the children ?
            log(self.name, "run", "End of scheduling", self.log_file)
            self.tsched.status = "NOT ACTIVE"
            self.tsched.end_date = timezone.now()
            self.tsched.save()

        except Exception as big_ex:
            log_error(self.name,
                      function,
                      "Error in main thread (abort!!!) :" + big_ex.__str__(),
                      self.log_file)
            self.tsched.status = ("CRASHED (" + big_ex.__str__() + ")")[:500]
            self.tsched.end_date = timezone.now()
            self.tsched.save()
            # should we kill child threads ?

    def launch_task(self, task):
        """
        This function checks the task and then
        tries to launch it in a separate thread
        while keeping the main thread alive.
        """
        function = "launch_task"
        try:
            # check args
            error_code = 0
            if not task.name:
                log_error(self.name,
                          function,
                          "Launching task " + task.name + ": task_name can not be null",
                          self.log_file)
                task.status = "CRASHED (task_name can not be null)"[:500]
                task.save()
                error_code = 1
            elif not task.command_line:
                log_error(self.name,
                          function,
                          "Launching task " + task.name + ": task_command can not be null",
                          self.log_file)
                task.status = "CRASHED (task_command can not be null)"[:500]
                task.save()
                error_code = 2

            if error_code:
                return error_code

            tasker = TaskerThread(tiny_scheduler=self,
                                  task=task)
            tasker.start()

        except Exception as ex:
            log_error(self.name,
                      function,
                      "Error while launching task " + task.name + ": " + ex.__str__(),
                      self.log_file)
            task.status = ("CRASHED (" + ex.__str__() + ")")[:500]
            task.save()
