from rest_framework import serializers
from .models import Company, Position, EmployeePosition


class PositionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'jobcategory']


class EmployeePositionSerializer(serializers.ModelSerializer):
    position = PositionSimpleSerializer(read_only=True)

    class Meta:
        model = EmployeePosition
        fields = ['id', 'title', 'position']


class PositionSerializer(serializers.ModelSerializer):
    employee_positions = EmployeePositionSerializer(many=True, read_only=True)

    class Meta:
        model = Position
        fields = ['id', 'jobcategory', 'employee_positions']


class CompanySerializer(serializers.ModelSerializer):
    employee_position = EmployeePositionSerializer(read_only=True)

    class Meta:
        model = Company
        fields = [
            'id', 'employee_position', 'name', 'location', 'details', 'mode',
            'salary', 'salarystatus', 'date_applied', 'image',
            'qualifications', 'benefits', 'location_image'
        ]
