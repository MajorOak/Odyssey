

import threading
from django.core.management import execute_from_command_line



class Server(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)
        self.name = 'ServerThread'
        self.args = ('django-admin', 'runserver',)

    def run(self):
        execute_from_command_line(self.args)

