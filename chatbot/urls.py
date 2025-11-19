from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Include your app's urls, NOT chatbot.urls
    path('', include('myapp.urls')),

    # Optional: redirect root to homepage (if needed)
    path('', RedirectView.as_view(url='/', permanent=False)),
]

# ✅ Serve static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
