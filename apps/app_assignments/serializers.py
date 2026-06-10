from rest_framework import serializers
from django.utils import timezone


from .models import Group, Assignment



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'teacher', 'students']



class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'group', 'title', 'description', 'deadline', 'created_at']
        read_only_fields = ["created_at"]




    def validate(self, attrs):
        group = attrs.get("group")
        deadline = attrs.get("deadline") 
        
        request_user = self.context["request"].user
        
        
        if group and group.teacher != request_user:
            raise serializers.ValidationError({
                "group": "Siz faqat o'zingiz dars o'tadigan guruhlarga vazifa qo'sha olasiz!"
            })


        if deadline and deadline < timezone.now():
            raise serializers.ValidationError({
                "deadline": "Topshirish muddati hozirgi vaqtdan orqada bo'lishi mumkin emas!"
            })
            
        return attrs














