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
    Open chunk config menu
---------------------------------------------------------------*/
function openChunkConfig(file_rid, file_chunk_size) {
  $('._bibf_div_c_cont').fadeIn();
  let downConfig = document.querySelector('._bibf_dc_div');
      downConfig.setAttribute("data-svr-id", file_rid);

  let sections = document.getElementsByClassName('_bibfdcd_section');
  let dropdown = document.querySelector('._bibfdcds_select');
  let specifiedInput = document.querySelector('.chunkInput[name="chunk_max_size"]');

  let checkBoxInput = document.querySelector('input[name="auto_config"]');
      checkBoxInput.checked = false;

  let droplist = [5, 10, 50, 100, 200];

  if (file_chunk_size != 'auto'){ // Value is in dropdown
    checkBoxInput.checked = true;
    if (!droplist.includes(file_chunk_size)) { // Value is specified
      dropdown.value = 's';
      specifiedInput.style.display = 'block';
      dropdown.removeAttribute('disabled');
      // console.log("val is not in drop");
    } else {
      dropdown.value = file_chunk_size;
      dropdown.setAttribute('disabled', 'true');
      // console.log("val is in drop");
    }
  }
  // else {
  //   console.log("val is auto");
  // }
    specifiedInput.value = file_chunk_size;
}
