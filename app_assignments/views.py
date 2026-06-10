from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404


from .models import Group, Assignment
from .serializers import GroupSerializer, AssignmentSerializer
from .permissions import IsTeacherOrReadOnly



class GroupListCreateAPIView(GenericAPIView):
    permission_classes = [IsTeacherOrReadOnly]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    
    def get(self, request):
        group = self.get_queryset()
        serializer = self.get_serializer(group, many = True)
        
        return Response({
            "message": "Guruhlar ro'yxati",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
    
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return Response({
            "message": "Guruh yaratildi",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)




class GroupDetailAPIView(GenericAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_field = "id"
    
    
    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [IsTeacherOrReadOnly()]

    
    def get(self, request, id):
        group = self.get_object()
        serializer = self.get_serializer(group)
        
        return Response({
            "message": "Detail",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
    def patch(self, request, id): 
        serializer = self.get_serializer(instance = self.get_object(), data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        
        return Response({
            "message": "Muvaffaqiyatli o'zgartirildi!",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
    def delete(self, request, id):
        group = self.get_object()
        
        self.check_object_permissions(request, group)
        
        group.delete()
        
        return Response({
            "message": "Guruh muvaffaqiyatli o'chirildi"
        }, status=status.HTTP_200_OK)    
    
    
    
class AssignmentListCreateAPIView(GenericAPIView):
    permission_classes = [IsTeacherOrReadOnly]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    
    
    def get(self, request):
        assignments = self.get_queryset()
        serializer = self.get_serializer(assignments, many=True)
        
        return Response({
            "message": "Vazifalar ro'yxati",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Vazifa muvaffaqiyatli yaratildi",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class AssignmentDetailAPIView(GenericAPIView):
    permission_classes = [IsTeacherOrReadOnly]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    lookup_field = "id"
    
    
    def get(self, request):
        assignment = self.get_object()
        serializer = self.get_serializer(assignment)
        
        return Response({
            "message": "Vazifa tafsilotlari",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
    def patch(self, request, id):
        assignment = self.get_object()
        serializer = self.get_serializer(instance=assignment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Vazifa muvaffaqiyatli tahrirlandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
    def delete(self, request, id):
        assignment = self.get_object()
        self.check_object_permissions(request, assignment)
        assignment.delete()
        
        return Response({
            "message": "Vazifa muvaffaqiyatli o'chirildi"
        }, status=status.HTTP_200_OK)
