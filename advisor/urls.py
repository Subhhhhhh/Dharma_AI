from django.urls import path
from . import views

app_name = 'advisor'

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat_view, name='chat'),
    path("ramayan-ai/", views.ramayan_ai_view, name="ramayan_ai"),
    path("sunderkand-ai/", views.sunderkand_ai_view, name="sunderkand_ai"),
    path("about/", views.about_view, name="about"),
    path("testimonials/", views.testimonials_view, name="testimonials"),
    path('hanuman-chalisa/', views.hanuman_chalisa_view, name='hanuman_chalisa'),
    path('bajrang-baan/', views.bajrang_baan_view, name='bajrang_baan'),
    path('sankat-mochan/', views.sankat_mochan_view, name='sankat_mochan'),
    path('ram-stuti/', views.Ram_stuti_view, name='Ram_stuti'),


]
