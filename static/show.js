function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
    }
    return "";
}

function users_opts()
{
  var fanin = getCookie("fanin");
  var fanout = getCookie("fanout");

  var fanin_cbox = document.getElementById("fanin_cbox");
  var fanout_cbox = document.getElementById("fanout_cbox");

  if(fanin_cbox && fanin == "off")
  {
    fanin_cbox.checked = false;
  }
  else if(fanin_cbox)
  {
    fanin_cbox.checked = true;
  }
  if(fanout_cbox && fanout == "off")
  {
    fanout_cbox.checked = false;
  }
  else if(fanout_cbox)
  {
    fanout_cbox.checked = true;
  }

  if(fanin_cbox)
  {
    fanin_check(fanin_cbox);
  }

  if(fanout_cbox)
  {
    fanout_check(fanout_cbox);
  }
}


function fanin_check(cb)
{
  var obj = document.getElementById("fanin_table");
  if(cb.checked)
  {
    obj.style.visibility = "visible";
    obj.style.height = "";
    setCookie("fanin", "on", 1);
  }
  else
  {
    obj.style.visibility = "collapse";
    obj.style.height = "0px";
    setCookie("fanin", "off", 1);
  }
}

function fanout_check(cb)
{
  var obj = document.getElementById("fanout_table");
  if(cb.checked)
  {
    obj.style.visibility = "visible";
    obj.style.height = "";
    setCookie("fanout", "on", 1);
  }
  else
  {
    obj.style.visibility = "collapse";
    obj.style.height = "0px";
    setCookie("fanout", "off", 1);
  }
}
