from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('car_app.urls')),
    path('customer/',include('customer_app.urls')),
    path('user/',include('user_app.urls')),

] + static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
