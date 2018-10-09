import pytz, datetime, ast

def get_current_time():

	return datetime.datetime.now().replace(tzinfo=pytz.utc)

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