from futuretrivia.utility import *
import datetime, pytz


def check_date_format(date_str):
	pass

def check_time_format(time_str):
	pass

def change_datetime(dt, dst):
	""" function to convert naive time from one timezone to UTC
		dst is time difference between utc and initial timezone
		dst is a string in format "05:30"

		dt is initial datetime object"""
	#print(dst.strip().split(":"))
	hr, s = map(int, dst.strip().split(":"))
	sign = hr//abs(hr)
	dst_in_seconds = abs(hr)*3600+s*60
	dst_in_seconds*=sign

	utc = pytz.UTC

	return (dt-datetime.timedelta(seconds=dst_in_seconds)).replace(tzinfo=utc)




def is_valid_trivia(form):

	valid = True

	trivia = {}
	errors = {}
	
	tmp = form["tname"]["val"].strip()
	if len(tmp)<6 or len(tmp)>100:
		valid=False
		errors[form["tname"]["id_selector"]]="Length of name must be between 6 and 100 characters"
	else:
		trivia["name"]=tmp

	tmp = form["tcategory"]["val"].strip()
	if len(tmp)<6 or len(tmp)>100:
		valid=False
		errors[form["tcategory"]["id_selector"]]="Length of name must be between 6 and 100 characters"
	else:
		trivia["category"]=tmp

	tmp = form["tquote"]["val"].strip()
	if len(tmp)>100:
		valid=False
		errors[form["tquote"]["id_selector"]]="Quote length must be less than 100 characters"
	else:
		trivia["quote"]=tmp


	tmp = form["tposter"]["val"].strip()
	if len(tmp)>2000:
		valid=False
		errors[form["tposter"]["id_selector"]]="URL is too long"
	else:
		trivia["poster"]=tmp


	tmp = form["tabout"]["val"].strip()
	if len(tmp)>5000:
		valid=False
		errors[form["tabout"]["id_selector"]]="Trivia about can not contain more than 5000 characters"
	else:
		if len(tmp)<=0:
			trivia["about"] = "No details"
		else:
			trivia["about"] = tmp


	tmp = form["tprizes"]["val"].strip()
	if len(tmp)>5000:
		valid=False
		errors[form["tprizes"]["id_selector"]]="Trivia Prizes details can not contain more than 5000 characters"
	else:
		if len(tmp)<=0:
			trivia["prizes"] = "Not Declared"
		else:
			trivia["prizes"] = tmp

		
	tmp = form["tannouncement"]["val"].strip()
	if len(tmp)>5000:
		valid=False
		errors[form["tannouncement"]["id_selector"]]="Trivia announcements can not contain more than 5000 characters"
	else:
		if len(tmp)<=0:
			trivia["announcement"] = "No announcement"
		else:
			trivia["announcement"] = tmp


	#checking start date and ttime

	tmpdatestr = form["tstartdate"]["val"].strip()
	tmptimestr = form["tstarttime"]["val"].strip()
	tmpdatetime = datetime.datetime.strptime(tmpdatestr+" "+tmptimestr,"%Y-%m-%d %H:%M")
	tmpdatetime = change_datetime(tmpdatetime, "05:30")
	now=get_current_time()

	if tmpdatetime<=now:
		valid=False
		if tmpdatetime.date()<now.date():
			errors[form["tstartdate"]["id_selector"]]="Date can not be in past"
		else:
			errors[form["tstarttime"]["id_selector"]]="Time can not be in past"

	else:
		trivia["start_time"]=tmpdatetime


	tmp = int(form["tportalduration"]["val"].strip())
	if tmp<=0:
		valid=False
		errors[form["tportalduration"]["id_selector"]]="Portal must be open for atleast 1 second"
	else:
		trivia["portal_duration"] = tmp


	individual = form["tindividualtiming"]
	trivia["individual_timing"] = individual
	if individual:
		tmp = int(form["tduration"]["val"].strip())
		if tmp<=0:
			valid=False
			errors[form["tduration"]["id_selector"]]="Duration must be greater tah 1 second"
		else:
			trivia["duration"] = tmp
	else:
		trivia["duration"] = trivia["portal_duration"]

	private = form["tprivate"]
	trivia["private"] = private
	if private:
		tmp = form["tpassword"]["val"]
		if tmp<=0:
			valid=False
			errors[form["tpassword"]["id_selector"]]="Password can not be blank"
		else:
			trivia["password"] = tmp

	else:
		trivia["password"]=""

	trivia["can_change_answer"]=form["tcanchangeanswer"]
	trivia["ready"]=form["tready"]

	if valid:
		return True, trivia


	return False, errors


