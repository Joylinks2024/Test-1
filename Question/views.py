from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
# from .models import Certificate
from .serializers import User_Serializer, Sertifikate_Serializer


@api_view(['POST'])
def Create_User(request):
    if request.method == 'POST':
        serializer = User_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"user_id": serializer.data['user_id']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Finish_User(request):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, user_id=request.data['user_id'])
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        start_time = request.data["start_time"]
        finish_time = request.data["finish_time"]
        dt1 = datetime.fromisoformat(start_time)
        dt2 = datetime.fromisoformat(finish_time)
        time_difference = dt2 - dt1

        serializer = Sertifikate_Serializer(user, data={"score": 50, "total_time": str(time_difference)})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
