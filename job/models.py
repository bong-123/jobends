from django.db import models 

class JobMode(models.TextChoices):
    FULLTIME = "Full-Time", "Full-Time"
    PARTTIME = "Part-Time", "Part-Time"
    WORKFROMHOME = "Workfrom-Home", "Workfrom-Home"

class Position(models.Model):
    jobcategory = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.jobcategory

class EmployeePosition(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="employee_positions")
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.position.jobcategory})"

class Company(models.Model):
    employee_position = models.ForeignKey(EmployeePosition, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    details = models.TextField(null=True, blank=True)  # Formerly 'description'

    mode = models.CharField(
        max_length=20, choices=JobMode.choices, default=JobMode.FULLTIME
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salarystatus = models.CharField(max_length=255)
    date_applied = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='company_images/', null=True, blank=True)

    qualifications = models.TextField(null=True, blank=True)
    benefits = models.TextField(null=True, blank=True)
    location_image = models.ImageField(upload_to='location_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} hiring {self.employee_position.title} at {self.location} - {self.get_mode_display()}"
