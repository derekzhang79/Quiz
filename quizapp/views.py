from quizapp.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import  reverse
from django.template import RequestContext
from django.http import HttpResponseForbidden, Http404
import random, string

def quizlist(request):
	return render_to_response("quizlist.html", {"quiz": Quiz.objects.all()})

def quizinfo(request, id):
	quiz = get_object_or_404(Quiz, pk=id)
	topq = quiz.result_set.order_by('-score')
	topscore = 0
	topppl = []
	for i in topq:
		if i.score > topscore:
			topscore = i.score
			topppl = []
		if topscore == i.score:
			topppl.append(i)
	lastentry = quiz.result_set.order_by('-time')[:5]
	return render_to_response("quizinfo.html", {"quiz": quiz, "topscore": topscore, "topppl": topppl, "lastentry": lastentry})

def doquiz(request, id):
	quiz = get_object_or_404(Quiz, pk=id)
	# FUCK FUCK FUCK YOU DJANGO
	# FREAKING STUPID PHILOSOPHIES
	quizl = []
	questlist = quiz.question_set.all()
	if quiz.shuffle:
		questlist = questlist.order_by("?")
	for i in questlist:
			choicelist = i.choice_set.all()
			if i.shuffle:
				choicelist = choicelist.order_by("?")
			else:
				choicelist = choicelist.order_by("index")
			quizl.append({"id": i.id, "title": i.title, "object": i, "choice": choicelist})
	return render_to_response("doquiz.html", {"quiz": quiz, "question": quizl}, context_instance=RequestContext(request))

def sendquiz(request, id):
	quiz = get_object_or_404(Quiz, pk=id)
	refCode = list(string.hexdigits.upper())
	random.shuffle(refCode)
	refCode = "".join(refCode[:4])
	score = 0
	for quest in quiz.question_set.all():
		sel = request.POST['q'+str(quest.id)]
		choice = Choice.objects.get(pk=sel)
		# 1: verify whether the selected choice is valid
		found = False
		for i in quest.choice_set.all():
			if i.id == choice.id:
				found = True
		if found == False:
			return HttpResponseForbidden("<h1>Invalid choice ID!</h1>") #hax
		# 2: add the score
		score += choice.score
	# Save result
	res = Result(ip=request.META['REMOTE_ADDR'], name=request.POST['name'], score=score, quiz=quiz, refCode=refCode)
	res.save()
	return render_to_response("results.html", {"quiz": quiz, "result": res, "justdone": True})

def result(request, id, resid, code, notused=None):
	quiz = get_object_or_404(Quiz, pk=id)
	res = get_object_or_404(Result, pk=resid)
	if res.quiz.id != quiz.id: raise Http404
	if res.refCode != code: return HttpResponseForbidden("<h1>Invalid refcode</h1>")
	return render_to_response("results.html", {"quiz": quiz, "result": res, "justdone": False})