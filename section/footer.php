<script type="text/javascript" src="/JDS/lib/js/ajx.js<?php echo "?v=".rand(100000000, 999999999);  ?>"></script>
<?php
// USER HOME PAGE ------------------------------------------------------------->
 if (isset($_GET['home'])) { // HOME PAGE ?>
  <script type="text/javascript">
  const socket_unique_id = genKey(6);
  function ws_client_connect() {
    // Connect to client application ------------------------------------------->
    var ws_client_app = new WebSocket("ws://127.0.0.1:5678/");
      ws_client_app.onopen = function () {
        ajx({
          type: 'POST',
          url: '/JDS/req/req_handler.php',
          data: {uData: true},
          success: (res) => {
            if (isJson(res)) {
              let uData = JSON.parse(res);
              ws_client_app.send(JSON.stringify({
                  "action": "jds_client_connected",
                  "interval": "none",
                  "socketID": socket_unique_id,
                  "socketType": "web",
                  "payload": {
                    "devID": uData.dID,
                    "userID": uData.uID,
                    "username": uData.uName,
                    "joints": uData.jds
                  }
                }));
            }
          },
          complete: () => {
            console.log("Done!!!!");
          },
          load: 'up'
        });
      }

      ws_client_app.onerror = function () {
        // alert("Failed to connect to client application");
      }
      // ws_client_app.onclose = function () { alert("Connection closed!"); }
      ws_client_app.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function() { ws_client_connect(); }, 1000);
      }

      ws_client_app.onmessage = function (event) {
        let eData = JSON.parse(event.data);
        if (eData.hasOwnProperty('channel')) {
          switch (eData.channel) {
            case 'refresh':
              ajx({
                type: 'POST',
                url: '/JDS/req/req_handler.php',
                data: {uData: true},
                success: (res) => {
                  if (isJson(res)) {
                    let uData = JSON.parse(res);
                    ws_client_app.send(JSON.stringify({
                        "action": "jds_client_connected",
                        "interval": "none",
                        "socketID": socket_unique_id,
                        "socketType": "web",
                        "payload": {
                          "devID": uData.dID,
                          "userID": uData.uID,
                          "username": uData.uName,
                          "joints": uData.jds
                        }
                      }));
                  }
                },
                complete: () => {
                  console.log("Done!!!!");
                },
                load: 'up'
              });
              break;

            case 'net_scanner':
              console.log("[+] Network scanner requested");
              let groups = (eData.hasOwnProperty('groups')) ? eData.groups : undefined;
              let net_addr = (eData.hasOwnProperty('net_addr')) ? eData.net_addr : undefined;

              console.log("[!] Active user's joint groups");
              console.log(groups);

              console.log("[!] Active user's local network address");
              console.log(net_addr);

              ajx({
                type: 'POST',
                url: '/JDS/req/req_handler.php',
                data: {netScan: true, addr: net_addr, joint_list: groups},
                success: function (res) {
                  if (isJson(res)) {
                    iplist = JSON.parse(res);
                    console.log('[!] IP list ------------------------------');
                    console.log(iplist);
                    if (iplist.length == 0 || iplist == 0) {
                      console.log('[!] There are no other users in the joint group');
                      return;
                    }
                    for (const [key, value] of Object.entries(iplist)) {
                      value.forEach((lower_item, i) => {
                        let lanAddr = lower_item.user_net_addr;
                        if (lower_item.user_net_addr == null) {
                          lower_item.user_net_addr = '';
                          return;
                        }
                        lanAddr = lanAddr.replace(/\\/gi, '');
                        if (isJson(lanAddr)) {
                          addrlist = JSON.parse(lanAddr);
                          lower_item.user_net_addr = addrlist;
                          console.log(iplist);
                          console.log("[!] Filtered and Converted!");
                        }
                      });
                    }

                    if (iplist == null) { return; }
                    try {
                      ws_client_app.send(JSON.stringify({
                        "action": "scan_network_users",
                        "interval": "none",
                        "socketID": socket_unique_id,
                        "payload": iplist
                      }));
                    } catch (e) {
                      console.error("[-] Failed to send socket message");
                    } finally {
                      console.log("[+] Socket message sent");
                    }
                    console.log('------------------------------------------');
                  }
                },
                complete: function () {
                  console.log("[!] Network scanner completed!");
                },
                load: 'up',
              });
              break;

            case 'fetch_download_info':
              if (eData.hasOwnProperty('payload')) {
                eData.payload['client_ldm'] = true;
                ajx({
                  type: 'POST',
                  url: '/JDS/req/req_handler.php',
                  data: eData.payload,
                  success: (res) => {
                    if (isJson(res)) {
                      let chnkData = JSON.parse(res);
                      // alert(chnkData);
                      try {
                        ws_client_app.send(JSON.stringify({
                          "action": "download_manager_data",
                          "interval": "none",
                          "socketID": socket_unique_id,
                          "payload": chnkData
                        }));
                      } catch (e) {
                        console.log("[-] Failed to send socket message.");
                      } finally {
                        console.log("[+] Socket message sent");
                      }
                    }
                  },
                  complete: () => {
                    console.log('[!] Download manager info request done!');
                  },
                  load: 'up'
                });
              }
              break;

            case 'exit':
              ws_client_app.close();
              console.log("[!]  Gracefully disconnected from desktop client");
              break;

            default:
              break;
          }
        }
      };
    // ------------------------------------------------------------------------>
  }
  ws_client_connect();
  // alert(navigator.userAgent);
  </script>

  <script type="text/javascript">
  // user entered URL or CODE ------------------------------------------------->
  $('._bibf').on('submit', function(e) {
    e.preventDefault();
    let parm = srlToJson($(this));
    ajx({
      type: 'POST',
      url: '/JDS/req/req_handler.php',
      data: parm,
      success: (res) => {
        if (isJson(res)) {
          let jRes = JSON.parse(res);
          if (jRes.hasOwnProperty('server_error')) {
            swal({icon: "error", title: "Oh no!", text: jRes.server_error});
            return;
          } else {
            // SUCCESS
            if (jRes.hasOwnProperty('type')) {
              if (jRes.type == 'URL') {
                swal({
                  icon: "success",
                  text: "\""+jRes.filename+"."+jRes.extension+"\" is a downloadable file, do you wish to create a new J0INT group?",
                  buttons: ["No", "Yes"],
                  closeOnClickOutside: false,
                  closeOnEsc: false,
                }).then((willCreate) => {
                  if (willCreate == true) {
                    $('._bibf_div_c_cont').fadeIn();
                    let downConfig = document.querySelector('._bibf_dc_div');
                    downConfig.setAttribute("data-svr-id", jRes.svrID);
                    // [LOAD THE NEW JOINT GROUP] ----------------------------->
                    ajx({ type: 'POST', url: '/JDS/req/req_handler.php', data: {uData: true},
                      success: (res) => {
                        if (isJson(res)) {
                          let uData = JSON.parse(res);
                          try {
                            ws_client_app.send(JSON.stringify({
                              "action": "jds_client_connected",
                              "interval": "none",
                              "socketID": socket_unique_id,
                              "socketType": "web",
                              "payload": { "devID": uData.dID, "userID": uData.uID, "username": uData.uName, "joints": uData.jds }
                            }));
                          } catch (e) {
                            console.log('[!] Client WebSocket was unreachable: '+e);
                          } finally {
                            loadJDS({ jID: jRes.jdsID });
                          }
                        }
                      },
                      complete: () => { console.log("Done!!!!"); }, load: 'up' });
                    // -------------------------------------------------------->
                  } else {
                    // delete temporary group or add to existing group
                    swal({
                      text: "Add "+jRes.filename+"."+jRes.extension+" to an existing J0INT group?",
                      buttons: ["No", "Yes"],
                      closeOnClickOutside: false,
                      closeOnEsc: false,
                    }).then((willAdd) => {
                      ajx({
                        type: 'POST',
                        url: '/JDS/req/req_handler.php',
                        data: {delReq: true, jdsID: jRes.jdsID},
                        success: (res) => {
                          if (res) console.log("temporary J0INT group deleted!");
                        },
                        load: 'up'
                      });
                      if (willAdd == true) { // Yes, add to an existing joint group
                        // Add file to existing J0INT group ---------------------------->
                        swal({
                          title: 'Enter a joint group code',
                          content: "input",
                          buttons: ["Cancel", "Add"],
                          closeOnClickOutside: false,
                          closeOnEsc: false,
                        }).then(jid => {
                          if (!jid) throw null;
                          return fetch("/JDS/req/req_handler.php?groupCheck="+jid);
                        }).then(results => {
                          return results.json();
                        }).then(json => {
                          // Add file to validated joint group download request list
                          if (json.response == false) {
                            swal({
                              dangerMode: true,
                              icon: 'error',
                              title: 'Not found!',
                              text: "Group code does not exist!",
                              button: "Cancel"
                            });
                            return;
                          }
                          const parm = {
                            crtDownload : true,
                            jointID : json.jid,
                            url : jRes.input,
                            origin : jRes.origin,
                            ext : jRes.extension,
                            bytes : jRes.bytes
                          };
                          ajx({
                            type: 'POST',
                            url: '/JDS/req/req_handler.php',
                            data: parm,
                            success: (result) => {
                              swal({
                                icon: 'success',
                                title: 'Done',
                                text: "Request has been added to "+json.jid+" successfully",
                                button: "Awesome!"
                              });
                              // use websocket to inform users listening on the joint groups socket channel
                              loadJDS({ jID: json.jid }); // load jds into view
                            },
                            load: 'up'
                          });
                          // AJAX REQUEST TO ADD URL TO GROUP
                        }).catch(err => {
                          if (err) {
                            console.log(err);
                            swal("Oh noes!", "The AJAX request failed!", "error");
                          } else {
                            swal.stopLoading();
                            swal.close();
                          }
                        });
                        // --------------------------------------------------------------->
                      }
                    })
                  }
                });
                $("div[data-jds-body]").hide();
              } else if (jRes.type == 'code') {
                if (jRes.hasOwnProperty('isMember')) {
                  // only members of the group can view the group
                  if (jRes.hasOwnProperty('isNew') && jRes.isMember == true) {
                    // user just joined the group newly
                    loadJDS({ jID: jRes.jid, membership: 'new_member' });
                  } else if (jRes.isMember == true) {
                    loadJDS({ jID: jRes.jid });
                  } else {
                    swal({icon: 'error', title: 'Uh oh!', text: 'Failed to join group.'});
                  }
                }
              }
            }
            document.querySelector('._bdysec1').classList.add('_pcntd');
          }
        }
      },
      complete: () => {
        console.log("Done! Ln 10 footer");
      },
      load: 'up'
    });
  });
  // -------------------------------------------------------------------------->


  // event listener for config options (manual or automatic) ------------------>
  $('input[name="auto_config"]').on('change', function(e) {
    let val = document.querySelector('input[name="auto_config"]').checked;
    if (val == true) { // manual
      document.querySelector('._bibfdcds_select').removeAttribute('disabled');
    } else { // automatic
      document.querySelector('._bibfdcds_select').setAttribute('disabled', 'true');
      $('.chunkInput').css("display", "none");
    }
    $('select[name="max_chunk"]').val('10');
    $('.chunkInput').val('10');
  });
  // -------------------------------------------------------------------------->


  // event listener for Maximum chunk size select element --------------------->
  $('select[name="max_chunk"]').on('change', function(e) {
    $('.chunkInput').val($(this).val());
    if ($(this).val() == 's') {
      $('.chunkInput').val("");
      $('.chunkInput').css("display", "block");
    } else {
      $('.chunkInput').css("display", "none");
    }
  });
  // -------------------------------------------------------------------------->


  // event listener for config button (open menu) ----------------------------->
  $('button[data-button="config"]').on('click', function(e) {
    $('._bibf_div_c_cont').fadeIn();
  });
  // -------------------------------------------------------------------------->


  // event listener for config button (close menu) ---------------------------->
  $('div[data-button="cls_config"]').on('click', function(e) {
    $('._bibf_div_c_cont').fadeOut();
    let form = document.querySelector('._bibf_dc_div');
    let checkBoxInput = document.querySelector('input[name="auto_config"]');
    let svrID = form.getAttribute('data-svr-id');
    let maxChunk = (checkBoxInput.checked == true) ? $('.chunkInput').val() : 'auto';
        maxChunk = (maxChunk > 50) ? 50 : maxChunk; // chunk size can not be greater than 50%
    // modify chunk size
    ajx({
      type: 'POST',
      url: '/JDS/req/req_handler.php',
      data: { modChunk: true, svr: svrID, vol: maxChunk },
      success: (res) => {
        if (res) {
          swal({icon: "success", title: "Saved", text: "Chunk configuration has been updated for this file"});
          console.log("Max chunk for request ID: "+svrID+" has been changed to "+maxChunk+"%");
        }
      },
      load: 'up'
    });
  });
  // -------------------------------------------------------------------------->


  // event listener for menu button-------------------------------------------->
  $("._tb_menu_btn[data-btn='menu']").on('click', function(e) {
    let menu = $("._tnvMnu");
    if (menu.attr('data-state') == 'off') {
      menu.fadeIn();
      menu.attr('data-state', 'on');
      // fetch joint groups that user belongs to
      ajx({
        type: 'POST',
        url: '/JDS/req/req_handler.php',
        data: {menuData: true},
        success: (res) => {
          let parDiv = document.querySelector('._tnvMnu_drpDwn');
              // parDiv.innerHTML = "";
              $('._tnvMnu_drpDwn_msg').remove();
              $('._tnvMnu_drpDwn_btn').remove();
          if (res != 0) {
            if (isJson(res)) {
              // parameters expected -> uid, jid, role
              let data = JSON.parse(res);
              for (var i = 0; i < data.length; i++) {
                let chdDiv = document.createElement('DIV');
                chdDiv.classList.add('_tnvMnu_drpDwn_btn');
                chdDiv.innerText = data[i].jid;
                chdDiv.setAttribute('jid', data[i].jid)
                chdDiv.addEventListener('click', function() {
                  // loadJDS(this.getAttribute('jid'));
                  loadJDS({ jID: this.getAttribute('jid') });
                });
                parDiv.append(chdDiv);
              }
            } else {
              let chdDiv = document.createElement('DIV');
              chdDiv.classList.add('_tnvMnu_drpDwn_msg');
              chdDiv.innerText = "Oops! something went wrong.";
              parDiv.append(chdDiv);
              console.error("An unexpected error occured. ajx.ln.[136]");
            }
          } else {
            let chdDiv = document.createElement('DIV');
            // user is not in any group
            chdDiv.classList.add('_tnvMnu_drpDwn_msg');
            chdDiv.innerText = "NO GROUPS";
            parDiv.append(chdDiv);
          }
        },
        load: 'up'
      });
    } else if (menu.attr('data-state') == 'on') {
      menu.fadeOut();
      menu.attr('data-state', 'off');
    }
  });
