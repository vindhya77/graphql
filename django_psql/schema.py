from app1.models import Course, Student
import graphene
from graphene_django import DjangoObjectType
import requests
import logging


# logging.basicConfig(filename="logs/course_record.log", level=logging.INFO)
logger = logging.getLogger(__file__)




class CourseType(DjangoObjectType):
	class Meta:
		model = Course
		fields = '__all__'


class StudentType(DjangoObjectType):
	class Meta:
		model = Student
		fields = '__all__'


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
			logger.debug('Course record deleted successful')
		return DeleteCourse(courses=course)


logging.basicConfig(filename="logs/request_logs.log", level=logging.info)


class Query(graphene.ObjectType):
	request = graphene.String(token=graphene.String())
	all_courses = graphene.List(CourseType, name=graphene.String())
	all_students = graphene.List(StudentType, name=graphene.String(), course_id=graphene.Int())

	def resolve_request(root, info, token):
		if token == 'qwertyuiop':
			response  = requests.get(url="https://api.github.com/users/mralexgray/repos")

			logging.info('Got success response')

			return response.json()

	def resolve_all_courses(root, info, name=None):
		return Course.objects.all()

	def resolve_all_students(root, info, name=None, course_id=None):
		return Student.objects.all()


class Mutations(graphene.ObjectType):
	create_course = CreateCourse.Field()
	update_course = UpdateCourse.Field()
	delete_course = DeleteCourse.Field()

schema = graphene.Schema(query=Query, auto_camelcase=False, mutation=Mutations)

