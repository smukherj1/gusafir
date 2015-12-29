
var lookupMap = [];

function clear_x() {
	var select = document.getElementById("x_select");
	while(select.length > 0)
	{
		select.remove(0);
	}

}

function clear_y() {
	var select = document.getElementById("y_select");
	while(select.length > 0)
	{
		select.remove(0);
	}

}

function clear_z() {
	var select = document.getElementById("z_select");
	while(select.length > 0)
	{
		select.remove(0);
	}

}

function clear_i() {
	var select = document.getElementById("i_select");
	while(select.length > 0)
	{
		select.remove(0);
	}

}

function elem_populate(xhttp) {
	// Set the global lookup map
	lookupMap = JSON.parse(xhttp.responseText);
	var select = document.getElementById("x_select");

	var coords = Object.keys(lookupMap);
	for(var i = 0; i < coords.length; i++)
	{
		var option = document.createElement("option");
		option.text = coords[i];
		option.value = coords[i];
		select.add(option);
	}
	x_selectcb();
}

function elem_selectcb () {
	var elem_select = document.getElementById("elem_select");
	var index = elem_select.selectedIndex;

	if(index == -1)
	{
		return;
	}

	var elem = elem_select.options[index].text;

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200)
		{
			elem_populate(xhttp);
		}
		else if(xhttp.readyState == 4)
		{
			alert("Server failed to respond to request for elements of type " + elem);
		}
  	}
  	clear_x();
	clear_y();
	clear_z();
	clear_i();

  	xhttp.open("GET", "/elems?elem=" + elem, true);
  	xhttp.send();
}

function x_selectcb () {
	var x_select = document.getElementById("x_select");
	var xidx = x_select.selectedIndex;

	if(xidx == -1)
	{
		return;
	}

	clear_y();
	clear_z();
	clear_i();

	var y_select = document.getElementById("y_select");
	var x = x_select.options[xidx].text;
	var y_coords = Object.keys(lookupMap[x]);

	for(var i = 0; i < y_coords.length; i++)
	{
		var option = document.createElement("option");
		option.text = y_coords[i];
		option.value = y_coords[i];
		y_select.add(option);
	}

	y_selectcb();
}

function y_selectcb () {
	var x_select = document.getElementById("x_select");
	var xidx = x_select.selectedIndex;
	var y_select = document.getElementById("y_select");
	var yidx = y_select.selectedIndex;

	if(xidx == -1 || yidx == -1)
	{
		return;
	}

	clear_z();
	clear_i();

	var z_select = document.getElementById("z_select");
	var x = x_select.options[xidx].text;
	var y = y_select.options[yidx].text;
	var z_coords = Object.keys(lookupMap[x][y]);

	for(var i = 0; i < z_coords.length; i++)
	{
		var option = document.createElement("option");
		option.text = z_coords[i];
		option.value = z_coords[i];
		z_select.add(option);
	}

	z_selectcb();
}

function z_selectcb () {
	var x_select = document.getElementById("x_select");
	var xidx = x_select.selectedIndex;
	var y_select = document.getElementById("y_select");
	var yidx = y_select.selectedIndex;
	var z_select = document.getElementById("z_select");
	var zidx = z_select.selectedIndex;

	if(xidx == -1 || yidx == -1 || zidx == -1)
	{
		return;
	}

	clear_i();

	var i_select = document.getElementById("i_select");
	var x = x_select.options[xidx].text;
	var y = y_select.options[yidx].text;
	var z = z_select.options[zidx].text;

	var i_coords = lookupMap[x][y][z];

	for(var i = 0; i < i_coords.length; i++)
	{
		var option = document.createElement("option");
		option.text = i_coords[i];
		option.value = i_coords[i];
		i_select.add(option);
	}
	

}