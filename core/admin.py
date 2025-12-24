from django.contrib import admin
from .models import Category, Course, Lesson,Enrollment,QuestionAnswer, Material

# Register your models here.

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(QuestionAnswer)
admin.site.register(Material)