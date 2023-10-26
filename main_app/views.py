from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from main_app.models import Habit, HabitsConnection
from main_app.paginators import paginate
from main_app.serializers import HabitSerializer


class HabitView(APIView):

    def post(self, request: Request):
        """Создать новую привычку"""
        serializer = HabitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        habit = Habit(
            user=request.user,
            **serializer.validated_data
        )
        habit.save()

        response_data = {
            'id': habit.pk
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def get(self, request: Request, *args, **kwargs):
        """Получить список всех привычек пользователя"""
        page_number = request.query_params.get('page', 1)
        habits = Habit.objects.filter(user=self.request.user)
        response = paginate(
            query=HabitSerializer(habits, many=True).data,
            per_page=1,
            page_number=page_number,
        )

        return Response(data=response, status=status.HTTP_200_OK)


class HabitsPublicView(APIView):

    def get(self, request, *args, **kwargs):
        """Получить список всех публичных привычек"""
        page_number = request.query_params.get('page', 1)
        habits = Habit.objects.filter(publicity=Habit.Publicity.PUBLIC).values(
            'action', 'place', 'time', 'habit_type', 'periodicity', 'reward', 'time_to_complete'
        )
        response = paginate(
            query=habits,
            per_page=1,
            page_number=page_number,
        )
        return Response(data=response, status=status.HTTP_200_OK)


class HabitsConnectionCreateAPIView(APIView):

    def post(self, request: Request, habit_id: int):
        useful_habit: Habit = get_object_or_404(Habit, pk=habit_id, habit_type=Habit.HabitType.USEFUL)
        if useful_habit.reward:
            error_text = f'Полезную привычку с вознаграждением нельзя связывать'
            return Response(data={'error': error_text}, status=status.HTTP_400_BAD_REQUEST)

        pleasant_id = request.data.get('id')
        pleasant_habit_query = Habit.objects.filter(pk=pleasant_id, habit_type=Habit.HabitType.PLEASANT)
        if len(pleasant_habit_query) == 0:
            error_text = f'Приятная привычка с id {pleasant_id} не найдена'
            return Response(data={'error': error_text}, status=status.HTTP_400_BAD_REQUEST)

        HabitsConnection.objects.create(
            useful=useful_habit,
            pleasant=pleasant_habit_query[0]
        )

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request, habit_id: int):
        """Удалить привычку"""
        habit: Habit = get_object_or_404(Habit, pk=habit_id)
        habit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, habit_id: int):
        """Редактировать привычку"""
        habit = get_object_or_404(Habit, pk=habit_id)
        serializer = HabitSerializer(habit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

