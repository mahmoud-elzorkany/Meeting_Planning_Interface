from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=200)
    room_location = models.CharField(max_length=200)


class Meeting(models.Model):
    meeting_name = models.CharField(max_length=200)
    meeting_votes_required = models.IntegerField()
    meeting_room = models.ForeignKey(Room, null=True, blank=True)
    meeting_date = models.DateField('meeting date', null=True, blank=True)


class MeetingDate(models.Model):
    date_meeting = models.ForeignKey(Meeting)
    date_date = models.DateField('date vote')


class Vote(models.Model):
    vote_meeting = models.ForeignKey(Meeting)
    vote_date = models.ForeignKey(MeetingDate)



