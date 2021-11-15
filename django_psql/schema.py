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


class CreateCourse(graphene.Mutation):
	class Arguments:
		name = graphene.String()

	courses = graphene.Field(CourseType)

	def mutate(self, info, name):
		courses = Course.objects.create(name=name)
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
		return UpdateCourse(courses=course)


class DeleteCourse(graphene.Mutation):
	class Arguments:
		id = graphene.Int()

	courses = graphene.Field(CourseType)

	def mutate(self, info, id):
		course = Course.objects.filter(id=id).first()
		if course:
			course.delete()
		return DeleteCourse(courses=course)


class Query(graphene.ObjectType):
	all_courses = graphene.List(CourseType, name=graphene.String())
	all_students = graphene.List(StudentType, name=graphene.String(), course_id=graphene.Int())

	def resolve_all_courses(root, info, name=None):
		return Course.objects.all()

	def resolve_all_students(root, info, name=None, course_id=None):
		return Student.objects.all()


class Mutations(graphene.ObjectType):
	create_course = CreateCourse.Field()
	update_course = UpdateCourse.Field()
	delete_course = DeleteCourse.Field()

schema = graphene.Schema(query=Query, auto_camelcase=False, mutation=Mutations)

