import pytz, datetime, ast


def get_endtime(trivia):
	# return endtime of contest
	return trivia.start_time + datetime.timedelta(seconds=trivia.portal_duration)


def trivia_ended(trivia):
	pass

def get_question(q_obj):
	question={"restrict_timing": False}

	question["id"] = q_obj.id
	question["statement"] = q_obj.question
	question["mcq"]=q_obj.mcq
	question["title"]=q_obj.get_title()
	if q_obj.duration:
		question["restrict_timing"]=True
		question["duration"]=q_obj.duration

	question["positive_score"] = q_obj.positive_score
	question["negative_score"] = q_obj.negative_score
	options = []

	opt_dict = ast.literal_eval(q_obj.options)

	for o_id in opt_dict.keys():
		option = {"id": o_id, "value": opt_dict[o_id]}
		options.append(option)

	question["options"] = options

	return question

def get_answer_status(q_obj, answers):
	answer = {}
	q_id = q_obj.id
	answers = ast.literal_eval(answers)
	if q_id in answers.keys():
		answer["time_elapsed"] = answers[q_id]["time_elapsed"]
		answer["opt_id"] = answers[q_id]["opt_id"]
	else:
		answer["time_elapsed"]=0
		answer["opt_id"]=0

	return answer

def submitted(result):

	return result.time_taken