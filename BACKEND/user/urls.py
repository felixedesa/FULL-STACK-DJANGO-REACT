# # user/urls.py
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import UserViewSet, RegisterViewSet

# router = DefaultRouter()
# #router.register(r'users', UserViewSet)
# router.register(r'users', UserViewSet, basename='user')
# router.register(r'register', RegisterViewSet, basename='register')

# urlpatterns = [
#     path('', include(router.urls)),
# ]
# user/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import UserViewSet, RegisterViewSet,LoginViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'register', RegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='login'),

    # JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # Login (obtain access & refresh)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),     # Refresh token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),        # Optional: verify token
]

