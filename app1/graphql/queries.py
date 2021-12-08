from app1.models import Course, Student
import graphene
from graphene_django import DjangoObjectType
import requests
import logging
from django_psql.custom_errors import APIException
from .model_type import CourseType, StudentType


logger = logging.getLogger('app')


class Query(graphene.ObjectType):
	request = graphene.String(token=graphene.String())
	all_courses = graphene.List(CourseType, name=graphene.String())
	all_students = graphene.List(StudentType, name=graphene.String(), course_id=graphene.Int())

	def resolve_request(root, info, token):
		if token == 'qwertyuiop':
			response  = requests.get(url="https://api.github.com/users/mralexgray/repos")

			logger.info('Response retrieved')

			return response.json()
		else:
			raise APIException("Invalid token", status=401)

	def resolve_all_courses(root, info, name=None):
		logger.info('All course records retrieved')
		return Course.objects.all()

	def resolve_all_students(root, info, name=None, course_id=None):
		logger.info('All students records retrieved')
		return Student.objects.all()