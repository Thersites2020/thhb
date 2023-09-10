
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from core.views import home

import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'accounts/password_change/',
        auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change',
    ),
    path(
        'accounts/password_change/done/',
        auth_views.PasswordChangeView.as_view(template_name='password_change_done.html'),
        name='password_change_done',
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls', namespace='core')),
]


if settings.DEBUG:
    urlpatterns += static('/static/',
                          document_root=os.path.join(settings.BASE_DIR, 'static/'))