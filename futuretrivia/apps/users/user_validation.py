import re, requests, json
from django.contrib.auth.models import User


#proxies = {'http': 'http://edcguest:edcguest@172.31.102.29:3128','https': 'https://edcguest:edcguest@172.31.102.29:3128','ftp': 'ftp://edcguest:edcguest@172.31.102.29:3128'}
proxies=None


def check_email_dns(email):
	r = requests.get("https://pozzad-email-validator.p.mashape.com/emailvalidator/validateEmail/%s"%(email),
	  headers={
	    "X-Mashape-Key": "LEvSDDoKLumshP4K4uDLKh9OGMD0p1jmHPWjsnlxByMKQO6KLM",
	    "X-Mashape-Host": "pozzad-email-validator.p.mashape.com"
	  },
	  proxies=proxies
	)
	
	j=json.loads(r.content.decode('ascii'))

	return j["isValid"]



def invalid_name(first_name, last_name):
	pattern=r'[^a-zA-Z]'
	if(re.search(pattern, first_name) or re.search(pattern, last_name)):
		return "Invalid Name, Only (A-Z) is allowed, No spaces allowed"
	return False


def validate_username(email):
	pattern=r'^[a-z_]{1}[a-z0-9_]{5,}$'
	if(re.match(pattern,email)):
		return True
	return False

def user_exists(username):
	if '@' in username:
		usr=User.objects.filter(email=username)
	else:
		usr=User.objects.filter(username=username)

	if usr:
		return True

	return False

def get_user(username):
	if '@' in username:
		usr=User.objects.filter(email=username)
	else:
		usr=User.objects.filter(username=username)

	if usr:
		return usr.first()

	return None

def validate_password(password):
	if(len(password)<8):
		return False
	return True