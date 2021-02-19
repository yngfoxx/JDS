let ajaxProcess = [];
let focused_socket;
let focused_gch;

function connectsocket(channel, uid) {
  const jdschannel = io('https://ws-jds-eu.herokuapp.com'+channel, {
  // const jdschannel = io('http://localhost:8000'+channel, {
    auth: { token: 'qPyFMKAdjtfL3Gq5pk2xDgy0SKMpEmLz', uid: uid, gc: channel }
  });

  // USER UNIQUE CHANNEL ID
  const userchannelID = genKey(12);

  jdschannel.on('connect', () => {
    console.log('{SOCKET} => ['+jdschannel.id+'] NOW LISTENING TO '+channel);

    focused_socket = jdschannel;
    console.log("FOCUSED: "+focused_socket);

    // JOIN ROOM
    jdschannel.emit('join', {gc: channel, uid: uid});

    // GET MEMBER ONLINE STATUS ----\/
    jdschannel.emit('msg', { action: 'clients', gc: channel, uid: uid, cid: userchannelID });

    // NOTIFY MEMBERS IN GROUP
    jdschannel.emit('msg', { action: 'user_status', gc: channel, uid: uid });
  });

  jdschannel.on('disconnect', () => {
    console.log("DISCONNECTED FROM CHANNEL: "+channel);
  });

  // USER CUSTOM CHANNEL LISTENER
  jdschannel.on(userchannelID, (data)=> {
    // ALL USERS STATUS IN JOINT GROUP CHANNEL
    if (data.hasOwnProperty('user_status')) {
      let uData = data.user_status;
      let memberDiv = document.querySelectorAll('._bs2dcprc_member');
      memberDiv.forEach((item, i) => { item.children[1].innerHTML = "<font color='grey'>disconnected</font>"; });
      for (var i = 0; i < uData.length; i++) {
        let data_uid = uData[i].gc+'/'+uData[i].uid;
        console.log("["+data_uid+"] user channel data recvd.");
        let userDiv = document.querySelector('._stat[data-uid="'+data_uid+'"]');
        if (userDiv) userDiv.innerHTML = "<font color='#4bc64b'>connected</font>";
      }
    }
  });

  // ----------------------------- [SOCKET MESSAGE HANDLER FOR SOCKET GROUP] -------------------------------- \\
  jdschannel.on('msg', (data) => {
    if (data.hasOwnProperty('file_data')) {
      let nsp = data.namespace;
      let chanID = data.channel_id; // channel_id
      let jointID = data.joint_id; // joint_id
      let reqID = data.request_id; // request_id
      // file_data (v1) # the file is downloading
        // [ETA, bar, downloaded, progress, speed, status]
      // file_data (v2) # the file has been downloaded
        // [MD5, SHA1, SHA256, download_path, download_time_length]
      let fileData = data.file_data;
      let targetDiv = document.querySelector("._jds_info[data-id='"+jointID+"/"+reqID+"']"); // Parent Div
      let targetProgress = (fileData.status != undefined) ? Math.floor(fileData.progress)+"%" : '100%';
      console.log("Something is here");
      if (!targetDiv) return;
      // Download filename -------------------------------------------
      let nameDiv = targetDiv.children[0].children[1].children[0].children[0].children[0];
      // -------------------------------------------------------------

      // Download size -----------------------------------------------
      let sizeDiv = targetDiv.children[0].children[1].children[0].children[1].children[0];
      // -------------------------------------------------------------

      // Download status ---------------------------------------------
      let statusDiv = targetDiv.children[0].children[1].children[0].children[2].children[0]; // status div
          statusDiv.innerText = (fileData.status != undefined) ? fileData.status : 'Completed';
      // -------------------------------------------------------------

      // Download progress -------------------------------------------
      let progressDiv = targetDiv.children[0].children[1].children[0].children[3].children[0];
          progressDiv.innerText = targetProgress;
      // -------------------------------------------------------------

      // Download Button ---------------------------------------------
      let downloadBtn = targetDiv.children[0].children[1].children[1].children[0];
          downloadBtn.children[0].setAttribute('class', 'icon-spin4 animate-spin');
          downloadBtn.setAttribute('title', 'File downloading');
          if (fileData.status === undefined) downloadBtn.children[0].setAttribute('class', 'icon-ok');
          if (fileData.status === undefined) downloadBtn.setAttribute('title', 'File downloaded');
      // -------------------------------------------------------------

      // Download progress Bar ---------------------------------------
      let progressBarDiv = targetDiv.children[0].children[1].children[1].children[2].children[0];
          $(progressBarDiv).css('width', targetProgress);
      // -------------------------------------------------------------
    } else if (data.hasOwnProperty('response')) {
      // OBJ: Process memeber activity data
      switch (data.response) {
        case 'user_status':
        let uData = data.data;
        let memberDiv = document.querySelectorAll('._bs2dcprc_member');
        memberDiv.forEach((item, i) => { item.children[1].innerHTML = "<font color='grey'>disconnected</font>"; });
        for (var i = 0; i < uData.length; i++) {
          let data_uid = uData[i].gc+'/'+uData[i].uid;
          console.log("["+data_uid+"] message channel data recvd.");
          let userDiv = document.querySelector('._stat[data-uid="'+data_uid+'"]');
          if (userDiv) {
            userDiv.innerHTML = "<font color='#4bc64b'>connected</font>";
          } else { // Create new member node
            console.log("New memeber detected!");
            let memberParDiv = document.createElement('DIV');
                memberParDiv.classList.add('_bs2dcprc_member');

                let nameBar = document.createElement('DIV');
                    nameBar.setAttribute('class', '_mem _name');
                    let nameBarIcon = document.createElement('A');
                        nameBarIcon.classList.add('icon-user');
                    let nameBarTxt = document.createElement('A');
                        nameBarTxt.innerText = '['+data_uid+']';
                    nameBar.append(nameBarIcon);
                    nameBar.append(nameBarTxt);
                memberParDiv.append(nameBar);

                let statusIndBar = document.createElement('A');
                    statusIndBar.setAttribute('class', '_mem _stat');
                    statusIndBar.setAttribute('data-uid', data_uid);
                    let statusInd = document.createElement('font');
                        statusInd.setAttribute('color', '#4bc64b');
                        statusInd.innerText = 'connected';
                    statusIndBar.append(statusInd);
                memberParDiv.append(statusIndBar);
            // Attach new user node to DOM
            document.querySelector('._bs2dcpr_container').append(memberParDiv);
          }
        }
        break;

        default:
        break;
      }
    } else if (data.hasOwnProperty('disconnected_user')) {
      let uid = data.disconnected_user.uid;
      let uGrp = data.disconnected_user.gc;

      let data_uid = uGrp+'/'+uid;
      let userDiv = document.querySelector('._stat[data-uid="'+data_uid+'"]');
      if (userDiv) userDiv.innerHTML = "<font color='grey'>disconnected</font>";
      console.log("user disconnected: "+uGrp+"/"+uid);
    }
  });
  // --------------------------------------------------------------------------------------------------------- \\

  jdschannel.on("connect_error", err => {
    if (err instanceof Error) {
      console.log(channel);
      console.error(err.message); // not authorized
      console.log(err.data); // { content: "Please retry later" }
    }
  });
}

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
function loadJDS(jdsArray) {
  // Load jds group, memeber list and download list
  if (!jdsArray.hasOwnProperty('jID')) return;
  console.log(jdsArray);
  ajx({
    type: 'POST',
    url: '/JDS/req/req_handler.php',
    data: {jdsCheck: jdsArray.jID},
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

            if (focused_socket) {
              // HANDLE CLIENT SOCKET DISCONNECTION
              focused_socket.emit('msg', { action: 'disconnect', gc: focused_gch, uid: jRes.UID });
              focused_socket.disconnect();
            }
            focused_gch = "/py_"+GROUP_CHANNEL;
            connectsocket(focused_gch, jRes.UID);

            // generate member element
            let member = jRes.member;
            $('._bs2dcprc_member').remove();
            for (var i = 0; i < member.length; i++) {
              let parDiv = document.createElement('DIV');
                  parDiv.classList.add('_bs2dcprc_member');
                  let childDiv = document.createElement('DIV');
                      childDiv.setAttribute('class', '_mem _name');
                      let childDivIcon = document.createElement('A');
                          childDivIcon.setAttribute('class', 'icon-user');
                          if (member[i].role == 'owner') childDivIcon.setAttribute('class', 'icon-crown');
                      let childDivLabel = document.createElement('A');
                          childDivLabel.append(document.createTextNode(member[i].username));
                      childDiv.append(childDivIcon);
                      childDiv.append(childDivLabel);
                  parDiv.append(childDiv);
                  let childDiv2 = document.createElement('A');
                      childDiv2.setAttribute('class', '_mem _stat');
                      childDiv2.setAttribute('data-uid', "/py_"+GROUP_CHANNEL+"/"+member[i].uid);
                      childDiv2.innerText = '---';
                  parDiv.append(childDiv2);
              document.querySelector('._bs2dcpr_container').append(parDiv);
            }
            // ---------------------------------------------------------------->

            document.querySelector('._bs2_div_contr ').classList.remove('hide');
            document.querySelector('.float_center_msg ').classList.add('hide');
            document.querySelector('._jds_holder').innerText = jdsArray.jID;
            document.querySelector('._bdysec1').classList.add('_pcntd');
            // close menu if open
            let menu = $("._tnvMnu");
            if (menu.attr('data-state') == 'on') {
              $("._tnvMnu").attr('data-state', 'off'); // close menu if open
              menu.fadeOut();
            }


            // generate download list
            // console.log(jRes.download);
            let download = jRes.download;
            $('div[class="_bs2dcp_row _jds_info"]').remove();
            for (var j = 0; j < download.length; j++) {
              let FILE_URL = download[j].url;
              let FILE_NAME = getFilename(FILE_URL).filename;
              let FILE_EXT = download[j].ext;
              let FILE_SIZE = download[j].size;
              let FILE_CHUNK_SIZE = download[j].chunk_size;
              let FILE_STATUS = (download[j].status == 0) ? 'Waiting' : ((download[j].status == 1) ? ((download[j].progress === undefined) ? 'Failed':'Downloading') : 'Finished');
              let FILE_PROGRESS = (download[j].status == 0) ? '0' : ((download[j].status == 1) ? download[j].progress : '100');
                  FILE_PROGRESS = (FILE_PROGRESS === undefined) ? 'Error' : FILE_PROGRESS;
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
                                        subRow_1_2_1_0_1.innerText = FILE_SIZE;
                                        subRow_1_2_1_0_3.innerText = "Size"; // name of field
                                        break;

                                      case 2: // STATUS
                                        subRow_1_2_1_0_1.innerText = FILE_STATUS;
                                        subRow_1_2_1_0_3.innerText = "Status"; // name of field
                                        break;

                                      case 3: // FILE DOWNLOAD PROGRESS [SERVER SIDE]
                                        subRow_1_2_1_0_1.innerText = (FILE_PROGRESS === 'Error') ? FILE_PROGRESS : FILE_PROGRESS+"%";;
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
                                if (FILE_STATUS == 'Failed' && (div1 == 1 || div1 == 3)) continue; // skip chunkify button and chunk config button
                                let subRow_1_2_2_0 = document.createElement('DIV');
                                    subRow_1_2_2_0.setAttribute('class', '_dwnld_btn'); // child_loop

                                switch (div1) {
                                  case 0:
                                    // DOWNLOAD BUTTON/LOADING INDICATOR
                                    let subRow_1_2_2_0_1 = document.createElement('A');
                                      if (FILE_STATUS == 'Waiting') {
                                        subRow_1_2_2_0_1.setAttribute('class', 'icon-play _start');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_1); // sub row 1 2 2 (1<->4) 1
                                        subRow_1_2_2_0.setAttribute('title', 'Start download');
                                        subRow_1_2_2_0.addEventListener('click', function() {
                                          // initialize download
                                          if (subRow_1_2_2_0.getAttribute('data-status') == "1") return; // the download button was already clicked
                                          ajx({
                                            type: 'POST',
                                            url: '/JDS/req/req_handler.php',
                                            data: {jdsInit: true, rid: FILE_RID, jid: FILE_JID},
                                            success: function(res) {
                                              if (isJson(res)) {
                                                let jRes = JSON.parse(res);
                                                if (jRes.started) {
                                                  // Download started
                                                  swal({icon: 'success', title: 'SUCCESS', text: 'Download started'});
                                                  subRow_1_2_2_0.setAttribute('data-status', '1');
                                                } else {
                                                  // Download failed to start
                                                  if (jRes.hasOwnProperty('server_error')) {
                                                    swal({icon: 'error', title: 'ERROR', text: 'Download could not start'});
                                                  } else {
                                                    swal({icon: 'warning', title: 'ERROR', text: 'Download failed to start, try again later...'});
                                                  }
                                                }
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
                                        subRow_1_2_2_0.setAttribute('title', 'File downloading');
                                        subRow_1_2_2_0.setAttribute('data-status', '1');
                                      } else if (FILE_STATUS == 'Finished') {
                                        subRow_1_2_2_0_1.setAttribute('class', 'icon-ok _ok');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_1); // sub row 1 2 2 (1<->4) 1
                                        subRow_1_2_2_0.setAttribute('title', 'File downloaded');
                                        subRow_1_2_2_0.setAttribute('data-status', '1');
                                      } else if (FILE_STATUS == 'Failed') {
                                        subRow_1_2_2_0_1.setAttribute('class', 'icon-trash');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_1); // sub row 1 2 2 (1<->4) 1
                                        subRow_1_2_2_0.setAttribute('title', 'Delete from list');
                                        subRow_1_2_2_0.setAttribute('data-status', '1');
                                        // TODO: Delete download from list
                                        subRow_1_2_2_0.addEventListener('click', function() {
                                          swal({
                                            dangerMode: true,
                                            icon: 'warning',
                                            title: 'Delete download',
                                            text: 'This download will be deleted permanently, proceed?',
                                            buttons: ['Cancel', 'Delete']
                                          }).then((result) => {
                                            if (result == true) swal("A delete request has been sent, the file will be deleted permanently.");
                                          });
                                        });
                                      }
                                    break;

                                  case 1:
                                    let subRow_1_2_2_0_4 = document.createElement('A');
                                        subRow_1_2_2_0_4.setAttribute('class', 'icon-resize-small-alt');
                                        subRow_1_2_2_0.setAttribute('title', 'Chunkify');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_4); // sub row 1 2 2 (1<->4) 4
                                    break;

                                  case 2:
                                    let subRow_1_2_2_0_3 = document.createElement('div');
                                        subRow_1_2_2_0.setAttribute('class', '_dwnld_bar'); // child_loop
                                        subRow_1_2_2_0_3.setAttribute('class', '_dwnld_bar_inner');
                                        if (FILE_STATUS != 'Failed') {
                                          subRow_1_2_2_0_3.style.width = FILE_PROGRESS+"%";
                                        } else {
                                          subRow_1_2_2_0_3.style.width = "100%";
                                          subRow_1_2_2_0_3.style.backgroundColor = "#d92323";
                                        }
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_3); // sub row 1 2 2 (1<->4) 3
                                    break;

                                  case 3:
                                    let subRow_1_2_2_0_2 = document.createElement('A');
                                        subRow_1_2_2_0_2.setAttribute('class', 'icon-cog _conf');
                                        subRow_1_2_2_0.append(subRow_1_2_2_0_2); // sub row 1 2 2 (1<->4) 2
                                        subRow_1_2_2_0.setAttribute('title', 'Chunk config');
                                        subRow_1_2_2_0.setAttribute('data-rid', FILE_RID);
                                        subRow_1_2_2_0.addEventListener('click', function(e) {
                                          let rID = e.currentTarget.getAttribute('data-rid');
                                          ajx({
                                            type: 'POST',
                                            url: '/JDS/req/req_handler.php',
                                            data: {jdsCheck: jdsArray.jID},
                                            success: function (res) {
                                              if (res != 0 && isJson(res)) {
                                                let jRes = JSON.parse(res);
                                                // extension, url, size, status, source
                                                if (jRes.hasOwnProperty('server_error')) {
                                                  swal({icon: "warning", title: "Oh no!", text: jRes.server_error});
                                                  return;
                                                } else {
                                                  // Generate group details and socket activity --------------------->
                                                  let nDownloadData = jRes.download;
                                                  for (var i = 0; i < nDownloadData.length; i++) if (nDownloadData[i].rid == rID) openChunkConfig(rID, nDownloadData[i].chunk_size);
                                                  // ---------------------------------------------------------------->
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
                                        });
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
