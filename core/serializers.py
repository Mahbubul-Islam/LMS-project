from rest_framework import serializers
from .models import Category, Course, Lesson,Enrollment,QuestionAnswer, Material


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        field = '__all__'
        
        
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        field = '__all__'
        
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        field = '__all__'
        
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        field = '__all__'
        
class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        field = '__all__'