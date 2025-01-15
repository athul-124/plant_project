from django.urls import path
from . import views
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    # path('chatbot/', views.chatbot_page, name='chatbot_page'),  # Renders the chatbot page
    path('chatbot_response/', views.chatbot_response, name='chatbot_response'),  # Handles the bot's response
    path('upload/', views.upload_image, name='upload_image'),
    path('plant-library/', views.plant_library, name='plant_library'),
    path('plant-advisor/', views.plant_advisor, name='plant_advisor'),
    path('expert-advice/', views.expert_advice, name='expert_advice'),
    path('care/', views.care, name='care'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)