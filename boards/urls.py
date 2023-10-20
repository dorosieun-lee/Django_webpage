from django.urls import path
from . import views

app_name="boards"
urlpatterns = [
    path('', views.index, name="index"),
    path('index/<str:order_by>/', views.index_order, name='index_order'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'), 
    path('<int:board_pk>/like/', views.like, name='like'),
    path('<int:pk>/update/', views.update, name='update'),   
    path('<int:board_pk>/comment/', views.comment, name='comment'),
    path('<int:board_pk>/comment/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
]
