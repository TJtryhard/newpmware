from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')), # 这里将myapp的URL引入
]


#path('myapp/', include('myapp.urls')),
