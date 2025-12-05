from datetime import timedelta
from django.utils import timezone

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import PhoneOTP
from apps.serializers import PhoneNumberUpdateSerializer, OtpTokenSerializer
from utils.otp_service import generate_otp


@extend_schema(tags=['Users'], request= PhoneNumberUpdateSerializer)
class RequestPhoneChangeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PhoneNumberUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_phone_number = request.data.get("new_phone_number")

        if not new_phone_number:
            return Response({"error": "new_phone_number is required"}, status=400)

        # validate UZ number
        import re
        pattern = r'^\+?998[0-9]{9}$'
        if not re.match(pattern, new_phone_number):
            return Response({"error": "Invalid Uzbekistan number"}, status=400)

        last_code = PhoneOTP.objects.filter(new_phone_number=new_phone_number).order_by("-created_at").first()
        if last_code and not last_code.can_send_new():
            remaining_seconds = int(
                (last_code.created_at + timedelta(minutes=2) - timezone.now()).total_seconds()
            )
            return Response({
                'error': "Please wait before sending a new code",
                'remain_seconds': remaining_seconds
            })


        # generate OTP
        otp_code = generate_otp()

        PhoneOTP.objects.filter(new_phone_number=new_phone_number).delete()

        otp_code = PhoneOTP.objects.create(
            user=request.user,
            new_phone_number=new_phone_number,
            code=otp_code
        )
        serializer = OtpTokenSerializer(instance=otp_code)

# return OTP for testing (no SMS service)
        return Response({
            "message": "Verification code sent",
            **serializer.data  # return only for staging/testing
        })

@extend_schema(tags=["Users"], request= OtpTokenSerializer)
class VerifyPhoneOTPView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response({"error": "code is required"}, status=400)

        try:
            phone_otp = PhoneOTP.objects.get(user=request.user)
        except PhoneOTP.DoesNotExist:
            return Response({"error": "No code request found"}, status=404)

        # expired?
        if phone_otp.is_expired():
            return Response({"error": "code expired. Request a new one."}, status=400)

        # wrong?
        if phone_otp.code != code:
            return Response({"error": "Invalid code"}, status=400)

        # correct OTP → update phone
        user = request.user
        user.phone_number = phone_otp.new_phone_number
        user.save()

        # delete OTP entry
        phone_otp.delete()

        return Response({
            "message": "Phone number updated successfully",
            "new_phone_number": user.phone_number,
            'status_code': status.HTTP_200_OK
        })
