let ajaxProcess = [];

// AJAX METHOD ---------------------------------------------------------------->
function ajx(obj) {
  // type, url, data, success, complete, err, load, loaderID, area
  if (!obj.hasOwnProperty('type')) return "No request type!";
  let type = obj.type;

  if (!obj.hasOwnProperty('url')) return "No request url!";
  const url = obj.url;

  if (!obj.hasOwnProperty('data')) return "No request parameter given!";
  let data = obj.data;

  if (!obj.hasOwnProperty('success')) return "No request parameter given!";
  let success = obj.success;

  let complete = (obj.complete || undefined);
  let err = (obj.errorMessage || undefined);

  let errMethod = (obj.errorMethod || undefined);

  let timeOut = (!obj.hasOwnProperty('timeOut')) ? ()=>{swal({ icon: "error", title: "Server timedout", text: "There seems to be a problem with the internet connection." });} : obj.timeOut;

  let timer = (obj.timer || 10000);

  if (!obj.hasOwnProperty('load')) return "No load option";
  let load = obj.load;


  let loaderID = (!obj.hasOwnProperty('loaderID')) ? crtEvnt() : obj.loaderID;

  let area = (!obj.hasOwnProperty('area')) ? "width" : obj.area;

  ajaxProcess[JSON.stringify(loaderID)] = $.ajax({
    xhr: function()
    {
      let xhr = new window.XMLHttpRequest();
      switch (load) {
        case 'up':
          //Upload progress
          xhr.upload.addEventListener("progress", function(evt){
            if (evt.lengthComputable) {
              let percentComplete = evt.loaded / evt.total;
              //Do something with upload progress
              let percentFinish = ((evt.loaded / evt.total) * 100);
              // console.log("UPLOADING => "+percentComplete);
              if (area == "height") {
                $("#"+loaderID).css('height', percentFinish + '%');
              } else if (area == "width") {
                $("#"+loaderID).css('width', percentFinish + '%');
              }
            }
          }, false);
          break;

        case 'down':
          //Download progress
          xhr.addEventListener("progress", function(evt){
            if (evt.lengthComputable) {
              let percentComplete = evt.loaded / evt.total;
              //Do something with download progress
              let percentFinish = ((evt.loaded / evt.total) * 100);
              // console.log("DOWNLOADING => "+percentComplete);
              if (area == "height") {
                $("#"+loaderID).css('height', percentFinish + '%');
              } else if (area == "width") {
                $("#"+loaderID).css('width', percentFinish + '%');
              }
            }
          }, false);
          break;
        default:

      }
      return xhr;
    },
    type: type,
    url: url,
    data: data,
    success: function(result) {
      if (isJson(result)) {
        let res = JSON.parse(result);
        if (res.session_id == "") {
          swal({icon: "error",title: "error",text: "Session expired, please log in again"});
          return false;
        }
      }
      success(result);
    },
    complete: function() {
      if (complete != undefined) complete();
      dstryEvent(loaderID);
      // console.log(ajaxProcess[loaderID]);
    },
    error: function(requestObject, error, errorThrown) {
      console.error("AJX ERROR: "+error);
      console.error("AJX ERROR THROWN: "+errorThrown);
      if (err != undefined) {
        swal({icon: "error",title: "Unexpected error",text: "AJX+SERVER: "+err});
      } else {
        console.error(requestObject);
      }
      if (errMethod != undefined) errMethod();
      if (timeOut != undefined && error == 'timeout') timeOut();
    },
    timeout: timer // 10 seconds timeOut
  });
}
// ---------------------------------------------------------------------------->



