from django.contrib.auth import authenticate, login, logout
from rest_framework import status, views
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User


class LoginView(views.APIView):

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"))

        if user is None or not user.is_active:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username or password incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response(UserSerializer(user).data)


class ChangePasswordView(views.APIView):

    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        print(user.username)
        if user.check_password(request.data['oldPassword']):
            print(request.data['newPassword'])
            user.set_password(request.data['newPassword'])
            user.save()
            return Response(UserSerializer(User.objects.get(username=request.data['username'])).data)
        return Response({
                'status': 'Unauthorized',
                'message': 'Your Password is incorrect'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):

    def get(self, request):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

