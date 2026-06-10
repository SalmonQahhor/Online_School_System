from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


from .models import Submission
from .serializers import SubmissionSerializer, TeacherSubmissionSerializer
from .permissions import IsStudentOnly, IsTeacherOnly






class StudentSubmissionAPIView(APIView):
    permission_classes = [IsStudentOnly]


    def get(self, request):
        submission = Submission.objects.filter(student = request.user)
        serializer = SubmissionSerializer(submission, many=True)
        
        return Response({
            "message": "Siz yuborgan barcha vazifalar ro'yxati muvaffaqiyatli yuklandi.",
            "total_count": submission.count(),
            "results": serializer.data
        }, status=status.HTTP_200_OK)


    def post(self, request):
        serizlizer = SubmissionSerializer(data = request.data)
        serizlizer.is_valid(raise_exception=True)
        serizlizer.save(student=request.user)
        
        return Response({
            "message": "Vazifa yechimi tekshirish uchun muvaffaqiyatli yuborildi.",
            "data": serizlizer.data
        }, status=status.HTTP_201_CREATED)
        
        
        
class TeacherSubmissionAPIView(APIView):
    permission_classes = [IsTeacherOnly]

    def get(self, request):
        submissions = Submission.objects.all()
        serializer = TeacherSubmissionSerializer(submissions, many=True)
        
        return Response({
            "message": "Barcha talabalar yechimlari!",
            "data": serializer.data
        }, status=status.HTTP_200_OK)



class TeacherSubmissionDetailAPIView(APIView):
    permission_classes = [IsTeacherOnly]
    

    def get(self, request, id):
        submission = get_object_or_404(Submission, id=id)
        serializer = TeacherSubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, id):
        submission = get_object_or_404(Submission, id=id)
        
        serializer = TeacherSubmissionSerializer(submission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Talabaning ishi muvaffaqiyatli baholandi!",
            "data": serializer.data
        }, status=status.HTTP_200_OK)



























