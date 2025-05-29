from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin  # Import the custom permission
from rest_framework.response import Response
from rest_framework import status
from .models import Apply, JobStatus
from job.models import Company
from .serializers import ApplySerializer
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

class ApplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.debug(f"Request user: {request.user}, Email: {request.user.email}, Data: {request.data}")
        try:
            required_fields = ["company_id", "age", "birthdate", "full_current_location", "job_level"]
            missing_fields = [field for field in required_fields if field not in request.data]
            if missing_fields:
                return Response(
                    {"detail": f"Missing fields: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            company_id = request.data.get("company_id")
            try:
                company_id = int(company_id)
            except (ValueError, TypeError):
                return Response(
                    {"detail": "Invalid company_id: must be a number."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                return Response(
                    {"detail": "Company not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            if Apply.objects.filter(user=request.user, company=company).exists():
                return Response(
                    {"detail": "You have already applied to this company."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = {
                "status": JobStatus.APPLIED,
                "age": request.data["age"],
                "birthdate": request.data["birthdate"],
                "full_current_location": request.data["full_current_location"],
                "job_level": request.data["job_level"],
            }
            if "resume" in request.FILES:
                data["resume"] = request.FILES["resume"]

            serializer = ApplySerializer(data=data)
            if serializer.is_valid():
                application = serializer.save(user=request.user, company=company)
                return Response(
                    {"message": "Application submitted successfully"},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error in ApplyView: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class UserApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.debug(f"Fetching applications for user: {request.user.email}")
        try:
            applications = Apply.objects.filter(user=request.user).order_by('-date_applied')
            serializer = ApplySerializer(applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching applications for user {request.user.email}: {str(e)}")
            return Response({"error": f"Failed to fetch applications: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateApplicationStatusView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, application_id):
        logger.debug(f"Request user: {request.user}, is_superuser: {request.user.is_superuser}, Application ID: {application_id}, Data: {request.data}")
        try:
            # Verify user permissions
            if not (request.user.is_superuser or request.user.groups.filter(name='Recruiters').exists()):
                logger.error(f"User {request.user} lacks required permissions")
                return Response(
                    {"detail": "Admin or Recruiter access required."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Fetch the application
            try:
                application = Apply.objects.get(id=application_id)
                logger.info(f"Application found: ID {application_id}, User: {application.user.username}, Email: {application.user.email}, Company: {application.company.name}")
            except Apply.DoesNotExist:
                logger.error(f"Application ID {application_id} not found")
                return Response(
                    {"detail": "Application not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if status is provided
            new_status = request.data.get("status")
            if not new_status:
                logger.error("Status field missing in request")
                return Response(
                    {"detail": "Status field is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate status
            valid_statuses = [choice[0] for choice in JobStatus.choices]
            if new_status not in valid_statuses:
                logger.error(f"Invalid status: {new_status}. Valid options: {valid_statuses}")
                return Response(
                    {"detail": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update status
            old_status = application.status
            application.status = new_status
            application.save()
            logger.info(f"Application {application_id} status updated from {old_status} to {new_status}")

            # Send email notification
            if application.user.email:
                try:
                    email_subject = f"Application Status Update - {application.company.name}"
                    email_message = (
                        f"Dear {application.user.first_name} {application.user.last_name},\n\n"
                        f"We have an update regarding your application for the {application.job_level} position "
                        f"at {application.company.name}.\n\n"
                        f"Previous Status: {JobStatus(old_status).label}\n"
                        f"New Status: {application.get_status_display()}\n\n"
                        f"Please log in to your account for more details or contact us if you have any questions.\n\n"
                        f"Best regards,\nThe Job Application Team"
                    )
                    send_mail(
                        subject=email_subject,
                        message=email_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[application.user.email],
                        fail_silently=False,
                    )
                    logger.info(f"Email successfully sent to {application.user.email} for status update to {new_status}")
                except Exception as e:
                    logger.error(f"Failed to send email to {application.user.email}: {str(e)}")
                    return Response(
                        {
                            "message": f"Status updated to {new_status}, but failed to send email.",
                            "email_error": str(e)
                        },
                        status=status.HTTP_200_OK
                    )
            else:
                logger.warning(f"No email address found for user {application.user.username} (ID: {application.user.id})")
                return Response(
                    {"message": f"Status updated to {new_status}, but no email address found for the user."},
                    status=status.HTTP_200_OK
                )

            return Response(
                {"message": f"Application status updated to {new_status}"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Error in UpdateApplicationStatusView: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)