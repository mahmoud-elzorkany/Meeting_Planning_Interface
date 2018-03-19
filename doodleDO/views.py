from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Meeting, Vote, Room, MeetingDate
from django.template import loader
from django.http import Http404
from django.db.models import Count


def index(request):
    voting_meetings = Meeting.objects.filter(meeting_date__isnull=True)
    room_selection_meetings = Meeting.objects.filter(meeting_date__isnull=False, meeting_room__isnull=True).order_by('-meeting_date')
    done_meetings = Meeting.objects.filter(meeting_date__isnull=False, meeting_room__isnull=False).order_by('-meeting_date')
    template = loader.get_template('doodleDO/index.html')
    context = {
        'voting_meetings': voting_meetings,
        'room_selection_meetings': room_selection_meetings,
        'done_meetings': done_meetings,
    }
    return HttpResponse(template.render(context, request))


def detail(request, meeting_id):
    try:
        meeting = Meeting.objects.get(pk=meeting_id)
    except Meeting.DoesNotExist:
        raise Http404("Question does not exist")

    rooms = Room.objects.all()

    dates = MeetingDate.objects.filter(date_meeting=meeting)

    return render(request, 'doodleDO/detail.html', {'meeting': meeting, 'rooms': rooms, 'dates': dates})


def vote(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    meeting_date = get_object_or_404(MeetingDate, pk=request.POST['date'])
    vote_new = Vote(vote_meeting=meeting, vote_date=meeting_date)
    vote_new.save()

    count = Vote.objects.filter(vote_meeting=meeting).count()

    print("count "+str(count) + " needed " + str(meeting.meeting_votes_required))

    print("ana are mere")

    if count >= meeting.meeting_votes_required:
        meeting_dates = Vote.objects.filter(vote_meeting=meeting).values('vote_date').annotate(total=Count('id')).order_by('-total')
        meeting.meeting_date = get_object_or_404(MeetingDate, pk=meeting_dates[0]["vote_date"]).date_date
        meeting.save()

    return HttpResponse("Vote registered <3  " + repr(meeting.meeting_date))


def choose_room(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    room = get_object_or_404(Room, pk=request.POST['room'])
    meeting.meeting_room = room
    meeting.save()
    return HttpResponse("Room chosen! <3")
