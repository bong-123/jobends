from django.contrib import admin
from .models import Apply, JobStatus
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@admin.register(Apply)
class ApplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'job_level', 'status', 'date_applied')
    list_filter = ('status', 'company', 'job_level')
    search_fields = ('user__username', 'user__email', 'company__name')
    list_editable = ('status',)
    ordering = ('-date_applied',)

    def save_model(self, request, obj, form, change):
        old_status = None
        if change:  # Only for updates, not for new objects
            old_status = Apply.objects.get(pk=obj.pk).status
        super().save_model(request, obj, form, change)
        
        if change and old_status != obj.status and obj.user.email:
            try:
                email_subject = f"Application Status Update - {obj.company.name}"
                email_message = (
                    f"Dear {obj.user.first_name} {obj.user.last_name},\n\n"
                    f"We have an update regarding your application for the {obj.job_level} position "
                    f"at {obj.company.name}.\n\n"
                    f"Previous Status: {JobStatus(old_status).label}\n"
                    f"New Status: {obj.get_status_display()}\n\n"
                    f"Please log in to your account for more details or contact us if you have any questions.\n\n"
                    f"Best regards,\nThe Job Application Team"
                )
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.user.email],
                    fail_silently=False,
                )
                logger.info(f"Email sent to {obj.user.email} for status update to {obj.status}")
            except Exception as e:
                logger.error(f"Failed to send email to {obj.user.email}: {str(e)}")
                self.message_user(request, f"Status updated, but failed to send email: {str(e)}", level='warning')
            else:
                self.message_user(request, f"Status updated and email sent to {obj.user.email}", level='success')