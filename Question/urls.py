from django.urls import path, register_converter

from .views import Create_User, Finish_User


# class TelegramIDConverter:
#     regex = '[0-9]+'
#
#     def to_python(self, value):
#         return int(value)
#
#     def to_url(self, value):
#         return str(value)


# register_converter(TelegramIDConverter, 'id')

urlpatterns = [
    path('create', Create_User),
    path('finish', Finish_User),
]