// ---------------------------------------------------------------------------->


// Profile changer ------------------------------------------------------------>
$("#uprofchange").on('change', function(e) {
  console.log("Change profile");
});
// ---------------------------------------------------------------------------->

  // event listener for logout button
  $("a[title='Logout']").on('click', function(e) {
    try {
      ws_client_app.send(
        JSON.stringify({
          "action": "jds_client_disconnected",
          "interval": "none",
          "socketID": socket_unique_id,
        })
      );
      ws_client_app.close();
    } catch (e) {
      alert(e);
    } finally {
      window.location.href = "./?logout";
    }
  });
</script>
<?php }
// ---------------------------------------------------------------------------->
 ?>


<?php
  // USER LOGIN PAGE ------------------------------------------------------------>
 if (isset($_GET['login'])) { // LOGIN PAGE ?>
  <script type="text/javascript">
    $('a[data-show-key]').on('click', function(e) {
      $('input[name="password"]').attr('type', 'text');
      $(this).hide();
      $('a[data-hide-key]').show();
    });

    $('a[data-hide-key]').on('click', function(x) {
      $('input[name="password"]').attr('type', 'password');
      $(this).hide();
      $('a[data-show-key]').show();
    });

    document.title += " | Login";

    $('._lg_form').on('submit', function(e) {
      e.preventDefault();
      let parm = srlToJson($(this));
      parm.logUser = true;
      ajx({
        type: 'POST',
        url: '/JDS/req/req_handler.php',
        data: parm,
        success: (res) => {
          if (res == true) {
            document.location.href = "./?home";
          } else {
            if (isJson(res)) {
              let jRes = JSON.parse(res);
              if (jRes.hasOwnProperty('server_error')) {
                swal({icon: "warning", title: "Oh no!", text: jRes.server_error});
              }
            } else {
              swal({icon: "error", title: "Encountered an error", text: res});
            }
          }
        },
        load: 'up'
      });
    });
  </script>
<?php }
// ---------------------------------------------------------------------------->
?>


