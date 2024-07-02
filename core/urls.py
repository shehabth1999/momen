"""
URL configuration for core project.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from customers.api.views import create_names

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('customers/', include('customers.urls')),
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
    path("create/", create_names, name="create"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)