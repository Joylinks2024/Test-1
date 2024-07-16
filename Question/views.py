import os
from datetime import datetime
from pathlib import Path

import cv2
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from Users.settings import BASE_DIR
from .models import User
# from .models import Certificate
from .serializers import User_Serializer, Sertifikate_Serializer, Time_Edit_Serializer, Sertifikate_ID_Serializer

colour_light_blue = 255, 255, 0


@api_view(['POST'])
def Create_User(request):
    if request.method == 'POST':
        serializer = User_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"user_id": serializer.data['user_id']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def create_certificate(certificate_id: [int, str], user_fullname="Diyorbek O'tamurodov"):
#     import os
#     file_path = os.path.join(BASE_DIR, 'media/template_certificate/Sertificat_2.png')
#     save_path = f"{BASE_DIR}\\media\\certificates"
#     path_template = template = cv2.imread(file_path)
#     if path_template is not None:
#         cv2.putText(template, user_fullname, (245, 575), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1.7, (colour_light_blue), 1,
#                     cv2.LINE_AA)
#         cv2.imwrite(f"{save_path}\\certificate_{certificate_id}.jpg", template)
#         return f"media/certificates/certificate_{certificate_id}.jpg"


BASE_DIR = Path(__file__).resolve().parent.parent


def create_certificate(certificate_id: [int, str], user_fullname="Diyorbek O'tamurodov"):
    # Fayl yo'llarini aniqlash
    file_path = os.path.join(BASE_DIR, 'media', 'template_certificate', 'Sertificat_2.png')
    save_path = os.path.join(BASE_DIR, 'media', 'certificates')

    # Tasvirni o'qish
    template = cv2.imread(file_path)
    if template is not None:
        cv2.putText(template, user_fullname, (245, 575), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1.7, colour_light_blue, 1,
                    cv2.LINE_AA)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_file_path = os.path.join(save_path, f"certificate_{certificate_id}.jpg")

        # Tasvirni saqlash
        cv2.imwrite(save_file_path, template)
        return f"media/certificates/certificate_{certificate_id}.jpg"
    else:
        # print(f"Tasvirni yuklashda xatolik yuz berdi: {file_path}")
        return None


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
        certificate_id = Sertifikate_ID_Serializer(user)
        path = create_certificate(certificate_id=certificate_id.data['certificate_id'])
        serializer = Sertifikate_Serializer(user, data={"score": 60, "total_time": str(time_difference)})
        if serializer.is_valid():
            serializer.save()
            return Response({"score": 60, "total_time": str(time_difference), "photo": path}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def Restart_User(request):
    if request.method == 'PUT':
        try:
            user = get_object_or_404(User, user_id=request.data['user_id'])
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        serializer = Time_Edit_Serializer(user, data={"started_time": request.data['started_time'],
                                                      "finished_time": request.data['finished_time']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
