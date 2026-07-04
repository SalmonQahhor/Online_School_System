from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


from .models import Submission
from .serializers import SubmissionSerializer, TeacherSubmissionSerializer

from .permissions import IsStudentOnly, IsTeacherOnly


class StudentSubmissionAPIView(GenericAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudentOnly]

    def get_queryset(self):
        return Submission.objects.select_related("assignment", "student").filter(student = self.request.user)

    def get(self, request):
        submissions = self.get_queryset()
        serializer = self.get_serializer(submissions, many=True)

        return Response({
            "message": "Siz yuborgan barcha vazifalar ro'yxati muvaffaqiyatli yuklandi.",
            "total_count": submissions.count(),
            "results": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(student=request.user)

        return Response({
            "message": "Vazifa yechimi tekshirish uchun muvaffaqiyatli yuborildi.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class TeacherSubmissionAPIView(GenericAPIView):
    serializer_class = TeacherSubmissionSerializer
    permission_classes = [IsTeacherOnly]

    def get_queryset(self):
        return Submission.objects.select_related("assignment", "student").all()


    def get(self, request):
        submissions = self.get_queryset()  
        serializer = self.get_serializer(submissions, many=True)

        return Response({
            "message": "Barcha talabalar yechimlari!",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class TeacherSubmissionDetailAPIView(GenericAPIView):
    serializer_class = TeacherSubmissionSerializer
    permission_classes = [IsTeacherOnly]
    lookup_field = "id" 


    def get_queryset(self):
        return Submission.objects.select_related("assignment", "student").all()


    def get(self, request, id):
        submission = self.get_object() 
        serializer = self.get_serializer(submission)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
        

    def put(self, request, id):
        submission = self.get_object()  

        serializer = self.get_serializer(submission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Talabaning ishi muvaffaqiyatli baholandi!",
            "data": serializer.data
        }, status=status.HTTP_200_OK)