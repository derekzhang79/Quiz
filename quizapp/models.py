from django.db import models
from django.contrib.auth.models import User
__all__ = ["Quiz", "Result", "Question", "Choice"]

# Create your models here.
class Quiz(models.Model):
	title = models.TextField("Quiz title")
	user = models.ForeignKey(User, related_name='+')
	creation = models.DateTimeField(auto_now_add=True)
	desc = models.TextField("Description")
	shuffle = models.BooleanField("Shuffle choices?")
	def __unicode__(self):
		return self.title
	@property
	def score(self):
		scores = 0
		for i in self.question_set.all():
			scores += i.score
		return scores

class Result(models.Model):
	ip = models.IPAddressField()
	name = models.CharField(max_length=50)
	score = models.FloatField()
	time = models.DateTimeField(auto_now=True)
	quiz = models.ForeignKey("Quiz")
	refCode = models.CharField(max_length=4)
	def __unicode__(self):
		return self.name + " got " + unicode(self.score)

class Question(models.Model):
	title = models.TextField("Question")
	shuffle = models.BooleanField("Shuffle choices?")
	quiz = models.ForeignKey("Quiz")
	def __unicode__(self):
		return self.title
	@property
	def score(self):
		""" Find the max score for this question """
		pts = []
		for i in self.choice_set.all():
			pts.append(i.score)
		if len(pts) == 0: return 0
		return max(pts)
	@property
	def num_choice(self):
		return self.choice_set.all().count()

class Choice(models.Model):
	index = models.SmallIntegerField("Choice No. (if not shuffling)", default=0)
	text = models.TextField("Choice Text")
	score = models.SmallIntegerField(default=0)
	question = models.ForeignKey("question")
	def __unicode__(self):
		return self.text