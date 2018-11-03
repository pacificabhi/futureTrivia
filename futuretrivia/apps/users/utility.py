import secrets
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def send_email_confirmation_mail(host, ud, to):

	context = {"host": host}
	subject = 'Email Confirmation'
	token = secrets.token_urlsafe(64)
	ud.confirm_token = token
	ud.confirmed = False
	context["confirm_token"] = token
	message = render_to_string('users/email_confirm_template.html', context)
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [to,]

	msg = EmailMessage(subject=subject, body=message, from_email=email_from, to=recipient_list)
	msg.content_subtype = "html"  # Main content is now text/html
	res = msg.send()
	ud.save()
	return res



def is_account_confirmed(request):
	
	return request.user.userdetails.confirmed

def send_password_reset_mail(user):

	subject = 'Password Reset'
	new_pass = secrets.token_urlsafe(9)
	
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [user.email,]
	user.set_password(new_pass)

	message = "You are recieving this mail because you requested for new password.<br><br> Your username is <b>%s</b><br><br>Your New Password is <font color='red'><b>%s</b></font><br><br><b>Note:</b> Please change your password after you log in with this password.<br><br>Thank you"%(user.username, new_pass)

	msg = EmailMessage(subject=subject, body=message, from_email=email_from, to=recipient_list)
	msg.content_subtype = "html"  # Main content is now text/html
	res = msg.send()
	if res:
		user.save()
	return res

