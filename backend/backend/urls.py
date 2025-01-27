from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    # Django Admin Site
    path('admin/', admin.site.urls),

    # Node Management
    path('nodes/', include('nodes.urls')),

    # List All Authors On The Local Server
    path('authors/', views.get_authors, name='get_authors'),

    # Proxy Requests Either To The Local Server Or To Other Servers In The Network
    path('authors/<path:path>/', views.proxy_requests, name='proxy_requests'),

    # Inbox API
    path('api/authors/<uuid:author>/inbox/', include('inbox.urls')),

    # Author API
    path('api/authors/', include('authors.urls')),

    # Post API
    path('api/authors/<uuid:author>/posts/', include('posts.urls')),

    # Comment Api
    path('api/authors/<uuid:author>/posts/<uuid:post>/comments/', include('comment.urls')),

    # Notification Api
    path('api/authors/<uuid:author>/notifications/', include('notifications.urls')),

    # Followers Api
    path('api/authors/<uuid:author>/followers/', include('followers.follower_urls')),

    # Following Api
    path('api/authors/<uuid:author>/following/', include('followers.following_urls')),

    # Friends Api
    path('api/authors/<uuid:author>/friends/', include('followers.friends_urls')),

    # Serve API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Serve Swagger Docs
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Serve React
    path("", TemplateView.as_view(template_name='index.html')),
]
