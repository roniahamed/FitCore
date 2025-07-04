from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('admin/', admin.site.urls),

    
    # users App
    path('api/v1/auth/', include('users.urls')),

    #meal
    path('api/v1/nutrition/',include('meal.urls')), # Meal app
    
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
