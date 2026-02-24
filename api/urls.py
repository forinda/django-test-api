from django.urls import path, include

urlpatterns = [
    path('tasks/', include('task.urls')),
    path('categories/', include('category.urls')),
    path('auth/', include('authentication.urls')),
    path('users/', include('users.urls')),
    path('articles/', include('articles.urls')),
]
