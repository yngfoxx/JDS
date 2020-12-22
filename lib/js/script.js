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
