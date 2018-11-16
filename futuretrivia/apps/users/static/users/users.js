

window.fbAsyncInit = function() {
	FB.init({
	    appId            : '312299856007804',
	    autoLogAppEvents : true,
	    cookie           : true,
	    xfbml            : true,
	    version          : 'v3.2'
	});
    
};

  (function(d, s, id){
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) {return;}
      js = d.createElement(s); js.id = id;
      js.src = "https://connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));

/*
function checkStatus(){
    FB.getLoginStatus(function(response) {
        var roo = document.getElementById("root");
        document.getElementById("btn-control").style.display="block";
        roo.innerHTML = "";
        if (response.status === 'connected') {
            var s="Logged in<br>";
            FB.api('/me', {locale: 'en_US', fields:'name, email'}, function(user){
                s+="your name is <b>"+user.name+"</b> <br> your email is <b>"+user.email+"</b><br>";
                //console.log(user);
                roo.innerHTML=s;
            });

            roo.innerHTML=s;
            document.getElementById("login-btn").style.display = "none";
            document.getElementById("logout-btn").style.display = "inline-block";
        
        } else {
            roo.innerHTML="You are not logged in<br>"
            document.getElementById("login-btn").style.display = "inline-block";
            document.getElementById("logout-btn").style.display = "none";          
        }
    });

}*/



function fblogout(){

    FB.logout(function(response){

    });

}

function fblogin(){

	var fb_btn = document.getElementById("fb-login-btn");
	fb_btn.disabled=true;
	fb_btn.innerHTML="Verifying User";
	document.getElementById("baseauthform").style.display="none";
	var b_btn = document.getElementById("baseauthbtn");
	b_btn.disabled=true;
	b_btn.style.display="inline-block";


	FB.login((resp)=>{
		console.log(resp);
		if(resp.status=="connected"){
			do_request(resp);

		} else {
			fb_btn = document.getElementById("fb-login-btn");
			fb_btn.disabled=false;
			fb_btn.innerHTML="Continue with Facebook"
			b_btn.disabled=false;
			show_top_popup("something went wrong", true, 5000);
		}
	}, {scope: 'public_profile,email'}, true);

}

function do_request(user){

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		//console.log(this.status);
		if(this.readyState == 4 && this.status == 200){
			var resp = JSON.parse(this.responseText);
			console.log(resp);
			if(resp.success == true){
				var fb_btn = document.getElementById("fb-login-btn");
				fb_btn.innerHTML="Logging you in";
				window.location.reload();
			} else {
				var fb_btn = document.getElementById("fb-login-btn");
				fb_btn.disabled=false;
				fb_btn.innerHTML="Continue with Facebook";
				show_top_popup(resp.error, true, 4500);
			}
		} else if(this.readyState == 4 && this.status == 403){
			window.location.reload();
		}
	}


	user = encodeURIComponent(JSON.stringify(user));
	//console.log(user);
	
	var token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

	var q = "csrfmiddlewaretoken="+token+"&user="+user;
	xhttp.open("POST", "/users/fblogin/", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
	xhttp.send(q);
}

