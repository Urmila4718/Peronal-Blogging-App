from django.urls import path, include

urlpatterns = [
    path('', include('blogging.urls'))
]
