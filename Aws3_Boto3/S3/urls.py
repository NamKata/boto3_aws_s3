from django.urls import path, include
from . import views
urlpatterns=[
    path('search_bucket/',views.search_bucket, name='search'),
    path('list/<bucket>', views.list_image, name='list'),
    path('', views.upload_in_request, name='test'),
    path('api/v1/link-presign/', views.list_url_demo, name='1132'),
    path('download/<bucket>', views.download_file, name ='download'),
    path('api/v1/rename/', views.rename_file, name='rename'),
    path('api/v1/move/', views.move_file, name='move'),
    path('api/v1/buckets', views.list_bucket, name='lstbucket'),
]