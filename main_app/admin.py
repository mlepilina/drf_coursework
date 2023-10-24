from django.contrib import admin

from main_app.models import Habit, HabitsConnection


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'place', 'time', 'habit_type', 'periodicity', 'publicity',)


@admin.register(HabitsConnection)
class HabitsConnectionAdmin(admin.ModelAdmin):
    list_display = ('useful', 'pleasant',)
