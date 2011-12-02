from quiz.quizapp.models import *
from django.contrib import admin

for i in [Result]:
	admin.site.register(i)

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 4

class QuestionInline(admin.TabularInline):
	model = Question
	extra = 1

class QuizAdmin(admin.ModelAdmin):
	date_hierarchy = "creation"
	fields = ('title','user', 'desc', 'shuffle')
	list_display = ["title", "user", "creation", "score", 'shuffle']
	#inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
	inlines = [ChoiceInline]
	list_display = ["title", "quiz", "score", "num_choice"]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)