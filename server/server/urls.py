from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from account.views import activateemail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('account.urls')),
    path('api/posts/',include('post.urls')),
    path('api/search/',include('search.urls')),
    path('api/chat/',include('chat.urls')),
    path('activateemail/',activateemail,name='activateemail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
