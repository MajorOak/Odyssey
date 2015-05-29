from django.db import models
from django.utils import timezone

# Create your models here.


class Scheduler(models.Model):
    status = models.CharField(max_length=500)
    start_date = models.DateTimeField('start date this run', null=True)
    end_date = models.DateTimeField('end date this run', null=True)
    to_be_ended = models.BooleanField(default=False)
    log_file = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return 'Scheduler(' + self.id.__str__() + '): ' + self.status

    def __unicode__(self):
        return unicode('Scheduler(' + self.id.__str__() + '): ' + self.status)


class Job(models.Model):
    request_date = models.DateTimeField('date when job was requested')
    request_user = models.CharField(max_length=200)

    def __str__(self):
        return str('Job requested on ' + self.request_date.__str__() + " by " + self.request_user)

    def __unicode__(self):
        return unicode('Job requested on ' + self.request_date.__str__() + " by " + self.request_user)


class TaskDefinition(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    command_line = models.CharField(max_length=4000)
    default_argument_list = models.CharField(max_length=4000, null=True)

    def __str__(self):
        return str('Task: ' + self.name)

    def __unicode__(self):
        return unicode('Task: ' + self.name)


class Task(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=500)
    job = models.ForeignKey(Job, null=True)
    run_date = models.DateTimeField('date of expected launch', null=True)
    start_date = models.DateTimeField('date of start', null=True)
    end_date = models.DateTimeField('date of end', null=True)
    run_number = models.IntegerField(default=0)
    command_line = models.CharField(max_length=4000)
    argument_list = models.CharField(max_length=4000, null=True)

    def __str__(self):
        return str('Task: ' + self.name + ' in status: ' + self.status)
        # return 'Task: ' + self.name \
        #        + ' in status: ' + self.status \
        #        + ' foreseen to be launched at: ' + str(self.run_date) \
        #        + ' (start: ' + str(self.start_date) + ' end_date: ' + str(self.end_date) \
        #        + ') with the command_line: <' + self.command_line + '>' \
        #        + ' args: <' + str(self.argument_list) + '>'

    def __unicode__(self):
        return unicode('Task: ' + self.name + ' in status: ' + self.status)


class TaskDependency(models.Model):
    task = models.CharField(max_length=200)
    dependency_task = models.CharField(max_length=200)

    def __str__(self):
        return self.task + " depends from " + self.dependency_task

    def __unicode__(self):
        return unicode(self.task + " depends from " + self.dependency_task)


class Log(models.Model):
    type = models.CharField(max_length=20)
    who = models.CharField(max_length=200)
    message = models.CharField(max_length=500)
    datetime = models.DateTimeField('log date', default=timezone.now)

    def __str__(self):
        return 'Log(' + self.type + ")> " + self.who + "@" + self.datetime.__str__() + "> " + self.message

    def __unicode__(self):
        return unicode('Log(' + self.type + ")> " + self.who + "@" + self.datetime.__str__() + "> " + self.message)

