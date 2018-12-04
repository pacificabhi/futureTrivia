from django.db import models
from django.contrib.auth.models import User
import ast
import datetime
from futuretrivia.utility import get_current_time

# Create your models here.

class Trivia(models.Model):

	admin = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=False, null=False)
	code = models.CharField(max_length=20, blank=False, null=False, unique=True)
	password = models.CharField(max_length=40, blank=True, null=False, default="")
	category = models.CharField(max_length=100, blank=False, null=False, default="General")
	poster = models.CharField(max_length=2000, blank=True, null=False)
	quote = models.CharField(max_length=100, blank=True, null=False)
	stars = models.TextField(blank=False, null=False, default="0,0,0,0,0")

	prizes = models.TextField(max_length=5000, blank=False, null=False, default="Not Declared")
	about = models.TextField(blank=False, null=False, max_length=5000, default="No details.")
	announcements = models.TextField(blank=False, null=False, max_length=5000, default="No Announcements")

	start_time = models.DateTimeField(blank=True, null=True)
	end_time = models.DateTimeField(blank=True, null=True)
	duration = models.IntegerField(blank=False, null=False, default=0)
	#per_questions_duration = models.IntegerField(blank=False, null=False, default=0)
	portal_duration = models.IntegerField(blank=False, null=False, default=0)


	#can_navigate = models.BooleanField(blank=False, null=False, default=False)
	can_change_answer = models.BooleanField(blank=False, null=False, default=False)
	individual_timing = models.BooleanField(blank=False, null=False, default=True)
	#question_timing = models.BooleanField(blank=False, null=False, default=True)
	#live = models.BooleanField(blank=False, null=False, default=False)
	rated = models.BooleanField(blank=False, null=False, default=False)
	private = models.BooleanField(blank=False, null=False, default=False)
	ready = models.BooleanField(blank=False, null=False, default=False)
	locked = models.BooleanField(blank=False, null=False, default=False)
	

	def __str__(self):
		return self.code


	def set_endtime(self):

		self.end_time = self.start_time + datetime.timedelta(seconds=self.portal_duration)
		

	def total_questions(self):
		return self.question_set.all().count()

	def total_registered(self):
		return self.userdetails_set.all().count()

	def get_endtime(self):

		if self.end_time:
			return self.end_time
		
		return self.start_time + datetime.timedelta(seconds=self.portal_duration)


	def is_ended(self):

		return self.get_endtime()<=get_current_time()

	def is_fully_ended(self):
		
		now = get_current_time()

		if self.individual_timing:
			return (self.start_time + datetime.timedelta(seconds=(self.portal_duration+self.duration)))<=now
		
		return self.get_endtime()<=now


	def is_started(self):

		if not self.start_time:
			return None
		return self.start_time<=get_current_time()

	def time_to_start(self):
		return int((self.start_time-get_current_time()).total_seconds())

	def time_to_end(self):

		if not self.is_started():
			return None

		return int((self.get_endtime()-get_current_time()).total_seconds())


	def get_rating(self):

		rating_list = list(map(int, self.stars.strip().split(',')))
		sm=0
		tot=0
		for i in range(5):
			sm+=((i+1)*rating_list[i])
			tot+=rating_list[i]

		if tot==0:
			return {"color":"text-secondary", "rating": "Review not available"}

		rate = sm/tot

		color = "text-secondary"

		if rate<=1:
			color = "text-danger"
		elif rate<3:
			color = "text-warning"
		elif rate<4:
			color = "text-info"
		else:
			color = "text-success"

		return {"yes": True,"color": color, "rating": '%.2f'%rate, "total": tot}


	def lock(self):
		
		"""end_time_for_lock = None

		if self.individual_timing:
			end_time_for_lock = self.start_time + datetime.timedelta(seconds=(self.portal_duration+self.duration))
		else:
			end_time_for_lock = self.get_endtime()

		now = get_current_time()"""

		if not self.is_fully_ended():
			return False

		results_left = TriviaResult.objects.filter(time_taken=0, trivia=self)
		questions = self.question_set.all()

		for result in results_left:
			timi = None
			if self.individual_timing:
				timi = self.duration
			else:
				timi = self.portal_duration

			result.calculate_score(questions_set=questions)
			result.time_taken = timi
			result.save()


		results = self.triviaresult_set.extra(select={'total_score':'positive_score - negative_score'}, order_by=('-total_score', 'time_taken'))
		
		for i in range(len(results)):

			results[i].rank=i+1
			results[i].save()

		self.locked=True
		self.save()
		return True

	def get_duration_string(self):

		dur = self.duration
		durs = ''
		days = dur//86400
		if days>0:
			if days==1:
				durs+="%d day "%(days)
			else:
				durs+="%d days "%(days)

		dur=dur%86400
		hrs=dur//3600

		if hrs>0:
			if hrs==1:
				durs+="%d hour "%(hrs)
			else:
				durs+="%d hours "%(hrs)

		dur=dur%3600
		mins = dur//60

		if mins>0:
			if mins==1:
				durs+="%d minute "%(mins)
			else:
				durs+="%d minutes "%(mins)

		dur=dur%60

		if dur>0:
			if dur==1:
				durs+="%d second "%(dur)
			else:
				durs+="%d seconds "%(dur)

		return durs




