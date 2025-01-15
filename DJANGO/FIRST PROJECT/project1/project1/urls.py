from django.contrib import admin
from django.urls import path
from video_stream import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('video/', views.video_feed, name='video_feed'),
    path('video1/', views.video_feed_ip, name='video_feed'),
    path('video11/', views.home, name='video_recording'),
    path('video-recording/', views.video_recording, name='video_recording'),
    path('video_feed/', views.video_feed, name='video_feed'),  # Route to stream video

    

]
