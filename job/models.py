from django.db import models

# class JobStatus(models.TextChoices):
#     APPLIED = "Applied", "Applied"
#     INTERVIEW = "For Interview", "For Interview"
#     EXAM = "For Exam", "For Exam"
#     REJECTED = "Rejected", "Rejected"
#     # ACCEPTED = "Accepted", "Accepted"  # Uncomment if needed

class JobMode(models.TextChoices):
    FULLTIME = "Full-Time", "Full-Time"
    PARTTIME = "Part-Time", "Part-Time"
    WORKFROMHOME = "Workfrom-Home", "Workfrom-Home"

class Position(models.Model):
    jobcategory = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.jobcategory})"

class Company(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    mode = models.CharField(
        max_length=20, choices=JobMode.choices, default=JobMode.FULLTIME  # Default is FULLTIME now
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salarystatus = models.TextField(null=True, blank=True)
    date_applied = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='company_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} in {self.location} - {self.get_mode_display()}"


# class Job(models.Model):
#     position = models.ForeignKey(Position, on_delete=models.CASCADE)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     status = models.CharField(
#         max_length=20, choices=JobStatus.choices, default=JobStatus.APPLIED
#     )
#     mode = models.CharField(
#         max_length=20, choices=JobMode.choices, default=JobMode.ONSITE
#     )
#     salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     date_applied = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.position} at {self.company} ({self.get_status_display()})"
