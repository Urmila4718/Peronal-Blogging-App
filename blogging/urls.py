
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from personal_blog import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.getArticle, name="get_article"),
    path('createpost/',views.addArticle, name="add_article"),
    path('editpost/<int:id>/',views.editArticle, name="edit_article"),
    path('deletepost/<int:id>', views.deleteArticle, name='delete_article'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
