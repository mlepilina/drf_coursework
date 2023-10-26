from django.urls import path

from main_app.apps import MainAppConfig

from main_app.views import HabitView, HabitsConnectionCreateAPIView, HabitsPublicView

app_name = MainAppConfig.name

urlpatterns = [
    path('habits/', HabitView.as_view(), name='habit'),
    path('habits/public/', HabitsPublicView.as_view(), name='habits_public'),
    path('habits/<int:habit_id>/', HabitsConnectionCreateAPIView.as_view(), name='connection_create'),
]
