from django.db import models

# Create your models here.

FALL = 'F'
WINTER = 'W'
SPRING = 'R'
SUMMER = 'S'

SCHOOL_TERM = (
    (FALL, 'Fall'),
    (WINTER, 'Winter'),
    (SPRING, 'Spring'),
    (SUMMER, 'Summer'),
)

FRESHMAN = 'FR'
SOPHOMORE = 'SO'
JUNIOR = 'JR'
SENIOR = 'SR'
GRADUATE = 'GR'
OTHER = 'OT'
NOTAPPLICABLE = 'NA'

YEAR_IN_SCHOOL_CHOICES = (
    (FRESHMAN, 'Freshman'),
    (SOPHOMORE, 'Sophomore'),
    (JUNIOR, 'Junior'),
    (SENIOR, 'Senior'),
    (GRADUATE, 'Graduate'),
    (OTHER, 'Other'),
    (NOTAPPLICABLE, 'Not Applicable'),
)

class DaysOfWeek(models.Model):
    day = models.CharField(max_length=8)

class Member(models.Model):
    """
    Model for a Lodge Member of Beaver Lodge
    """
    nickname = models.CharField(max_length=30, blank=True, null=True)
    member_since = models.DateField()
    year = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    workjobs = models.ManyToManyField(WorkJob, through='ScheduledWorkJob')
    positions = models.ManyToManyField(Position, through='PositionHeld')

    def GetCurrentPositions():
        """
        return a list of a members current jobs
        """
        return []

class WorkJobResponsibility(models.Model):
    """
    Model for a Work Job responsibility which has a priority of when it should get done
    """
    workjob = models.ForeignKey(WorkJob)
    description = models.CharField(max_length=200)
    priority = models.IntegerField()

class WorkJob(models.Model):
    """
    Model to define all the work jobs at beaver lodge, on a particular day a job must be started at a certain time and completed by a certain time
    """
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    time_start = models.TimeField()
    time_due = models.TimeField()
    length = models.IntegerField()
    days = models.ManyToManyField(DaysOfWeek)


class Position(models.Model):
    """
    Model for Exec positions at Beaver Lodge, if a member has an exec position they may be able to get reduced hours in their work hours
    """
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    seniority_points = models.IntegerField()
    is_exec = models.BooleanField()
    percent_off_workjobs = models.IntegerField()

class PositionHeld(models.Model):
    """
    Intermediary model for representing the positions that members have held in the past
    """
    position = models.ForeignKey(Position)
    member = models.ForeignKey(Member)
    begin_term = models.ForeignKey(Term)
    end_term = models.ForeignKey(Term)
    is_active = models.BooleanField()

class Term(models.Model):
    """
    Collection of terms representing school
    """
    begin_date = models.DateField()
    end_date = models.DateField()
    school_term = models.CharField(max_length = 1)

class ScheduledWorkJob(models.Model):
    """
    Model for the individual work jobs scheduled each week
    """
    date_due = models.DateField()
    member = models.ForeignKey(Member)
    workjob = models.ForeignKey(WorkJob)

class Trade(models.Model):
    """
    Model for proposing a job trade between two lodge members
    A job trade can be for the term or just for that particular position
    In order for a jobs to be traded, both parties must agree to the trade as well as the WM or AWM
    """
    proposed_date = models.DateTimeField(auto_now_add=true)
    proposed_by = models.ForeignKey(Member)
    proposed_by_workjob = models.ForeignKey(ScheduledWorkJob)
    recipient = models.ForeginKey(Member)
    recipient_workjob = models.ForeignKey(ScheduledWorkJob)
    approved_date = models.DateTimeField()
    is_permanent_trade = models.BooleanField(default=False)

class Fine(models.Model):
    """
    When a member fails to meet their duties for a work job or house duties they can be assigned a fine which must be paid in full to the Financial manager
    """
    offense = models.CharField(max_length = 50)
    amount = models.IntegerField(default = 0)
    paid = models.BooleanField(default = False)

    def GetAmount():
        """
        A member can either be fined an amount or be given a warning
        """
        if amount == 0:
            return "Warning"
        else:
            return amount

class MakeUpJob(models.Model):
    """
    When a member fails a job they may be asked to perform a work up job
    """
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    missed_workjob = models.ForeignKey(ScheduledWorkJob)
    date_due = models.DateField()
    fine = models.ForeignKey(Fine)
    completed = models.BooleanField(default = False)
