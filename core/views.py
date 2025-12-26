from django.shortcuts import render
from .models import Category, Course, Lesson,Enrollment,QuestionAnswer, Material

from .serializers import CategorySerializer, CouseSerializer, LessonSerializer, EnrollmentSerializer, QuestionAnswerSerializer, MaterialSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q

from rest_framework.pagination import PageNumberPagination

# Create your views here.

# Category
@api_view(['GET','POST'])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all() # return queryset or  dictionary
        serializer = CategorySerializer(categories, many = True) # conver dictionary into json
        return Response(serializer.data, status = 200)
    
    elif request.mthod == 'POST':
        if not request.user.is_authenticated or request.user.role != 'admin':
            return Response({'detail' : 'Only admin can create categories'}, status=401)
        
        serializer = CategorySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
  
@api_view(['GET','POST'])      
def course_list_create(request):
    if request.method == 'GET':
        category = request.query_params.get('category')
        search = request.query_params.get('search')
        queryset = Course.objects.all()

        if category:
            queryset = queryset.filter(category__title__icontains = category)

        if search:
            queryset = queryset.filter(
                Q(title__icontains = search) |
                Q(description_icontains = search)
            )
        
        if request.user.is_authenticated and request.user.role == 'teacher':
            queryset = queryset.filter(instructor = request.user)
            
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        
        serializer = CouseSerializer(
            paginated_queryset,
            many = True,
            context = {'request' : request}
        )
        
        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_authenticated and request.user.role != 'teacher':
            return Response({'detail' : 'Only teacher can create courses'})
        serializer = CouseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def lesson_list_create(request):
    if request.method == 'GET':
        course = request.query_params.get('courseId')
        if not course:
            return Response({'detail' : 'course id is required'}, status=400)
        try:
            course = Course.objects.get(pk = course)
        except Course.DoesNotExist:
            return Response({'detail' : 'Course not found!'})
        
        is_teacher = request.user.is_authenticated and request.user.role == 'teacher'  and request.user == course.instructor
        
        is_admin = request.user.is_authenticated and request.user.role == 'admin'  and request.user == course.instructor
        
        is_enrolled = Enrollment.objects.filter(
            student = request.user,
            course = course,
            status = 'active'
        ).exists() if request.user.is_authenticated and request.user.role == 'student' else False
        
        if not (is_teacher or is_admin or is_enrolled):
            return Response({'detail' : "you don't have permission to view these lessons"},status=401)
        
        lessons = Lesson.objects.filter(course = course)
        serializer = LessonSerializer(lessons, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        course = request.query_params.get('courseId')
        if not course:
            return Response({'detail' : 'course id is required'}, status=400)
        try:
            course = Course.objects.get(pk = course)
        except Course.DoesNotExist:
            return Response({'detail' : 'Course not found!'})
        
        if request.user != course.instructor:
            return Response({'detail' : 'you can only add lesson to your own courses!'})
        
        serializer = LessonSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        
        return Response(serializer.errors, status=400)
        
        
            

        