// LOAD JDS VIEW -------------------------------------------------------------->
function loadJDS(jdsID) {
  // Load jds group, memeber list and download list
  ajx({
    type: 'POST',
    url: 'http://localhost/JDS/req/req_handler.php',
    data: {jdsCheck: jdsID},
    success: function (res) {
      if (res != 0) {
        if (isJson(res)) {
          // extension, url, size, status, source
          let jRes = JSON.parse(res);
          if (jRes.hasOwnProperty('server_error')) {
            swal({icon: "warning", title: "Oh no!", text: jRes.server_error});
            return;
          } else {
            // Generate group details and socket activity --------------------->
            let info = jRes.info;
            // start listening to the py_channel of this joint group
            let GROUP_CHANNEL = info.channel;
            let GROUP_CAPACITY = info.capacity;
            let GROUP_OWNER = info.uid;
            let GROUP_CREATION_DATE = info.creationDate;

            const jdsChannel = io('ws://localhost:8000/py_'+GROUP_CHANNEL, {
            // io('ws://ws-jds-eu.herokuapp.com/'+GROUP_CHANNEL, {
              query: { auth: 'qPyFMKAdjtfL3Gq5pk2xDgy0SKMpEmLz' },
              reconnectionDelayMax: 10000,
              // forceNew: true
            });

            jdsChannel.on('connect', () => {
              console.log('{SOCKET} => ['+jdsChannel.id+'] NOW LISTENING TO '+GROUP_CHANNEL);
              // TODO: update socket id in database
            });

            jdsChannel.on('msg', (data) => {
              // TODO: Process incoming messages
              // This socket is only for download sockets, to recieve download progress
              // from the grab.py api through Python Flask and Node.js
              let nsp = data.namespace;
              // channel_id
              let chanID = data.channel_id;
              // joint_id
              let jointID = data.joint_id;
              // request_id
              let reqID = data.request_id;
                // file_data (v1) # the file is downloading
                  // ETA
                  // bar
                  // downloaded
                  // progress
                  // speed
                  // status
                // file_data (v2) # the file has been downloaded
                  // MD5
                  // SHA1
                  // SHA256
                  // download_path
                  // download_time_length
              let fileData = data.file_data;

              let targetDiv = document.querySelector("._jds_info[data-id='"+jointID+"/"+reqID+"']"); // Parent Div
              let targetProgress = (fileData.status != undefined) ? Math.floor(fileData.progress)+"%" : '100%';
              // Download filename -------------------------------------------->
              let nameDiv = targetDiv.children[0].children[1].children[0].children[0].children[0];
              // -------------------------------------------------------------->

              // Download size ------------------------------------------------>
              let sizeDiv = targetDiv.children[0].children[1].children[0].children[1].children[0];
              // -------------------------------------------------------------->

              // Download status ---------------------------------------------->
              let statusDiv = targetDiv.children[0].children[1].children[0].children[2].children[0]; // status div
                  statusDiv.innerText = (fileData.status != undefined) ? fileData.status : 'Completed';
              // -------------------------------------------------------------->

              // Download progress -------------------------------------------->
              let progressDiv = targetDiv.children[0].children[1].children[0].children[3].children[0];
                  progressDiv.innerText = targetProgress;
              // -------------------------------------------------------------->

              // Download progress Bar ---------------------------------------->
              let progressBarDiv = targetDiv.children[0].children[1].children[1].children[2].children[0];
                  $(progressBarDiv).css('width', targetProgress);
              // -------------------------------------------------------------->
            });

            jdsChannel.on("connect_error", err => {
              if (err instanceof Error) {
                console.error(err.message); // not authorized
                console.log(err.data); // { content: "Please retry later" }
              }
            });
            // ---------------------------------------------------------------->

            document.querySelector('._bs2_div_contr ').classList.remove('hide');
            document.querySelector('.float_center_msg ').classList.add('hide');
            document.querySelector('._jds_holder').innerText = jdsID;
            document.querySelector('._bdysec1').classList.add('_pcntd');
            // close menu if open
            let menu = $("._tnvMnu");
            if (menu.attr('data-state') == 'on') {
              $("._tnvMnu").attr('data-state', 'off'); // close menu if open
              menu.fadeOut();
            }
            // generate member element
            let member = jRes.member;
            $('._bs2dcprc_member').remove();
            for (var i = 0; i < member.length; i++) {
              let parDiv = document.createElement('DIV');
                  parDiv.classList.add('_bs2dcprc_member');
                  let childDiv = document.createElement('A');
                      childDiv.setAttribute('class', '_mem _name');
                      childDiv.innerText = member[i].username;
                  parDiv.append(childDiv);
                  let childDiv2 = document.createElement('A');
                      childDiv2.setAttribute('class', '_mem _stat');
                      childDiv2.setAttribute('data-uid', member[i].uid);
                      childDiv2.innerText = '---';
                  parDiv.append(childDiv2);
              document.querySelector('._bs2dcpr_container').append(parDiv);
            }

            // generate download list
            console.log(jRes.download);
            let download = jRes.download;
            $('div[class="_bs2dcp_row _jds_info"]').remove();
            for (var j = 0; j < download.length; j++) {
              let FILE_URL = download[j].url;
              let FILE_NAME = getFilename(FILE_URL).filename;
              let FILE_EXT = download[j].ext;
              let FILE_STATUS = (download[j].status == 0) ? 'Waiting' : ((download[j].status == 1) ? 'Downloading' : 'Finished');
              let FILE_RID = download[j].rid;
              let FILE_JID = download[j].jid;
              let FILE_RQ_UID = download[j].uid;

              let mainRow = document.createElement('DIV');
                  mainRow.setAttribute('class', '_bs2dcp_row _jds_info'); // main row
                  mainRow.setAttribute('data-id', FILE_JID+'/'+FILE_RID); // main row

                  let subRow_1 = document.createElement('DIV');
                      subRow_1.setAttribute('class', '_jdsi_row _info'); // sub row 1
                      // --------------------------------------------------------------->
                      let subRow_1_1 = document.createElement('DIV');
                          subRow_1_1.setAttribute('class', '_jdsiri_row _rext'); // sub row 1 1
                          let subRow_1_1_1 = document.createElement('DIV');
                              subRow_1_1_1.setAttribute('class', '_jdsiri_ext');  // sub row 1 1 1
                              let subRow_1_1_1_1 = document.createElement('A');
                                  subRow_1_1_1_1.setAttribute('class', '_ext');  // sub row 1 1 1 1
                                  subRow_1_1_1_1.innerText = FILE_EXT; // file extension
                              subRow_1_1_1.append(subRow_1_1_1_1);
                          subRow_1_1.append(subRow_1_1_1);
                      subRow_1.append(subRow_1_1);
                      // --------------------------------------------------------------->

                      // --------------------------------------------------------------->
                      let subRow_1_2 = document.createElement('DIV');
                          subRow_1_2.setAttribute('class', '_jdsiri_row'); // sub row 1 2
                          let subRow_1_2_1 = document.createElement('DIV');
                              subRow_1_2_1.setAttribute('class', '_jdsirir_row'); // sub row 1 2 1
                              for (var div = 0; div < 4; div++) {  // sub row 1 2 1 ->  sub row 1 2 1 (1<->4) 3
                                let subRow_1_2_1_0 = document.createElement('DIV');
                                    subRow_1_2_1_0.setAttribute('class', '_jdsirir_itm'); // child_loop
                                    let subRow_1_2_1_0_1 = document.createElement('A');
                                        subRow_1_2_1_0_1.setAttribute('class', '_jdsirir_itm_val');

                                    let subRow_1_2_1_0_2 = document.createElement('HR');

                                    let subRow_1_2_1_0_3 = document.createElement('A');
                                        subRow_1_2_1_0_3.setAttribute('class', '_jdsirir_itm_label');

                                    switch (div) {
                                      case 0: // File
                                        subRow_1_2_1_0_1.innerText = FILE_NAME+'.'+FILE_EXT;
                                        subRow_1_2_1_0_1.setAttribute('title', FILE_URL);
                                        subRow_1_2_1_0_3.innerText = "File"; // name of field
                                        break;

                                      case 1: // SIZE
                                        subRow_1_2_1_0_1.innerText = "---";
                                        subRow_1_2_1_0_3.innerText = "Approx. size"; // name of field
                                        break;

                                      case 2: // STATUS
                                        subRow_1_2_1_0_1.innerText = FILE_STATUS;
                                        subRow_1_2_1_0_3.innerText = "Status"; // name of field
                                        break;

                                      case 3: // SOURCE IP
                                        subRow_1_2_1_0_1.innerText = "-.-.-.-";
                                        // subRow_1_2_1_0_3.innerText = "Source IP"; // name of field
                                        subRow_1_2_1_0_3.innerText = "Progress"; // name of field
                                        break;

                                      default:
                                        break;
                                    }
                                    subRow_1_2_1_0.append(subRow_1_2_1_0_1); // sub row 1 2 1 (1<->4) 1
                                    subRow_1_2_1_0.append(subRow_1_2_1_0_2); // sub row 1 2 1 (1<->4) 2
                                    subRow_1_2_1_0.append(subRow_1_2_1_0_3); // sub row 1 2 1 (1<->4) 3
                                    subRow_1_2_1.append(subRow_1_2_1_0); // Attach column to row
                              }
                          let subRow_1_2_2 = document.createElement('DIV');
                              subRow_1_2_2.setAttribute('class', '_jdsirir_row'); // sub row 1 2 2
                              for (var div1 = 0; div1 < 4; div1++) {  // sub row 1 2 2 ->  sub row 1 2 2 (1<->4) 3
                                let subRow_1_2_2_0 = document.createElement('DIV');
                                    subRow_1_2_2_0.setAttribute('class', '_dwnld_btn'); // child_loop

                                switch (div1) {
                                  case 0:
                                    let subRow_1_2_2_0_1 = document.createElement('A');
                                      if (FILE_STATUS == 'Waiting') {
                                        subRow_1_2_2_0_1.setAttribute('class', 'icon-play _start');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_1); // sub row 1 2 2 (1<->4) 1
                                        subRow_1_2_2_0.addEventListener('click', function() {
                                          // initialize download
                                          ajx({
                                            type: 'POST',
                                            url: 'http://localhost/JDS/req/req_handler.php',
                                            data: {jdsInit: true, rid: FILE_RID, jid: FILE_JID},
                                            success: function(res) {
                                              console.log(res);
                                              if (res != 0) {
                                                if (isJson(res)) {
                                                  let jres = JSON.parse(res);
                                                  if (jres.hasOwnProperty('server_error')) {
                                                    swal({icon: 'error', title: jres.code, text: jres.server_error});
                                                    return false;
                                                  }
                                                  swal({icon: 'success', title: 'Nice!', text: JSON.stringify(jres)});
                                                } else {
                                                  swal(res);
                                                }
                                              } else {
                                                console.error(res);
                                              }
                                            },
                                            errorMethod: function() {
                                              swal({icon: 'error', title: '500 Internal server error', text: 'Server returned error'});
                                            },
                                            load: 'up'
                                          });
                                        });
                                      } else if (FILE_STATUS == 'Downloading') {
                                        subRow_1_2_2_0_1.setAttribute('class', 'icon-spin4 animate-spin');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_1); // sub row 1 2 2 (1<->4) 1
                                      } else if (FILE_STATUS == 'Finished') {
                                        subRow_1_2_2_0_1.setAttribute('class', 'icon-ok _ok');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_1); // sub row 1 2 2 (1<->4) 1
                                      }
                                    break;

                                  case 1:
                                    let subRow_1_2_2_0_2 = document.createElement('A');
                                        subRow_1_2_2_0_2.setAttribute('class', 'icon-cog _conf');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_2); // sub row 1 2 2 (1<->4) 2
                                    break;

                                  case 2:
                                    let subRow_1_2_2_0_3 = document.createElement('div');
                                        subRow_1_2_2_0.setAttribute('class', '_dwnld_bar'); // child_loop
                                        subRow_1_2_2_0_3.setAttribute('class', '_dwnld_bar_inner');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_3); // sub row 1 2 2 (1<->4) 3
                                    break;

                                  case 3:
                                    let subRow_1_2_2_0_4 = document.createElement('A');
                                        subRow_1_2_2_0_4.setAttribute('class', 'icon-trash _del');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_4); // sub row 1 2 2 (1<->4) 4
                                    break;
                                  default:
                                    break;
                                }
                                subRow_1_2_2.append(subRow_1_2_2_0); // Attach column to row
                              }
                          subRow_1_2.append(subRow_1_2_1);
                          subRow_1_2.append(subRow_1_2_2);
                      subRow_1.append(subRow_1_2);
                      mainRow.append(subRow_1);
                      // --------------------------------------------------------------->


                      let subRow_2 = document.createElement('DIV');
                          subRow_2.setAttribute('class', '_jdsi_row _options'); // child
                      // --------------------------------------------------------------->
                      mainRow.append(subRow_2);
                      // --------------------------------------------------------------->

                // ATTACH DOWNLOAD LIST ITEM TO VIEW
                document.querySelector('div[class="_bs2dc_pane _pane_r"]').append(mainRow);
            }
          }
        }
      }
    },
    errorMethod: function() {
      swal({
        icon: 'error',
        title: 'Whoops',
        text: 'Something went wrong, might be your internet connection.'
      });
    },
    load: 'up'
  });
}
