function show_popup(text){
	document.getElementById("alert_data").innerHTML=text;
	var ele = document.getElementById("alert_popup_container");
	ele.style.display="flex";
	//ele.style.zIndex="+999999";
	ele.style.opacity="1";

	setTimeout(function(){
		ele.style.opacity="0";
	}, 1800);

	setTimeout(function(){
		ele.style.display="none";
	}, 2000);
}

function show_top_popup(text, close){
	document.getElementById("top_popup_text").innerHTML=text;
	var ele = document.getElementById("top_popup");
	ele.style.top="0px";
	
	if(close){
		setTimeout(function(){
			ele.style.top="-300px";
		}, 1000);
	}	

}



function checkBrowserOnline(){
	if(navigator.onLine){
		show_top_popup("Connected", true);
	} else {
		show_top_popup("You are not connected to internet", false);
	}
}

window.addEventListener("online", function(){
	checkBrowserOnline();
});

window.addEventListener("offline", function(){
	checkBrowserOnline();
});