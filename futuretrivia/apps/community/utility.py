from futuretrivia.utility import *

def is_valid_trivia(form):
	
	tmp = form["tname"]["val"].strip()
	if len(tmp)<6 or len(tmp)>100:
		form["tname"]["error"]=True
		form["tname"]["error_msg"]="Length of name must be between 6 and 100 characters"
	else:
		form["tname"]["val"]=tmp

	tmp = form["tcategory"]["val"].strip()
	if len(tmp)<6 or len(tmp)>100:
		form["tcategory"]["error"]=True
		form["tcategory"]["error_msg"]="Length of name must be between 6 and 100 characters"
	else:
		form["tcategory"]["val"]=tmp

	tmp = form["tquote"]["val"].strip()
	if len(tmp)>100:
		form["tquote"]["error"]=True
		form["tquote"]["error_msg"]="Quote length must be less than 100 characters"
	else:
		form["tquote"]["val"]=tmp


	tmp = form["tabout"]["val"].strip()
	if len(tmp)>5000:
		form["tabout"]["error"]=True
		form["tabout"]["error_msg"]="Trivia about can not contain more than 5000 characters"
	else:
		if len(tmp)<=0:
			form["tabout"]["val"] = "No details"
		else:
			form["tabout"]["val"]=tmp


	tmp = form["tprizes"]["val"].strip()
	if len(tmp)>5000:
		form["tprizes"]["error"]=True
		form["tprizes"]["error_msg"]="Trivia Prizes details can not contain more than 5000 characters"
	else:
		if len(tmp)<=0:
			form["tprizes"]["val"] = "Not Declared"
		else:
			form["tprizes"]["val"]=tmp

		
	tmp = form["tannouncement"]["val"].strip()
	if len(tmp)>5000:
		form["tannouncement"]["error"]=True
		form["tannouncement"]["error_msg"]="Trivia announcements can not contain more than 5000 characters"
	else:
		if len(tmp)<=0:
			form["tannouncement"]["val"] = "No announcement"
		else:
			form["tannouncement"]["val"]=tmp

		