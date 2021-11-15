from django.db import models


class Course(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Student(models.Model):
	name = models.CharField(max_length=30)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	mobile = models.CharField(max_length=30)

	def __str__(self):
		return self.name
