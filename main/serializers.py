from rest_framework import serializers
from .models import Courses,Universities,Student,Acknowledgements
from .models import Aspnetusers, Aspnetuserroles, Acknowledgements, Aspnetroles



class CourseSerializer(serializers.Serializer):
    class Meta:
        model=Courses
        fields='__all'

class UniversitySerializer(serializers.Serializer):
    class Meta:
        model=Universities
        fields='__all__'

class StudentSerializer(serializers.Serializer):
    class Meta:
        model=Student
        fields='all'

class AcknowledgementsSerializer(serializers.Serializer):
    name= serializers.CharField()
    course=CourseSerializer(read_only=True)
    student=StudentSerializer(read_only=True)
    class Meta:
        model=Acknowledgements
        fields='__all__'

class AspNetUserSerializer(serializers.Serializer):
    class Meta:
        model= Aspnetusers
        fields=['email','username','id']