class Question(models.Model):
	
	trivia = models.ForeignKey(Trivia,on_delete=models.CASCADE)
	title = models.CharField(max_length=40, blank=False, null=False, default=" ")
	question = models.TextField(blank=False, null=False)
	mcq = models.BooleanField(blank=False, null=False, default=True)
	positive_score = models.IntegerField(blank=False, null=False, default=0)
	negative_score = models.IntegerField(blank=False, null=False, default=0)
	duration = models.IntegerField(blank=False, null=False, default=0)

	options = models.TextField(blank=False, null=False, default="{}")

	correct_answer = models.IntegerField(blank=False, null=False, default=0)

	explaination = models.TextField(blank=False, null=False, default = "No explaination")


	def get_title(self):
		return self.title




	def get_question(self):
		question={"restrict_timing": False}

		question["id"] = self.id
		question["statement"] = self.question
		question["mcq"]=self.mcq
		question["title"]=self.get_title()
		if self.duration:
			question["restrict_timing"]=True
			question["duration"]=self.duration

		question["positive_score"] = self.positive_score
		question["negative_score"] = self.negative_score
		options = []

		opt_dict = ast.literal_eval(self.options)

		for o_id in opt_dict.keys():
			option = {"id": o_id, "value": opt_dict[o_id]}
			options.append(option)

		question["options"] = options

		return question

	

	def __str__(self):
		return self.trivia.code+'_'+self.title




class TriviaResult(models.Model):

	trivia = models.ForeignKey(Trivia,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	start_time = models.DateTimeField(blank=True, null=True)
	modified_at = models.DateTimeField(blank=True, null=True)
	time_taken = models.IntegerField(blank=False, null=False, default=0)
	rank = models.IntegerField(blank=False, null=False, default=0)

	answers = models.TextField(blank=False, null=False, default="{}")

	positive_score = models.IntegerField(blank=False, null=False, default=0)
	negative_score = models.IntegerField(blank=False, null=False, default=0)
	stars = models.IntegerField(blank=False, null=False, default=0)


	def __str__(self):
		return self.user.username+'_'+self.trivia.code



	def calculate_score(self, questions_set=None):

		if self.submitted():
			return None

		if not questions_set:
			questions_set = self.trivia.question_set.all()
		
		answers = ast.literal_eval(self.answers)

		for ques in questions_set:
			if ques.id in answers.keys() and answers[ques.id]["opt_id"]!=0:

				if ques.correct_answer == answers[ques.id]["opt_id"]:
					self.positive_score+=ques.positive_score
				else:
					self.negative_score+=ques.negative_score

		#self.total_score = self.positive_score - self.negative_score

	def get_timetaken_string(self):

		tt = self.time_taken

		hrs = tt//3600
		tt=tt%3600

		mins = tt//60
		tt=tt%60

		return "%d:%d:%d"%(hrs,mins,tt)



	def get_score(self):

		return self.positive_score - self.negative_score

	def submitted(self):

		return self.time_taken

