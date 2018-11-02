import secrets
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def send_email_confirmation_mail(host, ud, to):

	context = {"host": host}
	subject = 'Email Confirmation'
	token = secrets.token_urlsafe()
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