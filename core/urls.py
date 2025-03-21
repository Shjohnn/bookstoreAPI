from django.conf.urls.i18n import urlpatterns
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings
from main.views import *

from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns=[
    path('accounts/register/', RegisterAPIVIew.as_view()),
    path('accounts/me/',AccountRetrieveUpdateDeleteAPIView.as_view()),

]
urlpatterns+=[
    path('books/', BooksListCreateAPIView.as_view()),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view()),
    path('books/mine/', MyBooksList.as_view()),
    path('books/<int:pk>/mark-sold/', BookMarkSoldAPIView.as_view()),
    # path('books/<int:pk>/wishlist/', MyWishlistListAPIView.as_view()),
]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns+=[
    path('token/', token_obtain_pair),
    path('token/refresh/', token_refresh)
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


