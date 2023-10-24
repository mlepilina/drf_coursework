from django.urls import path

from main_app.apps import MainAppConfig

from main_app.views import HabitView, HabitsConnectionCreateAPIView

app_name = MainAppConfig.name

urlpatterns = [
    path('habits/', HabitView.as_view(), name='habit'),
    path('habits/<int:habit_id>/', HabitsConnectionCreateAPIView.as_view(), name='connection_create'),
]
