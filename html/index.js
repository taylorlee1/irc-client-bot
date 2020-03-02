
(function(){

  // by not declaring var this variable is going to be at global namespace


  var calendarHeaderMonth = function(opts){
  };

  var calendarHeaderWeek = function(opts){
  };

  var calendarData = function(opts){
  };

  var drawCalendar = function(opts,d){
  };

  var getCellID = function(year,month,day){
  };

  var get_listing = function(callback) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
         // Action to be performed when the document is read;
        callback(JSON.parse(this.responseText));
      }
    };
    xhttp.open("GET", "/api/get-listing", true);
    xhttp.send();

  }

  var urlify = function(text) {
    var linkText = document.createTextNode(text);

    var link = document.createElement("A");
    link.appendChild(linkText);
    link.title = text;
    var filename = encodeURIComponent(text);
    link.href = "/api/get-file?filename=" + filename;
    return link;
  }

  var update_page = function(what){
    console.log(what);
    var maindiv = document.getElementById('maindiv');

    var table = document.createElement("table");
    
    what.forEach(function (item, index) {

      if (item.startsWith("#")) {
       	return; 
      }

      var row = document.createElement("tr");
      var tokens = item.split(/\s+/);
      for (var i=0; i < 6; i++) {
	if (typeof tokens[i] == 'undefined') {
	  tokens[i] = '';
	}

        var td = document.createElement("td");
        if ( i == 1 ) {
          td.appendChild(urlify(tokens[i]));
        } else {
	  td.appendChild(document.createTextNode(tokens[i]));
	}
        row.appendChild(td);
      }
      table.appendChild(row);
    });

    maindiv.appendChild(table);
  };

  get_listing(update_page);

})();

