from django.db import models
from django.conf import settings




class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Gurh nomi")
    teacher = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name="O'qituvchi", related_name='taught_groups', on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='enrolled_groups')


    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        
        
    def __str__(self):
        return self.name


class Assignment(models.Model):
    group = models.ForeignKey(to=Group, verbose_name="Guruh", on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(verbose_name="Vazifa nomi", max_length=200)
    description = models.TextField(verbose_name="Vazifa tavsifi")
    deadline = models.DateTimeField( verbose_name="Topshirish muddati",db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Berilgan vaqti", db_index=True)
    
    
    class Meta:
        verbose_name = "Vazifa"
        verbose_name_plural = "Vazifalar"
        

def __str__(self):
    return f"{self.title} — {self.group.name} ({self.created_at.strftime('%d.%m.%Y %H:%M')})"