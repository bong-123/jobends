from django.db import models
from user.models import CustomUser  # Adjust import based on your project structure
from job.models import Company

class JobStatus(models.TextChoices):
    APPLIED = "Applied", "Applied"
    INTERVIEW = "For Interview", "For Interview"
    EXAM = "For Exam", "For Exam"
    REJECTED = "Rejected", "Rejected"
    ACCEPTED = "Accepted", "Accepted"

class Apply(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='applicants')
    status = models.CharField(
        max_length=20, choices=JobStatus.choices, default=JobStatus.APPLIED
    )
    date_applied = models.DateField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    full_current_location = models.CharField(max_length=255, null=True, blank=True)
    job_level = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'company')  # Prevent duplicate applications to the same job

    def __str__(self):
        return f"{self.user.username} applied to {self.company.name} - {self.status}"