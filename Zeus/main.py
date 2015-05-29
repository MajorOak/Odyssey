#!/usr/bin/env python


######## IMPORTS ########

import django
import time
import scheduling
import server
from controller.models import *



######## DEFINITIONS ########


def launch_scheduler():
    tiny_scheduler = scheduling.TinyScheduler()
    tiny_scheduler.start()
    time.sleep(1)
    return tiny_scheduler


def launch_server():
    django_server = server.Server()
    django_server.start()
    time.sleep(1)
    return django_server




######## SETTING UP ########

django.setup()



######## LETS PLAY ########


tsched = launch_scheduler()
print("We are free to do what we want now...")










