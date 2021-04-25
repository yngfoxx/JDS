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
    Get key of object by value
---------------------------------------------------------------*/
function getKeyByValue(object, value) {
  return Object.keys(object).find(key => object[key] === value);
}




/*-------------------------------------------------------------
 * Format bytes as human-readable text.
 *
 * @param bytes Number of bytes.
 * @param si True to use metric (SI) units, aka powers of 1000. False to use
 *           binary (IEC), aka powers of 1024.
 * @param dp Number of decimal places to display.
 *
 * @return Formatted string.
 Credit: https://stackoverflow.com/users/65387/mpen
---------------------------------------------------------------*/
function humanFileSize(bytes, si=false, dp=1) {
  const thresh = si ? 1000 : 1024;

  if (Math.abs(bytes) < thresh) {
    return bytes + ' B';
  }

  const units = si
    ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
  let u = -1;
  const r = 10**dp;

  do {
    bytes /= thresh;
    ++u;
  } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);


  return bytes.toFixed(dp) + ' ' + units[u];
}
