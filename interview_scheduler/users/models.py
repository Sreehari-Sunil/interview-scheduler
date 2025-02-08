from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    profile_type = models.CharField(max_length=255, choices=[('candidate', 'Candidate'), ('recruiter', 'Recruiter')], blank=True, null=True)

    class Meta:
        db_table = 'users_user'

    def __str__(self):
        return self.username


class InterviewAvailability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = 'users_interviewavailability'
        verbose_name_plural = 'interview availabilities'

    def __str__(self):
        return f"{self.user.username} - {self.date} {self.start_time} - {self.end_time}"


class InterviewSchedule(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recruiter')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidate')
    date = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = 'users_interviewschedule'
        verbose_name_plural = 'interview schedules'


    def __str__(self):
        return f"{self.recruiter.username} - {self.candidate.username} - {self.date} {self.start_time} - {self.end_time}"
