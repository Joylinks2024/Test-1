from rest_framework.serializers import ModelSerializer

from .models import User


class User_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class Sertifikate_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['correct_answer', 'wrong_answer', 'score', 'image']

    def create(self, validated_data):
        # Fayl yo'lini to'g'ri formatda olish
        image_path = validated_data.pop('image')
        sertifikate_instance = User.objects.create(**validated_data)
        sertifikate_instance.image = image_path
        sertifikate_instance.save()
        return sertifikate_instance


class Sertifikate_Info_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name']


class Time_Edit_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['started_time', 'finished_time']


class Time_Edit_Finish_Serializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['finished_time']

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
