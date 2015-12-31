function device_select () {
	var part_select = document.getElementById("part_select");

	while(part_select.length > 0)
	{
		part_select.remove(0);
	}

	var family_select = document.getElementById("family_select");
	var family_index = family_select.selectedIndex;
	if(family_index == -1)
	{
		return;
	}

	var family = family_select.options[family_index].text;
	var parts = device_map[family];

	for(var i = 0; i < parts.length; i++)
	{
		var option = document.createElement("option");
		option.text = parts[i];
		option.value = parts[i];
		part_select.add(option);
	}
}

function load_animation (part) {
	var msg = "<p>Loading " + part + ". This may take a minute or two. The page will automatically refresh when done</p>";
	var loader_body = document.getElementById("loader_body");
	loader_body.innerHTML = msg + "<div class=\"spinner-loader\">_Patience_</div>";
}

function device_load_submit () {
	var part_select = document.getElementById("part_select");
	var index = part_select.selectedIndex;

	if(index == -1)
	{
		return;
	}

	var part = part_select.options[index].text;


	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200)
		{
			window.location.href = "/";
		}
		else if(xhttp.readyState == 4)
		{
			alert("Server indicated that it failed to load the device :(");
		}
  	}
  	xhttp.open("POST", "/", true);
  	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  	xhttp.send("part=" + part);
		load_animation(part);

}

function part_load_submit () {
	var part = document.getElementById("direct_part_name").value;

	if(typeof part === 'undefined')
	{
		return;
	}

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200)
		{
			window.location.href = "/";
		}
		else if(xhttp.readyState == 4)
		{
			alert("Server indicated that it failed to load the device :(");
		}
  	}
  	xhttp.open("POST", "/", true);
  	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  	xhttp.send("part=" + part);

  	load_animation(part);
}
