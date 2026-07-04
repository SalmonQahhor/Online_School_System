from django.db import models
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.app_assignments.models import Assignment



class Submission(models.Model):
    class Status(models.TextChoices):
        UNFINISHED = 'B', 'Bajarilmagan'
        PENDING = 'K', 'Kutilmoqda'
        ACCEPTED = 'Q', 'Qabul qilindi'
        REJECTED = 'R', 'Rad etildi'

    assignment = models.ForeignKey(to=Assignment, on_delete=models.CASCADE, verbose_name="Vazifa")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Talaba")
    file = models.FileField(upload_to='submissions/', null=True, blank=True, verbose_name="Yechim fayli")
    answer_text = models.TextField(blank=True, verbose_name="Yozma javob")
    grade = models.IntegerField(null=True, blank=True, verbose_name="Baholash (Ball)")
    teacher_comment = models.TextField(blank=True, verbose_name="O'qituvchi izohi")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.UNFINISHED, verbose_name="Holati")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqti")


    class Meta:
        verbose_name = "Topshiriq yechimi"
        verbose_name_plural = "Topshiriq yechimlari"


    def __str__(self):
        return f"{self.student.username} -> {self.assignment.title}"
    
    
    def save(self, *args, **kwargs):
       
        if not self.id:
            if self.assignment.deadline and self.assignment.deadline < timezone.now():
                raise ValidationError("Kechirasiz, ushbu vazifani topshirish muddati tugagan!")
            
            self.status = self.Status.PENDIN
      
        if self.grade is not None:
            if self.grade >= 60: 
                self.status = self.Status.ACCEPTED
            else:
                self.status = self.Status.REJECTED
        
        super().save(*args, **kwargs)