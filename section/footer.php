<?php
// USER HOME PAGE ------------------------------------------------------------->
 if (isset($_GET['home'])) { // HOME PAGE ?>
  <script type="text/javascript">
  // user entered URL or CODE ------------------------------------------------->
  $('._bibf').on('submit', function(e) {
    e.preventDefault();
    let parm = srlToJson($(this));
    ajx({
      type: 'POST',
      url: 'http://localhost/JDS/req/req_handler.php',
      data: parm,
      success: (res) => {
        console.log(res);
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
                })
                .then((willCreate) => {
                  if (willCreate) {
                    $('._bibf_div_c_cont').fadeIn();
                    let downConfig = document.querySelector('._bibf_dc_div');
                    downConfig.setAttribute("data-svr-id", jRes.svrID);
                    // show panes [LOAD JOINT GROUP] -------------------------->
                    loadJDS(jRes.jdsID);
                    // -------------------------------------------------------->
                  } else {
                    // delete temporary group or add to existing group
                    swal({
                      text: "Add "+jRes.filename+"."+jRes.extension+" to an existing J0INT group?",
                      buttons: ["No", "Yes"],
                    }).then((willAdd) => {
                      if (willAdd) {
                        swal("Choose where to add the file.");
                        // TODO: Add file to existing J0INT group
                      } else {
                        ajx({
                          type: 'POST',
                          url: 'http://localhost/JDS/req/req_handler.php',
                          data: {delReq: true, jdsID: jRes.jdsID},
                          success: (res) => {
                            if (res) console.log("temporary J0INT group deleted!");
                          },
                          load: 'up'
                        });
                      }
                    })
                  }
                });
                // swal({icon: "success", title: "File found!", text: jRes.filename+"."+jRes.extension+" is a downloadable file."});
                $("div[data-jds-body]").hide();
                // REQUEST TYPE IS A URL
              }
            }
            document.querySelector('._bdysec1').classList.add('_pcntd');
          }
        }
      },
      complete: () => {
        console.log("Done!");
      },
      load: 'up'
    });
  });
  // -------------------------------------------------------------------------->


  // event listener for config options (manual or automatic) ------------------>
  $('input[name="auto_config"]').on('change', function(e) {
    let val = document.querySelector('input[name="auto_config"]').checked;
    if (val == true) {
      document.querySelectorAll('._bibfdcds_select').forEach((e, i) => {
        e.removeAttribute('disabled');
      });
    } else {
      document.querySelectorAll('._bibfdcds_select').forEach((e, i) => {
        e.setAttribute('disabled', 'true');
        $('select[name="max_chunk"]').val('5');
        $('.chunkInput').css("display", "none");
      });
    }
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
    let svrID = form.getAttribute('data-svr-id');
    let maxChunk = $('.chunkInput').val();
    // modify chunk size
    ajx({
      type: 'POST',
      url: 'http://localhost/JDS/req/req_handler.php',
      data: { modChunk: true, svr: svrID, vol: maxChunk },
      success: (res) => {
        if (res) {
          swal({icon: "success", title: "Saved", text: "Download configuration has been updated for this file"});
          console.log("Max chunk for request ID: "+svrID+" has been changed to "+maxChunk+"MB");
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
        url: 'http://localhost/JDS/req/req_handler.php',
        data: {groupList: true},
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
                  loadJDS(this.getAttribute('jid'));
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


  // event listener for logout button
  $("a[title='Logout']").on('click', function(e) {
    window.location.href = "./?logout";
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
        url: 'http://localhost/JDS/req/req_handler.php',
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
        url: 'http://localhost/JDS/req/req_handler.php',
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
