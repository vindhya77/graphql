from app1.models import Course, Student
import graphene
from graphene_django import DjangoObjectType

class CourseType(DjangoObjectType):
	class Meta:
		model = Course
		fields = '__all__'


class StudentType(DjangoObjectType):
	class Meta:
		model = Student
		fields = '__all__'