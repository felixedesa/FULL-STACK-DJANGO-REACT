# # from rest_framework.permissions import AllowAny
# # from rest_framework import viewsets
# # from user.serializers import UserSerializer

# # from rest_framework.response import Response
# # from rest_framework.viewsets import ViewSet
# # from rest_framework.permissions import AllowAny
# # from rest_framework import status
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from user.serializers import RegisterSerializer
# # from user.models import User

# # class UserViewSet(viewsets.ModelViewSet):
# #     http_method_names = ('patch', 'get')
# #     permission_classes = (AllowAny,)
# #     serializer_class = UserSerializer

# #     def get_queryset(self):
# #         if self.request.user.is_superuser:
# #             return User.objects.all()
# #         return User.objects.exclude(is_superuser=True)

# #     def get_object(self):
# #         obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
# #         self.check_object_permissions(self.request, obj)
# #         return obj
    


# # class RegisterViewSet(ViewSet):
# #     serializer_class = RegisterSerializer
# #     permission_classes = (AllowAny,)
# #     http_method_names = ['post']

# #     def create(self, request, *args, **kwargs):
# #         serializer = self.serializer_class(data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         user = serializer.save()

# #         refresh = RefreshToken.for_user(user)
# #         access_token = str(refresh.access_token)

# #         return Response({
# #             "user": serializer.data,
# #             "refresh": str(refresh),
# #             "token": access_token,
# #         }, status=status.HTTP_201_CREATED)

# # views.py (Improved with Full CRUD support and best practices)
# from rest_framework.response import Response
# from rest_framework.viewsets import ViewSet
# from rest_framework.permissions import AllowAny
# from rest_framework import status
# from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
# from user.serializers import LoginSerializer


# from rest_framework import viewsets, status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.viewsets import ViewSet
# from rest_framework_simplejwt.tokens import RefreshToken

# from user.serializers import UserSerializer, RegisterSerializer
# from user.models import User
# from django.shortcuts import get_object_or_404


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for performing CRUD operations on User model.
#     """
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'public_id'
#     queryset = User.objects.all()

#     def get_queryset(self):
#         # Admins see all users, others don't see superusers
#         if self.request.user.is_superuser:
#             return User.objects.all()
#         return User.objects.exclude(is_superuser=True)

#     def retrieve(self, request, *args, **kwargs):
#         user = get_object_or_404(User, public_id=kwargs['public_id'])
#         self.check_object_permissions(request, user)
#         serializer = self.get_serializer(user)
#         return Response(serializer.data)

#     def update(self, request, *args, **kwargs):
#         user = get_object_or_404(User, public_id=kwargs['public_id'])
#         self.check_object_permissions(request, user)
#         serializer = self.get_serializer(user, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         user = get_object_or_404(User, public_id=kwargs['public_id'])
#         self.check_object_permissions(request, user)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class RegisterViewSet(ViewSet):
#     """
#     ViewSet for handling user registration.
#     """
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)

#         return Response({
#             "user": serializer.data,
#             "refresh": str(refresh),
#             "token": access_token,
#         }, status=status.HTTP_201_CREATED)

# # login viewsets 

# class LoginViewSet(ViewSet):
#     serializer_class = LoginSerializer
#     permission_classes = (AllowAny,)
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except TokenError as e:
#             raise InvalidToken(e.args[0])

#         return Response(serializer.validated_data, status=status.HTTP_200_OK)

# views.py

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.shortcuts import get_object_or_404

from user.serializers import UserSerializer, RegisterSerializer, LoginSerializer
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for performing CRUD operations on User model.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'public_id'

    def get_queryset(self):
        # Superusers see all users, others don't see superusers
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, public_id=kwargs['public_id'])
        if not request.user.is_superuser and request.user != user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(User, public_id=kwargs['public_id'])
        if not request.user.is_superuser and request.user != user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterViewSet(ViewSet):
    """
    ViewSet for handling user registration.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "token": access_token,
        }, status=status.HTTP_201_CREATED)


class LoginViewSet(ViewSet):
    """
    ViewSet for handling user login and token return.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
