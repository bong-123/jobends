from rest_framework import serializers
from .models import Apply
from user.models import CustomUser
from job.models import Company

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']  # Adjust fields based on your CustomUser model

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']  # Adjust fields based on your Company model

class ApplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    resume = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Apply
        fields = [
            'id',
            'user',
            'company',
            'status',
            'date_applied',
            'resume',
            'age',
            'birthdate',
            'full_current_location',
            'job_level',
        ]
        read_only_fields = ['date_applied']