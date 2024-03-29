<?php
// PACKAGES ---------------------------
include_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/class/standard.php';
include_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/class/auth.php';
include_once $_SERVER['DOCUMENT_ROOT'] . '/JDS/class/user.php';
// ------------------------------------


// OBJECTS [reusable] -----------------
$std = new stdlib();
$auth = new auth();
$usr = new user();
// ------------------------------------


// SECURITY CHECK {CHECK IF USER IS AUTHENTIC}
if (isset($_COOKIE['dKEY'])) {
  if ($auth->verfUser($_COOKIE['dKEY']) == false) {
    $result = array('server_error' => "Access violation detected!", 'code' => '403'); // forbidden
    // echo json_encode($result);
    header("location: ./?logout");
    exit();
  }
} else {
  $_SESSION['error'] = "Unauthorized access";
  header("location: ./?logout");
  exit();
}

// GET USER DATA
$userData = $usr->getUserByDeviceID($_COOKIE['dKEY']);

?>

<div class="_tnvbr">
  <a class="icon-menu _tb_menu_btn" data-btn="menu"></a>
  <h3 class="_tblgo" title="Joint Download Software">JDS</h3>
  <a class="icon-logout _tb_menu_btn _mnuli" title="Logout"></a>
</div>

<!-- Menu -->
<div class="_tnvMnu" data-state="off">

  <div data-group-block="PROFILE" class="_tnvMnu_drpProf">
    <div class="_tnvMnu_drpProf_img" style="background-image: linear-gradient(to top, #484848 0%, #0000002e 30%), url('https://itsyoungfox.github.io/static/media/original-favicon.e5940a02.png');">
      <label for="uprofchange" class="_tnvMnu_drpProf_img_edit">
        <i aria-hidden="true" class="icon-pencil"></i>
      </label>
      <input type="file" name="uprofile" id="uprofchange" class="hide"/>
    </div>
    <div class="_tnvMnu_drpProf_uname"><?php echo $userData['username']; ?></div>
  </div>

  <div class="_tnvMnu_drpDwn" data-group-block="J0INT">
    <a class="_tnvMnu_drpDwn_title">GROUPS</a> <!-- skeleton -->
    <div class="_tnvMnu_drpDwn_msg">Loading</div> <!-- skeleton -->
  </div>

</div>

<div class="_bdyMain">
  <div class="_bdysec1">
    <!-- Input bar -->
    <form class="_bibf" method="POST">
      <div class="_bibf_div">
        <input class="_bibftxt" name="path_code" placeholder="Enter URL or JDS code" type="text" required>
        <button type="submit" class="_bibfbtn icon-plus" title="New J0INT"></button>
      </div>
      <div class="floating_info">Don't have JDS extension? download from <a href="#">here</a></div>
    </form>

    <!-- Configuration menu -->
    <div class="_bibf_div_c_cont">
      <form class="_bibf_dc_div">
        <div class="_bibfdcd_section">
          <div class="_bibfdcds_title">Chunk configuration</div>
        </div>
        <div class="_bibfdcd_section">
          <div class="_bibfdcds_text">Split manually</div>
          <label class="switch"><input type="checkbox" name="auto_config"><span class="slider round"></span></label>
        </div>
        <div class="_bibfdcd_section">
          <div class="_bibfdcds_text v_row">
            <label>Maximum chunk size [%]</label>
            <select style="background: #EEE;" name="max_chunk" disabled class="_bibfdcds_select">
              <option value="auto" selected>auto</option>
              <option value="10">10%</option>
              <option value="20">20%</option>
              <option value="30">30%</option>
              <option value="50">50%</option>
              <option value="s">Specify</option>
            </select>
            <input type="text" style="display: none;" name="chunk_max_size" value="10" class="chunkInput" placeholder="Specify chunk size [%]">
          </div>
        </div>
        <div class="_bibfdcd_section">
          <div class="_bibfdcds_btn" data-button="cls_config">Save</div>
        </div>
      </form>
    </div>

  </div>

  <div class="_bdysec2">
    <div class="float_center_msg" data-jds-body>Enter a URL or a Group code to begin</div>
    <div class="_bs2_div_contr hide">

      <div class="_bs2dc_pane _pane_l">
        <div class="_bs2dcp_row _jds_holder">[CODE HERE]</div> <!-- skeleton -->
        <div class="_bs2dcp_row _jds_member">
          <div class="_bs2dcpr_container">
            <div class="_bs2dcprc_title">Members</div>
            <!-- skeleton -->
            <div class="_bs2dcprc_member">
              <a class="_mem _name">Stephen</a>
              <a class="_mem _stat">online</a>
            </div>
            <!-- skeleton -->
          </div>
        </div>
      </div>

      <div class="_bs2dc_pane _pane_r">
        <div class="_bs2dcpr_title">Downloads</div>

        <!-- SAMPLE -->
        <div class="_bs2dcp_row _jds_info">   <!-- main row -->
          <div class="_jdsi_row _info">       <!-- sub row 1 -->
            <div class="_jdsiri_row _rext">   <!-- sub row 1 1 -->
              <div class="_jdsiri_ext">       <!-- sub row 1 1 1 -->
                <a class="_ext">EXT</a>       <!-- sub row 1 1 1 1 -->
              </div>
            </div>
            <div class="_jdsiri_row">         <!-- sub row 1 2 -->
              <div class="_jdsirir_row">      <!-- sub row 1 2 1 -->
                <div class="_jdsirir_itm">    <!-- sub row 1 2 1 1-->
                  <a class="_jdsirir_itm_val">music.mp3</a>
                  <hr>
                  <a class="_jdsirir_itm_label">File</a>
                </div>
                <div class="_jdsirir_itm">    <!-- sub row 1 2 1 2-->
                  <a class="_jdsirir_itm_val">---</a>
                  <hr>
                  <a class="_jdsirir_itm_label">Estimated size</a>
                </div>
                <div class="_jdsirir_itm">    <!-- sub row 1 2 1 3-->
                  <a class="_jdsirir_itm_val">Downloading</a>
                  <hr>
                  <a class="_jdsirir_itm_label">Status</a>
                </div>
                <div class="_jdsirir_itm">    <!-- sub row 1 2 1 4-->
                  <a class="_jdsirir_itm_val">-.-.-.-</a>
                  <hr>
                  <a class="_jdsirir_itm_label">Source IP address</a>
                </div>
              </div>
              <div class="_jdsirir_row">      <!-- sub row 1 2 2 -->
                <div class="_dwnld_btn">      <!-- sub row 1 2 2 1 -->
                  <a class="icon-play _start"></a>
                </div>
                <div class="_dwnld_btn">      <!-- sub row 1 2 2 2 -->
                  <a class="icon-cog _conf"></a>      <!-- sub row 1 2 2 2 1 -->
                </div>
                <div class="_dwnld_bar">      <!-- sub row 1 2 2 3 -->
                  <div class="_dwnld_bar_inner"></div>      <!-- sub row 1 2 2 3 1 -->
                </div>
                <div class="_dwnld_btn">      <!-- sub row 1 2 2 4 -->
                  <a class="icon-trash _del"></a>      <!-- sub row 1 2 2 4 1 -->
                </div>
              </div>
            </div>
          </div>
          <div class="_jdsi_row _options"></div> <!-- sub row 2 -->
        </div>


        <!-- <div class="_bs2dcp_row"></div> -->
      </div>
    </div>
  </div>
</div>
