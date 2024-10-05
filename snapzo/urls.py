from django.contrib import admin 
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from authentication.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('auth/', include('authentication.urls')),
    path('auth/logout/', LogoutView.as_view(), name='logoutPage'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)