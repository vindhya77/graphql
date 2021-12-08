import graphene
from graphene_django import DjangoObjectType
import requests
import logging
from django_psql.custom_errors import APIException
from app1.models import Course, Student
from .model_type import CourseType, StudentType


logger = logging.getLogger('app')


class CreateCourse(graphene.Mutation):
	class Arguments:
		name = graphene.String()

	courses = graphene.Field(CourseType)

	def mutate(self, info, name):
		courses = Course.objects.create(name=name)
		logger.info('New course record created')
		return CreateCourse(courses=courses)


class UpdateCourse(graphene.Mutation):
	class Arguments:
		name = graphene.String()
		id = graphene.Int()

	courses = graphene.Field(CourseType)

	def mutate(self, info, id, name=None):
		course = Course.objects.filter(id=id).first()
		if course:
			course.name = name if name is not None else course.name
			course.save()
			logger.info("Update of course record successful")
		return UpdateCourse(courses=course)


class DeleteCourse(graphene.Mutation):
	class Arguments:
		id = graphene.Int()

	courses = graphene.Field(CourseType)

	def mutate(self, info, id):
		course = Course.objects.filter(id=id).first()
		if course:
			course.delete()
			logger.info('Course record deleted successful')
		return DeleteCourse(courses=course)


class Mutations(graphene.ObjectType):
	create_course = CreateCourse.Field()
	update_course = UpdateCourse.Field()
	delete_course = DeleteCourse.Field()