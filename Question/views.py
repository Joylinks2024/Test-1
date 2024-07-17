import os
from pathlib import Path

import cv2
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import User_Serializer, Sertifikate_Serializer, Sertifikate_ID_Serializer

colour_light_blue = 255, 255, 0


@api_view(['POST'])
def Create_User(request):
    if request.method == 'POST':
        serializer = User_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"user_id": serializer.data['user_id']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return None


def score_calculation(test: dict):
    count_true = int()
    count_false = int()
    correct_answers = {
        "1": "C",
        "2": "A",
        "3": "D",
        "4": "C",
        "5": "A",
        "6": "C",
        "7": "C",
        "8": "A",
        "9": "C",
        "10": "B"
    }
    for key, value in test.items():
        true_answer = correct_answers.get(key)
        if true_answer == value:
            count_true += 1
        else:
            count_false += 1
    return count_true, count_false


@api_view(['POST'])
def Finish_User(request):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, user_id=request.data['user_id'])
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        count_true, count_false = score_calculation(test=request.data['test'])
        if count_true < 6:
            return Response(
                data={"true_answer": count_true, "false_answer": count_false, "score": count_true * 10,
                      "status": False},
                status=status.HTTP_200_OK)
        certificate_id = Sertifikate_ID_Serializer(user)
        serializer = Sertifikate_Serializer(user,
                                            data={"correct_answer": count_true, "wrong_answer": count_false,
                                                  "score": count_true * 10})
        path = create_certificate(certificate_id=certificate_id.data['certificate_id'],
                                  user_fullname=f"{serializer.data['last_name']} {serializer.data['first_name']}")
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"true_answer": count_true, "false_answer": count_false, "score": count_true * 10, "photo": path,
                 "status": True},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

