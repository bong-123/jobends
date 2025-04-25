from rest_framework import serializers
from .models import Company, Position

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'jobcategory', 'title']

class CompanySerializer(serializers.ModelSerializer):
    position = PositionSerializer()  # Corrected to use 'position', not 'company'

    class Meta:
        model = Company
        fields = ['id', 'position', 'name', 'location', 'description', 'mode', 'salary', 'salarystatus', 'date_applied', 'image']

    # def create(self, validated_data):
    #     company_data = validated_data.pop('company')
    #     position_data = validated_data.pop('position')

    #     company, _ = Company.objects.get_or_create(**company_data)
    #     position, _ = Position.objects.get_or_create(**position_data)

    #     job = Job.objects.create(
    #         position=position, company=company, **validated_data
    #     )
    #     return job
