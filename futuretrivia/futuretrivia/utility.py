import pytz, datetime, ast

def get_current_time():

	return datetime.datetime.now().replace(tzinfo=pytz.utc)
