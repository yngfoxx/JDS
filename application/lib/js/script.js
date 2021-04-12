/* ------------------------------------------------------------
    Set element as active element (like tabs in a web browser)
---------------------------------------------------------------*/
function setActiveElement(e, activeClass, className) {
    document.querySelectorAll("."+className).forEach((element, i) => {
      if (element !== e) element.classList.remove(activeClass);
      if (!e.classList.contains(activeClass)) e.classList.add(activeClass);
    });
}


/* -----------------------------------------------------
    Generate random string with given length
--------------------------------------------------------*/
function genKey(length) {
   var result           = '';
   var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   var charactersLength = characters.length;
   for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}


/*-------------------------------------------------------------
    AJAX event loader bar creator
---------------------------------------------------------------*/
function crtEvnt() {
  let evtID = genKey(6);
  let evtElement = document.createElement('DIV');
      evtElement.classList.add('_prc_evt');
      evtElement.setAttribute('id', evtID);
  document.querySelector('._prc_container').append(evtElement);
  return evtID;
}


/*-------------------------------------------------------------
    AJAX event loader bar destroyer
---------------------------------------------------------------*/
function dstryEvent(evtID) {
  let evtElement = document.getElementById(evtID);
  $(evtElement).hide();
  $(evtElement).remove();
}


/*-------------------------------------------------------------
    Json detector (check if string is a JSON object)
---------------------------------------------------------------*/
function isJson(str) {
  try {
    JSON.parse(str);
  } catch (e) {
    return false;
  }
  return true;
}


/*-------------------------------------------------------------
    Convert form data to JSON
---------------------------------------------------------------*/
function srlToJson(form) {
  let data = form.serialize().split("&");
  let obj={};
  for (var key in data) {obj[data[key].split("=")[0]] = data[key].split("=")[1];}
  obj.dtz = new Date();
  return obj;
}


/*-------------------------------------------------------------
    Get Filename and extension from URL
---------------------------------------------------------------*/
function getFilename(url){
  // get the part after last /, then replace any query and hash part
  url = url.split('/').pop().replace(/\#(.*?)$/, '').replace(/\?(.*?)$/, '');
  url = url.split('.');  // separates filename and extension
  return {filename: (url[0] || ''), ext: (url[1] || '')}
}


/*-------------------------------------------------------------
    Generate random integer
---------------------------------------------------------------*/
function rand(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}


/*-------------------------------------------------------------
    DOM manipulation functions
---------------------------------------------------------------*/
function clearDOM(element) {
  while (element.firstChild) { element.removeChild(element.lastChild); }
}

function replaceInnerDOM(element, newDOM) {
  while (element.firstChild) { element.removeChild(element.lastChild); }
  element.innerHTML = newDOM;
}



/*-------------------------------------------------------------
    Get key of object by value
---------------------------------------------------------------*/
function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] === value);
}


/*-------------------------------------------------------------
    Get cookie by name
---------------------------------------------------------------*/
function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}



/*-------------------------------------------------------------
    Revelation effect (dycryption effect)
---------------------------------------------------------------*/
function startdecrypt(decrypted, encrypted) {
    // Original text, split into an array and reversed (for faster pop())
    var originalText = decrypted.textContent.split('').reverse();
    var decryptedText = "";
    var i = 0;

    decrypted.textContent = "";

    var shuffleInterval = setInterval(function(){
      // Generate random strings. You can modify the generator function range
      // (Math.random()*(to-from+1)+from);
      var shuffledText = '';
      var j = originalText.length;
      while(j--) shuffledText += String.fromCharCode((Math.random()*94+33) | 0);

      // On every 10 cycles, remove a character from the original text to the decoded text
      if(i++ % 10 === 0) decryptedText += originalText.pop();

      // Display
      decrypted.textContent = decryptedText;
      encrypted.textContent = shuffledText;

      // Stop when done
      if(!shuffledText.length) clearInterval(shuffleInterval);

    // 50ms looks more dramatic
    },50);
}
