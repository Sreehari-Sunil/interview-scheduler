from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, InterviewSchedule, InterviewAvailability


class UserAdmin(DefaultUserAdmin):
    # Add custom fields to the admin interface
    fieldsets = (
        *DefaultUserAdmin.fieldsets,
        (
            'Extra datas',
            {
                'fields': (
                    'profile_type',
                ),
            },
        ),
    )

    list_display = (
        'username', 'date_joined', 'first_name',
        'email', 'profile_type', 'is_active',
    )
    search_fields = ('username', 'first_name')
    list_filter = ('profile_type',)
admin.site.register(User, UserAdmin)


class InterviewScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'recruiter', 'candidate', 'date', 'start_time', 'end_time',
    )
    list_filter = ('recruiter', 'candidate', 'date', 'start_time', 'end_time')
admin.site.register(InterviewSchedule, InterviewScheduleAdmin)

class InterviewAvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'date', 'start_time', 'end_time',
    )
    list_filter = ('user', 'date', 'start_time', 'end_time')
admin.site.register(InterviewAvailability, InterviewAvailabilityAdmin)


