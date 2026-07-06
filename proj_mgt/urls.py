
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('accounts.urls')),
    path("accounts/", include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('coordinator/', include('coordinator.urls')),
    path('student/', include('student.urls')),
    path('faculty/', include('faculty.urls')),
    path('administrator/', include('administrator.urls')),
    path('lms/', include('lms.urls')),
    path('mcqexams/', include('mcqexams.urls')),
    path('sdc/', include('sdc.urls')),
    path('feedback/', include('feedback.urls')),
    path('result_analysis/', include('result_analysis.urls')),
    path('alumni/', include('alumni.urls')),
    path('employer/', include('employer.urls')),
    
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)