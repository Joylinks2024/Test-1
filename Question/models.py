import uuid

from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    passport_serial_number = models.CharField(max_length=9, unique=True)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField()
    score = models.IntegerField(blank=True, null=True)
    total_time = models.CharField(max_length=10, blank=True, null=True)
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    started_time = models.DateTimeField(null=True, blank=True)
    finished_time = models.DateTimeField(null=True, blank=True)
    objects = models.Manager()

    class Meta:
        ordering = ['-created_time']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