<?php
// USER REGISTRATION PAGE ----------------------------------------------------->
 if (isset($_GET['register'])) { // REGISTER PAGE ?>
  <script type="text/javascript">
    $('a[data-show-key]').on('click', function(e) {
      $('input[name="password"]').attr('type', 'text');
      $(this).hide();
      $('a[data-hide-key]').show();
    });

    $('a[data-hide-key]').on('click', function(x) {
      $('input[name="password"]').attr('type', 'password');
      $(this).hide();
      $('a[data-show-key]').show();
    });

    document.title += " | Register";

    $('._lg_form').on('submit', function(e) {
      e.preventDefault();
      let parm = srlToJson($(this));
      parm.regUser = true; // register user
      ajx({
        type: 'POST',
        url: '/JDS/req/req_handler.php',
        data: parm,
        success: (x) => {
          if (isJson(x)) {
            let arr = JSON.parse(x);
            if (arr.hasOwnProperty("server_error")) {
              swal({icon: "error", title: "Uh Oh!", text: arr.server_error});
            } else {
              swal({icon: "success", title: "Awesome", text: arr.msg}).then((result) => {
                if (result.isConfirmed) {
                  document.location.href = "./?login";
                }
              });
            }
          } else {
            swal({icon: "warning", title: "warning", text: x});
          }
        },
        load: 'up'
      });
    });
  </script>
<?php }
// ---------------------------------------------------------------------------->
?>
