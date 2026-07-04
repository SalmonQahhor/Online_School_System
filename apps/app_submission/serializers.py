from rest_framework import serializers
from django.utils import timezone


from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ['student', 'grade', 'teacher_comment', 'status']
        
        
    def validate(self, attrs):
        if not self.instance:
            assignment = attrs.get('assignment')
            if assignment and assignment.deadline < timezone.now():
                raise serializers.ValidationError(
                    {"message": "Ushbu vazifani topshirish muddati yakunlangan! Kechikdingiz."}
                )
            
        return attrs


class TeacherSubmissionSerializer(serializers.ModelSerializer):
     class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ['assignment', 'student', 'file', 'answer_text', 'submitted_at']
