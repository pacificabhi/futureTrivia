function register_contest_and_enter(btn, code){
	btn.disabled=true;
	btn.innerHTML="Registering...";

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			var resp = JSON.parse(this.responseText);
			if(resp.success == true){
				window.location.reload();
				show_popup("You are registered");
			} else {
				show_top_popup(resp.error, true, 3000);
				if(!resp.auth){
					window.location.reload();
				}
				btn.innerHTML = "Click to Register";
				btn.disabled=false;
				
			}
		} else if(this.readyState == 4){
			btn.innerHTML = "Click to Register";
			btn.disabled=false;
		}
	};
	var q = "code="+code;
	xhttp.open("GET", "/users/registercontest?"+q, true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send();
}