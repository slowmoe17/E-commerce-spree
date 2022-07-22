from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer, UserSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import CustomUser
from rest_framework.views import APIView
from .mail import send_confirmation_email
class Login(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not CustomUser.objects.get(email=serializer.data['email']).is_verified:
            return Response({"detail": "Please verify your email first"}, status=status.HTTP_400_BAD_REQUEST)
        else : 

            try :
            
                serializer.is_valid(raise_exception=True)
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            except InvalidToken:
                return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            except TokenError:
                return Response({"detail": "Token error"}, status=status.HTTP_400_BAD_REQUEST)
            

        

class Register(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save()


class ValidateOtp(APIView):
    permission_classes = (permissions.AllowAny,)

    
    def post(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
            if user.otp == request.data['otp']:
                user.is_verified = True
                user.save()

               
                
                return Response({"detail": "OTP is valid"}  ,status=status.HTTP_200_OK ,)
            else:
                return Response({"detail": "OTP is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    
        