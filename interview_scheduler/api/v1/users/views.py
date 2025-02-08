# views.py
from django.contrib.auth import authenticate
import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User, InterviewSchedule, InterviewAvailability
from .serializers import UserSerializer


@api_view(["POST"])
def signup(request):
    """
    Handle user registration
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,
                "profile_type": user.profile_type,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def signin(request):
    """
    Handle user authentication
    """
    username = request.data.get("username")
    password = request.data.get("password")
    instance = User.objects.filter(username=username).first()
    if instance:
        print(instance)
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "username": user.username,
                    "profile_type": user.profile_type,
                }
            )
    return Response(
        {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_interview_availability(request):
    """
    Add interview availability
    """
    interview_date = request.data.get("interview_date")
    start_time = request.data.get("start_time")
    end_time = request.data.get("end_time")
    user = request.user
    if InterviewAvailability.objects.filter(user=user, date=interview_date).exists():
        return Response(
            {"error": "Interview availability already exists for this date"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    InterviewAvailability.objects.create(
        user=user, date=interview_date, start_time=start_time, end_time=end_time
    )
    return Response(
        {"message": "Interview availability added successfully"},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def get_possible_interviews(request):
    """
    Get possible interviews
    """
    candidate_id = request.GET.get("candidate_id")
    recruiter_id = request.GET.get("recruiter_id")
    date = request.GET.get("date", datetime.date.today().strftime("%Y-%m-%d"))
    candidate = User.objects.filter(id=candidate_id).first()
    recruiter = User.objects.filter(id=recruiter_id).first()
    candidate_availability = InterviewAvailability.objects.filter(
        user=candidate, date=date
    )
    if not candidate_availability.exists():
        return Response(
            {"error": "Candidate is not available on this date"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    recruiter_availability = InterviewAvailability.objects.filter(
        user=recruiter, date=date
    )
    if not recruiter_availability.exists():
        return Response(
            {"error": "Recruiter is not available on this date"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if recruiter_availability.filter(
        end_time__gt=candidate_availability.first().start_time
        + datetime.timedelta(hours=1),
        start_time__lt=candidate_availability.first().end_time,
    ).exists():
        start_time = (
            candidate_availability.first().start_time
            if candidate_availability.first().start_time
            > recruiter_availability.first().start_time
            else recruiter_availability.first().start_time
        )
        end_time = recruiter_availability.first().end_time
        availabe_slots = []
        while end_time > start_time + datetime.timedelta(hours=1):
            time_slots = (
                start_time.time(),
                (start_time + datetime.timedelta(hours=1)).time(),
            )
            availabe_slots.append(time_slots)
            start_time += datetime.timedelta(hours=1)
        return Response({"available_slots": availabe_slots}, status=status.HTTP_200_OK)

    return Response(
        {"error": "Interview is not possible"}, status=status.HTTP_400_BAD_REQUEST
    )
