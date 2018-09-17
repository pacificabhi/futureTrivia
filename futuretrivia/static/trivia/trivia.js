function register_contest_and_view(btn, code){
	btn.disabled=true;
	btn.innerHTML="Registering";

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			var resp = JSON.parse(this.responseText);
			if(resp.success == true){
				btn.removeAttribute("onclick");
				btn.setAttribute("onclick", "window.location.assign('/trivia/"+code+"')");// link to contest details
				btn.innerHTML = "View";
				btn.disabled = false;
			} else {
				show_popup(resp.error);
				btn.innerHTML = "Register";
				btn.disabled=false;
				
			}
		} else if(this.readyState == 4){
			btn.innerHTML = "Register";
			btn.disabled=false;
		}
	}
	var q = "code="+code;
	xhttp.open("GET", "/users/registercontest?"+q, true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send();
}



function register_contest_and_enter(btn, code, enter){
	btn.disabled=true;
	btn.innerHTML="Registering";

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			var resp = JSON.parse(this.responseText);
			if(resp.success == true){
				btn.removeAttribute("onclick");
				btn.setAttribute("onclick", "window.location.assign('#')");
				btn.innerHTML = "Enter";
				//alert(enter+" "+(enter == 'True'));
				if(enter == 'True'){
					btn.disabled = false;
				} else {
					btn.disabled = true;
				}
			} else {
				show_popup(resp.error);
				btn.innerHTML = "Register";
				btn.disabled=false;
				
			}
		} else if(this.readyState == 4){
			btn.innerHTML = "Register";
			btn.disabled=false;
		}
	}
	var q = "code="+code;
	xhttp.open("GET", "/users/registercontest?"+q, true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send();
}