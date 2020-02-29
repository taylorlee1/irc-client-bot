
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
    if (!text.match(/^\d/)) {
      return linkText;
    }

    var link = document.createElement("A");
    link.appendChild(linkText);
    link.title = text;
    var tokens = text.split(/\s+/);
    console.log(tokens);
    var filename = encodeURIComponent(tokens[1]);
    link.href = "/api/get-file?filename=" + filename;
    return link;
  }

  var update_page = function(what){
    console.log(what);
    var maindiv = document.getElementById('maindiv');

    var ul = document.createElement("UL");
    
    what.forEach(function (item, index) {
      var il = document.createElement("LI");
      il.appendChild(urlify(item));
      ul.appendChild(il);
    });

    maindiv.appendChild(ul);
  };

  get_listing(update_page);

})();

