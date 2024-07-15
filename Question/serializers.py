from rest_framework.serializers import ModelSerializer

from .models import User


class User_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class Sertifikate_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['score', 'total_time']

# class Sertificate_Serializer(ModelSerializer):
#     class Meta:
#         model = Certificate
#         fields = '__all__'

# class Update_Courses_Serializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['info', 'photo', 'is_active']
#
#
# class Update_Courses_Title_Serializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['title']
